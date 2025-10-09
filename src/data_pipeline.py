
import pandas as pd
from sqlalchemy import create_engine, text
import requests
import time

# --- 1. Database Connection ---
db_url = 'postgresql://neondb_owner:npg_siXJHlLYwC10@ep-muddy-mode-ad05g277-pooler.c-2.us-east-1.aws.neon.tech/neondb'
engine = create_engine(
    db_url,
    pool_pre_ping=True,
    connect_args={'sslmode': 'require'}
)

def refresh_data():
    print("--- Starting Data Refresh ---")
    bootstrap_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    try:
        response = requests.get(bootstrap_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bootstrap data: {e}")
        return

    teams_df = pd.DataFrame(data['teams'])
    original_players_df = pd.DataFrame(data['elements'])
    gameweeks_df = pd.DataFrame(data['events'])
    player_types_df = pd.DataFrame(data['element_types'])

    next_gw_df = gameweeks_df[gameweeks_df['is_next'] == True]
    fixtures_df = pd.DataFrame()
    if not next_gw_df.empty:
        next_gw_id = next_gw_df['id'].iloc[0]
        try:
            fixtures_url = f'https://fantasy.premierleague.com/api/fixtures/?event={next_gw_id}'
            fixtures_df = pd.DataFrame(requests.get(fixtures_url).json())
        except requests.exceptions.RequestException as e:
            print(f"Error fetching fixtures data: {e}")

    player_history_data = []
    player_ids = original_players_df['id'].tolist()
    for i, player_id in enumerate(player_ids):
        try:
            player_url = f'https://fantasy.premierleague.com/api/element-summary/{player_id}/'
            history = requests.get(player_url).json().get('history', [])
            for item in history:
                item['element'] = player_id
                player_history_data.append(item)
            time.sleep(0.02)
        except requests.exceptions.RequestException:
            continue
    player_history_df = pd.DataFrame(player_history_data)

    gameweek_cols = ['id', 'name', 'deadline_time', 'finished', 'is_previous', 'is_current', 'is_next']
    gameweeks_df = gameweeks_df[gameweek_cols]

    player_cols = {
        'id': 'id', 'first_name': 'Nombre', 'second_name': 'Apellido', 'team': 'team_id', 
        'element_type': 'Posicion', 'now_cost': 'Precio', 'total_points': 'Puntos Totales',
        'cost_change_event': 'tendencia'
    }
    players_df = original_players_df[list(player_cols.keys())].rename(columns=player_cols)
    players_df['Posicion'] = players_df['Posicion'].map(player_types_df.set_index('id')['singular_name'])

    try:
        with engine.begin() as conn:
            for table in ["fixtures", "player_history", "players", "teams", "gameweeks", "player_types"]:
                conn.execute(text(f"DROP TABLE IF EXISTS {table};"))
            teams_df.to_sql('teams', conn, index=False, if_exists='replace')
            gameweeks_df.to_sql('gameweeks', conn, index=False, if_exists='replace')
            player_types_df.to_sql('player_types', conn, index=False, if_exists='replace')
            players_df.to_sql('players', conn, index=False, if_exists='replace')
            if not player_history_df.empty: player_history_df.to_sql('player_history', conn, index=False, if_exists='replace')
            if not fixtures_df.empty: fixtures_df.to_sql('fixtures', conn, index=False, if_exists='replace')
        print("--- Data Refresh Complete ---")
    except Exception as e:
        print(f"An error occurred during database operations: {e}")

def get_data_from_db():
    print("--- Loading data from database ---")
    try:
        with engine.connect() as conn:
            return {name: pd.read_sql(f"SELECT * FROM {name}", conn) for name in ["players", "teams", "gameweeks", "player_history", "fixtures"]}
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None

def calculate_features(db_data):
    print("--- Calculating features ---")
    players_df = db_data['players'].set_index('id')
    teams_df = db_data['teams'].set_index('id')
    history_df = db_data['player_history']
    fixtures_df = db_data['fixtures']

    # Form
    if not history_df.empty:
        history_df = history_df.sort_values(by=['element', 'round'])
        form = history_df.groupby('element')['total_points'].apply(lambda x: x.shift(1).rolling(5, min_periods=1).mean())
        players_df['form'] = form.groupby('element').last()

    # Difficulty
    if not fixtures_df.empty:
        opp_map = {row['team_h']: {'opp': row['team_a'], 'home': True} for _, row in fixtures_df.iterrows()}
        opp_map.update({row['team_a']: {'opp': row['team_h'], 'home': False} for _, row in fixtures_df.iterrows()})
        players_df['opponent'] = players_df['team_id'].map(lambda x: opp_map.get(x, {}).get('opp'))
        players_df['is_home'] = players_df['team_id'].map(lambda x: opp_map.get(x, {}).get('home'))
        def get_strength(row):
            if pd.isna(row['opponent']): return None
            strength = teams_df.loc[row['opponent']]
            return strength['strength_overall_away'] if row['is_home'] else strength['strength_overall_home']
        players_df['difficulty'] = players_df.apply(get_strength, axis=1)

    # Value
    players_df['valor'] = (players_df['form'] / (players_df['Precio'] / 10.0)).fillna(0)
    return players_df.reset_index()

def train_and_predict(players_df, history_df, teams_df):
    print("--- Training model and predicting xPts ---")
    # 1. Create historical training data
    train_df = history_df[['element', 'round', 'opponent_team', 'was_home', 'total_points']].copy()
    train_df = train_df.sort_values(by=['element', 'round'])
    
    # Add historical form
    train_df['form'] = train_df.groupby('element')['total_points'].apply(lambda x: x.shift(1).rolling(5, min_periods=1).mean())
    
    # Add historical difficulty
    teams_strength = teams_df.set_index(teams_df.index.astype(int))
    def get_hist_strength(row):
        opp_strength = teams_strength.loc[row['opponent_team']]
        return opp_strength['strength_overall_away'] if row['was_home'] else opp_strength['strength_overall_home']
    train_df['difficulty'] = train_df.apply(get_hist_strength, axis=1)

    # Merge player position
    train_df = train_df.merge(players_df[['id', 'Posicion']], left_on='element', right_on='id', how='left')
    train_df.dropna(inplace=True)

    # 2. Train model
    features = ['form', 'difficulty', 'Posicion']
    target = 'total_points'
    X = train_df[features]
    y = train_df[target]

    preprocessor = ColumnTransformer(transformers=[
        ('pos', OneHotEncoder(handle_unknown='ignore'), ['Posicion'])
    ], remainder='passthrough')

    model = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', LinearRegression())])
    model.fit(X, y)

    # 3. Predict on current players
    current_features = players_df[['id', 'form', 'difficulty', 'Posicion']].copy()
    current_features.dropna(inplace=True)
    
    if not current_features.empty:
        predictions = model.predict(current_features[features])
        pred_df = pd.DataFrame({'id': current_features['id'], 'xPts': predictions})
        players_df = players_df.merge(pred_df, on='id', how='left')
        players_df['xPts'] = players_df['xPts'].clip(lower=0).round(2) # Clean up predictions

    return players_df

if __name__ == '__main__':
    # refresh_data() # Run this only when you need to update from the API
    db_data = get_data_from_db()

    if db_data:
        players_df = calculate_features(db_data)

        # Add team names for readability
        team_map = db_data['teams'].set_index('id')['name'].to_dict()
        players_df['team_name'] = players_df['team_id'].map(team_map)
        players_df['opponent_name'] = players_df['opponent'].map(team_map)

        # --- 5. Save and Display Results ---
        final_cols = ['Nombre', 'Apellido', 'team_name', 'Posicion', 'opponent_name', 'is_home', 'Precio', 'form', 'difficulty', 'valor', 'tendencia']
        final_df = players_df.sort_values('valor', ascending=False)[final_cols].reset_index(drop=True)
        
        output_filename = 'resultados.csv'
        try:
            final_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
            print(f"\nSuccessfully saved final results to {output_filename}")
        except Exception as e:
            print(f"\nError saving results to file: {e}")

        print("\n--- Final Player Features (Top 15 by Value) ---")
        print(final_df.head(15))
