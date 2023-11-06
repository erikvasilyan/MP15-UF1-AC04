import matplotlib.pyplot as plt
import pandas as pd

# TITLE: MP15-UF1-AC04 - Exercicis Python IV
# NAME: Erik Vasilyan, Marçal Herraiz
# DATA: 2023-10-30


def fetch_csv_data(csv_file_path):
    return pd.read_csv(csv_file_path, header=0)


stations_path = 'CSV/2020_MeteoCat_Estacions.csv'
stations_details_path = 'CSV/2022_MeteoCat_Detall_Estacions.csv'
metadata_path = 'CSV/MeteoCat_Metadades.csv'

stations = fetch_csv_data(stations_path)
stations_details = fetch_csv_data(stations_details_path)
metadata = fetch_csv_data(metadata_path)

# GRAPHICS - Visualitza temperatura mitjana del mes de Febrer

stations_details['DATA_LECTURA'] = pd.to_datetime(stations_details['DATA_LECTURA'])

february_data = stations_details[
    (stations_details['DATA_LECTURA'].dt.month == 2) &
    (stations_details['DATA_LECTURA'].dt.year == 2022) &
    (stations_details['ACRÒNIM'] == 'TM')]

temperatures_per_station = february_data.groupby(['CODI_ESTACIO', february_data['DATA_LECTURA'].dt.day])['VALOR'].mean().unstack(level=0)

print("Matplotlib current backend: Agg")

plt.figure(figsize=(10, 6))

for station in temperatures_per_station.columns:
    plt.plot(temperatures_per_station.index, temperatures_per_station[station], label=f'Estación {station}', marker='o')

plt.xlabel('Días de Febrero')
plt.ylabel('Temperatura media diaria')
plt.title('Comparativa de Temperatura Media Diaria - Febrero 2022')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xticks(temperatures_per_station.index)
plt.savefig('Graphics/grafico_temperaturas.png')
