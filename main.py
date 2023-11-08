import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# TITLE: MP15-UF1-AC04 - Exercicis Python IV
# NAME: Erik Vasilyan, Marçal Herraiz
# DATA: 2023-11-08


def fetch_csv_data(csv_file_path):
    return pd.read_csv(csv_file_path, header=0)


def exercise_3():  # GRAPHIC - Visualitza temperatura mitjana del mes de Febrer
    
    # Part 1
    plt.figure(figsize=(10, 6))
    for station in temperatures_per_station.columns:
        plt.plot(temperatures_per_station.index, temperatures_per_station[station], label=f'Estación {station}',
                 marker='o')
    plt.xlabel('Días de Febrero')
    plt.ylabel('Temperatura media diaria')
    plt.title('Comparativa de Temperatura Media Diaria - Febrero 2022')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(temperatures_per_station.index)
    plt.savefig('Graphics/exercise-3-1.png')

    # Part 2
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle('Comparativa de Temperatura Media Diaria - Febrero 2022')

    for i in range(4):
        plt.subplot(2, 2, i + 1)
        plt.plot(temperatures_per_station.index, temperatures_per_station[temperatures_per_station.columns[i]],
                 label=f'Estación {temperatures_per_station.columns[i]}', marker='o', color=plt.cm.tab10(i))
        plt.xlabel('Días de Febrero')
        plt.ylabel('Temperatura media diaria')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.xticks(temperatures_per_station.index)
        plt.ylim(temperatures_per_station.min().min()-1, temperatures_per_station.max().max()+1)
        plt.savefig('Graphics/exercise-3-2.png')


def exercise_4():  # GRAPHIC - Predicció temperatura mes de Febrer
    february_2022_mean = temperatures_per_station.mean().mean()
    february_2023_prediction = february_2022_mean

    print(
        f"Predicción de temperatura media estándar para febrero de 2023: {int(round(february_2023_prediction))} grados")

    daily_median_temperatures = temperatures_per_station.median(axis=1).round().astype(int)

    plt.figure(figsize=(8, 4))
    plt.hist(daily_median_temperatures, bins=20, color='skyblue')
    plt.xlabel('Temperatura')
    plt.ylabel('Cantidad de días')
    plt.title('Distribución de temperaturas - Febrero 2022')
    plt.xticks(np.unique(daily_median_temperatures))
    plt.ylim(0, max(plt.hist(daily_median_temperatures, bins=20, color='skyblue')[0]) + 2)
    plt.savefig('Graphics/exercise-4.png')

    days_in_february_2023 = 28
    february_2023_random_temperatures = np.round(
        np.random.normal(february_2023_prediction, 2, days_in_february_2023)).astype(int)

    print("Valores de temperatura aleatoria para febrero de 2023:")
    for i, temperature in enumerate(february_2023_random_temperatures, start=1):
        print(f"{i} de febrero: {temperature} grados")


def exercise_5():  # GRAPHIC - Predicció pluges mes de Febrer

    february_rain_data_2022 = stations_details[
        (stations_details['DATA_LECTURA'].dt.month == 2) &
        (stations_details['DATA_LECTURA'].dt.year == 2022) &
        (stations_details['ACRÒNIM'] == 'PPT')
    ]

    february_rain_per_station = february_rain_data_2022.groupby(['CODI_ESTACIO', february_rain_data_2022['DATA_LECTURA'].dt.day])[
        'VALOR'].mean().unstack(level=0)

    daily_median_rain = february_rain_per_station.median(axis=1)

    rainy_days_bool = daily_median_rain > 0

    days_of_february = range(1, len(daily_median_rain) + 1)

    plt.figure(figsize=(15, 6))
    plt.bar(days_of_february, rainy_days_bool, color=['blue' if rain else 'orange' for rain in rainy_days_bool])
    plt.xlabel('Días de Febrero')
    plt.ylabel('Lluvia (True/False)')
    plt.title('Predicción de lluvia para Febrero 2023')
    plt.yticks([0, 1], ['No llueve', 'Llueve'])
    plt.xticks(days_of_february)
    plt.savefig('Graphics/exercise-5-2.png')

    rainy_days_count = np.sum(rainy_days_bool)
    non_rainy_days_count = len(rainy_days_bool) - rainy_days_count

    labels = ['Llueve', 'No llueve']
    sizes = [rainy_days_count, non_rainy_days_count]
    colors = ['#75cfb8', '#f8b195']
    explode = (0.1, 0)
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title('Proporción de lluvia para Febrero 2023')
    plt.savefig('Graphics/exercise-5-1.png')


stations_path = 'CSV/2020_MeteoCat_Estacions.csv'
stations_details_path = 'CSV/2022_MeteoCat_Detall_Estacions.csv'
metadata_path = 'CSV/MeteoCat_Metadades.csv'

stations = fetch_csv_data(stations_path)
stations_details = fetch_csv_data(stations_details_path)
metadata = fetch_csv_data(metadata_path)

stations_details['DATA_LECTURA'] = pd.to_datetime(stations_details['DATA_LECTURA'])

february_data = stations_details[
    (stations_details['DATA_LECTURA'].dt.month == 2) &
    (stations_details['DATA_LECTURA'].dt.year == 2022) &
    (stations_details['ACRÒNIM'] == 'TM')]

temperatures_per_station = february_data.groupby(['CODI_ESTACIO', february_data['DATA_LECTURA'].dt.day])[
    'VALOR'].mean().unstack(level=0)

# MAKE GRAPHICS AND SAVE IT
exercise_3()
exercise_4()
exercise_5()
