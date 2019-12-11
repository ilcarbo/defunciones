import streamlit as st
import pandas as pd
#import pickle

st.markdown('# 💀¿Cómo podrías morir hoy?💀')
#st.title('¿De qué te vas a morir?')
st.write('Utilizando los datos históricos de defunciones entre 2010 y 2017 se calculan las muertes' +
        ' más frecuentes para tu grupo etario, sexo y provincia de residencia.' +
         '\n Fuente(http://www.deis.msal.gov.ar/index.php/base-de-datos/)')

#por_causa = pd.read_csv('./por_causa.csv')
por_causa = pd.read_pickle('./adicionales/por_causa.pkl')
causa = pd.read_csv('./adicionales/causa.csv')
def_dict = causa.set_index('CAUSA')['DESCRIPCION'].to_dict()
 

# Generar selector para provincia
prov = st.selectbox('¿En qué provincia vivís?', por_causa['PROVRES'].unique())
# Generar selector para Sexo
sexo_v = st.selectbox('¿Cuál es tu sexo biológico?', ['Masculino', 'Femenino'])
sexo = 1 if sexo_v == 'Masculino' else 2
# Generar casillero para edad
edad = st.slider('¿Cuál es tu edad?', min_value=0, max_value=110, value=30, step=1)

# Primer filtrado por edades
mask = por_causa['GRUPEDAD'].apply(lambda x: edad in x)
filt1 = por_causa[mask]
# filtrado por provincia y sexo
row = pd.DataFrame(filt1.loc[(filt1['PROVRES'] == prov) & (filt1['SEXO'] == sexo)])
#row = filt1.loc[(filt1['PROVRES'] == prov) & (filt1['SEXO'] == sexo)].copy()
row.index = [0]

#st.write(row)

if st.button('Calcular!!!'):
    # Eliminar NaNs
    row.dropna(axis= 1, inplace= True)
    #row.fillna(0, inplace= True)
    # Eliminar Columnas que no me permiten ordenar y ordenar columnas
    #row.drop(['PROVRES', 'SEXO', 'GRUPEDAD'], axis= 1, inplace= True)
    final = row.drop(['PROVRES', 'SEXO', 'GRUPEDAD'], axis= 1).sort_values(by = 0, axis= 1, ascending= False)
    #row.sort_values(by = 229, axis= 1, inplace = True, ascending= False)
    #st.write(row)
    #st.write(final)

    st.title('Las 5 causas de muerte más comunes para tu sexo, edad y provincia de residencia son:')
    st.markdown('**1:** ' + def_dict[final.columns[0]])
    st.markdown('**2:** ' + def_dict[final.columns[1]])
    st.markdown('**3:** ' + def_dict[final.columns[2]])
    st.markdown('**4:** ' + def_dict[final.columns[3]])
    st.markdown('**5:** ' + def_dict[final.columns[4]])
    
st.markdown('-----------------------------------')
st.markdown('Las causas de muerte corresponden a la _"Clasificación internacional de enfermedades, 10.ª edición"_')
st.markdown("Creado por: [@ilcarbo](https://www.twitter.com/ilcarbo)")
st.markdown("[Acceder al código](https://www.twitter.com/ilcarbo)")