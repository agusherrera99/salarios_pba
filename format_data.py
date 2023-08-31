import pandas as pd

indec = pd.read_csv("csvs/cod_dptos_indec.csv")
salarios = pd.read_csv("csvs/salario_prom_dpt-part_total.csv")
afip = pd.read_csv("csvs/dic_clases_afip.csv")

# Preparación de data
indec = indec[["codigo_departamento_indec", "nombre_departamento_indec", "nombre_provincia_indec"]]
afip = afip[["clae2", "clae2_desc",]]

merge_1 = pd.merge(indec, salarios, on="codigo_departamento_indec")
data = pd.merge(merge_1, afip, on="clae2")

data = data[
    [
        "nombre_departamento_indec",
        "nombre_provincia_indec",
        "fecha",
        "w_mean",
        "clae2_desc",
    ]
].copy()

data = data.rename(
    columns={
        "fecha": "Fecha",
        "w_mean": "Promedio",
        "clae2_desc": "Actividad",
        "nombre_departamento_indec": "Partido",
        "nombre_provincia_indec": "Provincia",
    }
).copy()

data = data.query('Provincia == "Buenos Aires" | Provincia == "CABA"').copy()

data.to_pickle('pkls/pba.pkl')