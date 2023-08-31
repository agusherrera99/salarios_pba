import pandas as pd 

# Diccionario base
base = {}

# Dataframes
data_pkl = pd.read_pickle('pkls/pba.pkl')
dolar_pkl = pd.read_pickle('pkls/dollar_values.pkl')

cities = list(set(data_pkl['Partido']))

for city in cities:
    base[city] = {}

for city in base.keys():
    print(city)
    # Preparación de Data
    df = data_pkl.query(F'Partido == "{city}"').copy()
    df = df[df['Promedio'] != -99].copy()
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Lista con todas las actividades registradas.
    activities = list(set(df['Actividad']))

    # Para cada actividad se crea un DataFrame de Pandas, se reorganizan los promedios de manera anual y se añaden a las listas correspondientes
    for activity in activities:
        df_activity = df.query(F'Actividad == "{activity}"')
        df_anual = df_activity.groupby(df_activity['Fecha'].dt.year)['Promedio'].mean()
        if len(df_anual.keys()) <= 3:
            pass
        else:
            base[city].setdefault(activity.title(), {'ARS': [[], []], 'USD': [[], []]})
            for year, avg in df_anual.items():
                base[city][activity.title()]['ARS'][0].append(year)
                base[city][activity.title()]['USD'][0].append(year)
                base[city][activity.title()]['ARS'][1].append(avg)

                # Añade los promedios correspondientes a los años a la lista USD, utilizando la cotización correcta para cada año.
                dolar_serie = dolar_pkl.query(F'Año == {str(year)}')
                base[city][activity.title()]['USD'][1].append(avg / dolar_serie['Promedio'].values[0])

# pd.to_pickle(base, 'pkls/pba_dict.pkl')