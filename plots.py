import locale
# --------------- 
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

pba_pkl = pd.read_pickle('pba_dict_copy.pkl')

# Título y selectores para ciudad y actividad en streamlit.
st.title('Promedio Anual de Salarios Mensuales a lo Largo del Tiempo en la Provincia de Buenos Aires.')
city = st.selectbox(label='Selecciona una Ciudad.', options=pba_pkl.keys())
activity = st.selectbox(label='Seleccione Actividad a Visualizar.', options=pba_pkl[city].keys())

#Listas con datos a visualizar 
ars = pba_pkl[city][activity]['ARS']
usd = pba_pkl[city][activity]['USD']

plt.style.use('dark_background')

def createPlot(currency, dollar=False):
    year = currency[0]
    avg = currency[1]

    fontsize = 16

    fig, ax = plt.subplots(figsize=(12, 10))
    if dollar:
        bars = ax.bar(year, avg, tick_label=year, color='#4ade80')
        ax.set_title(F'Promedio Anual de Salarios en Dólares \n Sector: {activity}', fontsize=fontsize)
        ax.set_xlabel('Año', fontsize=fontsize)
        ax.set_ylabel('Salario Mensual en Dolares', fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=fontsize)
    else:
        bars = ax.bar(year, avg, tick_label=year, color='#60a5fa')
        ax.set_title(F'Promedio Anual de Salarios Mensuales en Pesos \n Sector: {activity}', fontsize=fontsize)
        ax.set_xlabel('Año', fontsize=fontsize)
        ax.set_ylabel('Salario Mensual', fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=fontsize)
    
    # Agrega valores a las barras
    def addValueToBar(bars):
        for bar in bars:
            yval = bar.get_height()
            formatted_yval = "${:,.0f}".format(round(yval))
            ax.text((bar.get_x() + bar.get_width() / 2), (yval), formatted_yval, ha='center', va='bottom', fontsize=14)

    addValueToBar(bars)

    #Visualización del gráfico en streamlit 
    st.pyplot(fig)

createPlot(ars)
createPlot(usd, dollar=True)

st.write(F'Autor: Agustin Herrera | agustinherrera.dev@gmail.com')
st.write(F'Data: https://datos.gob.ar/dataset/produccion-salarios-por-departamentopartido-sector-actividad | https://www.ambito.com/contenidos/dolar-informal-historico.html')