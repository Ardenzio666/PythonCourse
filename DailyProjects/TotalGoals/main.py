import requests
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# URL del file CSV
url = 'https://www.football-data.co.uk/mmz4281/2021/E0.csv'

# Effettua una richiesta GET per scaricare il file CSV
response = requests.get(url)


# Controlla se la richiesta ha avuto successo
if response.status_code == 200:
    # Leggi il contenuto del CSV in un DataFrame di pandas
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)

    # Mostra i primi 5 record del DataFrame
    print(df.head())
else:
    print(f"Errore nel scaricare il file CSV: {response.status_code}")

squadre = df['HomeTeam'].unique()
df_small = df[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]

#soluzione ottimizzata
# Raggruppiamo e sommiamo i gol in casa e in trasferta in una singola operazione
pd.set_option('display.max_columns', None)
print(df_small.head())
# Raggruppiamo e sommiamo i gol in casa e in trasferta in una singola operazione
total_goals_home = df_small.groupby('HomeTeam')['FTHG'].sum().rename('TotalHomeGoals').reset_index()
total_goals_away = df_small.groupby('AwayTeam')['FTAG'].sum().rename('TotalAwayGoals').reset_index()

# Uniamo i risultati delle somme
total_goals_teams = pd.merge(total_goals_home, total_goals_away, left_on='HomeTeam', right_on='AwayTeam', how='outer').fillna(0)

# Calcoliamo il totale dei gol per ogni squadra
total_goals_teams['TotalGoal'] = total_goals_teams['TotalHomeGoals'] + total_goals_teams['TotalAwayGoals']
total_goals_teams = total_goals_teams.rename(columns={'HomeTeam': 'Team'})
total_goals_teams = total_goals_teams[['Team', 'TotalGoal']]

# Uniamo i risultati delle somme al DataFrame originale
df_small = df_small.merge(total_goals_teams, left_on='HomeTeam', right_on='Team', how='left').drop('Team', axis = 1)
df_small = df_small.merge(total_goals_teams, left_on='AwayTeam', right_on='Team', how='left').drop('Team',  axis = 1)



print(df_small)
# Applica la colormap 'viridis' ai valori delle barre
cmap = cm.get_cmap('viridis')
norm = plt.Normalize(total_goals_teams['TotalGoal'].min(), total_goals_teams['TotalGoal'].max())
colors = cmap(norm(total_goals_teams['TotalGoal']))
# Ordina il DataFrame in ordine decrescente in base ai gol totali
total_goals_teams = total_goals_teams.sort_values(by='TotalGoal', ascending=False)

# Crea il grafico
plt.figure(figsize=(10, 8))
plt.barh(total_goals_teams['Team'], total_goals_teams['TotalGoal'], color=colors)
plt.xlabel('Total Goals')
plt.title('Total Goals Scored by Each Team in the 2020/2021 Season')
plt.gca().invert_yaxis()  # Inverti l'asse y per avere le barre ordinate dall'alto verso il basso
plt.show()



