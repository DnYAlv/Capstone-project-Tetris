import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import lorem
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from numerize import numerize
from scipy.stats.stats import pearsonr

# Set Page
st.set_page_config(layout='wide')

# Dataset Loading

df = pd.read_csv('./Datasets/data_kualitas_udara.csv')

# Data preprocessing

df['tanggal'] = pd.to_datetime(df['tanggal'])

# Title
st.title('Kualitas Udara di DKI Jakarta Selama Masa Pandemi COVID-19')
st.markdown('***Polusi Udara*** di DKI Jakarta diyakini sudah berkurang selama pandemi COVID-19, namun apakah benar demikian?')

# Chart (Full 2017 - 2021)
st.subheader('Distribusi Materi Partikel Faktor Polusi Udara (2017-2021)')
select_freq, chart_full = st.columns([1,4])

chosen_freq = ''
with select_freq:
    freq = st.selectbox('Frekuensi Periode Waktu', ('Minggu','Bulan','Tahun'))
    if freq == 'Minggu':
        chosen_freq = 'W'
    elif freq == 'Bulan':
        chosen_freq = 'M'
    else:
        chosen_freq = 'Y'

with chart_full:
    data_full = df[['tanggal','pm10','so2','co','no2','o3']].set_index('tanggal').resample(chosen_freq).sum()
    st.line_chart(data_full)

st.write('Pada bulan Juli tahun 2020, terdapat ***sedikit penurunan*** volume materi partikel polusi udara di semua partikel yang ada, di mana pada bulan ini pandemi COVID-19 sedang berada pada tahap awal penyebaran sehingga banyak orang yang mengurangi aktivitas luar rumah seperti penggunaan kendaraan bermotor dan lainnya. Hal ini tidak berlangsung lama, di mana di bulan berikutnya, volume partikel polusi udara ini kembali meningkat selama pandemi COVID-19 berlangsung.')

# Chart each Year
st.subheader('Distribusi Kategori Kualitas Udara tiap Tahun')
selected_year, chart_1, chart_2 = st.columns([1,2,2])

chosen_year = -1
with selected_year:
    year = st.select_slider('Tahun',options=['2017','2018','2019','2020','2021'])
    if year == '2017':
        chosen_year = 2017
    elif year == '2018':
        chosen_year = 2018
    elif year == '2019':
        chosen_year = 2019
    elif year == '2020':
        chosen_year = 2020
    else:
        chosen_year = 2021

data = df[['tanggal','pm10','so2','co','no2','o3','categori']].set_index('tanggal')
data = data[data.index.year == chosen_year]['categori'].value_counts()
chart_data = pd.DataFrame()
chart_data['Categories'] = data.index
chart_data['Jumlah Sampel'] = data.values

with chart_1:
    fig = px.bar(chart_data, x='Categories', y ='Jumlah Sampel', color='Jumlah Sampel')
    fig.update_layout( yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    st.caption('Distribusi Kategori Kualitas Udara pada Tahun '+ year)

with chart_2:
    labels = list(chart_data['Categories'])
    values = list(chart_data['Jumlah Sampel'])

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_layout(annotations=[dict(text=str(chosen_year), x=0.5, y=0.5,font_size=20, showarrow=False)])
    st.plotly_chart(fig, use_container_width=True)
    

# Metrics
st.markdown('### Volume Partikel Udara')
met1, met2, met3, met4, met5, met6 = st.columns(6)
df_now = df[df['tanggal'].dt.year == chosen_year]
df_last = df[df['tanggal'].dt.year == chosen_year-1]


with met1:
    if chosen_year == 2017:
        percentage = 0
    else:
        percentage = (df_now['pm10'].sum() - df_last['pm10'].sum()) / df_last['pm10'].sum()

    st.metric(
        'PM10',
        numerize.numerize(df_now['pm10'].sum()),
        str(round(percentage*100,2)) + '%'
    )

with met2:
    if chosen_year == 2017:
        percentage = 0
    else:
        percentage = (df_now['co'].sum() - df_last['co'].sum()) / df_last['co'].sum()

    st.metric(
        'co',
        numerize.numerize(df_now['co'].sum()),
        str(round(percentage*100,2)) + '%'
    )

with met3:
    if chosen_year == 2017:
        percentage = 0
    else:
        percentage = (df_now['no2'].sum() - df_last['no2'].sum()) / df_last['no2'].sum()

    st.metric(
        'no2',
        numerize.numerize(df_now['no2'].sum()),
        str(round(percentage*100,2)) + '%'
    )

with met4:
    if chosen_year == 2017:
        percentage = 0
    else:
        percentage = (df_now['o3'].sum() - df_last['o3'].sum()) / df_last['o3'].sum()

    st.metric(
        'o3',
        numerize.numerize(df_now['o3'].sum()),
        str(round(percentage*100,2)) + '%'
    )

with met5:
    if chosen_year == 2017:
        percentage = 0
    else:
        percentage = (df_now['so2'].sum() - df_last['so2'].sum()) / df_last['so2'].sum()

    st.metric(
        'so2',
        numerize.numerize(df_now['so2'].sum()),
        str(round(percentage*100,2)) + '%'
    )

with met6:
    st.markdown('#### Tahun ' + str(chosen_year))

# Penjelasan
st.write('Tetap terdapat kenaikan volume materi partikulat udara yang menandakan bahwa tetap terdapat pencemaran udara selama pandemi COVID-19, namun demikian, pada masa sebelum pandemi berlangsung (2017, 2020), bisa dilihat bahwa konsentrasi pencemaran udara mencapai tahap kategori *SANGAT TIDAK SEHAT*, yang mana hal ini berbeda pada masa pandemi berlangsung (tidak mencapai kategori *SANGAT TIDAK SEHAT*).')

# Correlation Analysis
st.subheader('Korelasi Antar Partikel Udara')

choose_1, chart_corr, correlation = st.columns([1,3,1])

with choose_1:
    part = st.selectbox('Partikel 1', ('PM10','CO','NO2','O3','SO2'))

    part2 = st.selectbox('Partikel 2',('PM10','CO','NO2','O3','SO2'))

with chart_corr:
    fig = px.scatter(df, x=part.lower(), y=part2.lower(), color='categori')
    st.plotly_chart(fig, use_container_width=True)

with correlation:
    corr_part = pearsonr(df[part.lower()], df[part2.lower()])
    st.markdown(f'##### Korelasi antara {part} dengan {part2}')
    percent = round(abs(corr_part[0])*100,2)

    if percent > 50:
        percent_status = 'Korelasi Tinggi'
    elif percent > 30:
        percent_status = 'Korelasi Sedang'
    else:
        percent_status = 'Korelasi Rendah'

    st.subheader(f'{percent}%')
    st.markdown(f'##### ***{percent_status}***')

st.subheader('Kesimpulan')
st.write('Hasil analisis yang saya dapatkan yaitu ***terdapat perubahan kualitas udara*** selama pandemi COVID-19 berlangsung, yang mana polusi udara sedikit berkurang meskipun tidak berlangsung lama, hal ini disebabkan karena meskipun pemakaian kendaraan bermotor bisa saja berkurang selama pandemi, namun penggunaan alat listrik di rumah juga semakin meningkat. Dengan demikian, pencemaran udara tetap terjadi di DKI Jakarta')

# Side Bar

with st.sidebar:
    st.title('Capstone Project Tetris Dashboard')
    st.write('by: Denny Alvito Ginting')
    
    # Penjelasan Partikel Polusi
    with st.expander('Apa itu PM10?'):
        st.write('Menurut [BMKG](https://www.bmkg.go.id/kualitas-udara/informasi-partikulat-pm10.bmkg#:~:text=Partikulat%20(PM10)%20adalah%20Partikel,%3D%20150%20%C2%B5gram%2Fm3.), PM10 merupakan partikel udara berukuran 10 Mikrometer atau lebih kecil yang biasa ditemui pada debu dan asap.')
    
    with st.expander('Apa itu SO2?'):
        st.write('[Gas SO2](https://dspace.uii.ac.id/handle/123456789/30912) adalah partikel gas polutan akibat pembakaran bahan bakar fosil seperti minyak yang mampu mengganggu sistem pernapasan manusia.')
    
    with st.expander('Apa itu NO2?'):
        st.write('[NO2](https://pengen-tau.weebly.com/nitrogen-oksida.html) (Nitrogen Dioksida) merupakan gas polutan yang apabila memiliki kadara polusi yang tinggi, maka akan mengganggu paru - paru manusia.')
    
    with st.expander('Apa itu CO?'):
        st.write('[CO](https://www.alodokter.com/keracunan-karbon-monoksida) (Karbon Monoksida) adalah suatu gas yang timbul akibat asap hasil pembakaran bahan bakar kendaraan bermotor yang berlebihan.')
    
    with st.expander('Apa itu O3?'):
        st.write('[O3](https://dlhk.jogjaprov.go.id/perlindungan-lapisan-ozon) (Ozon) merupakan lapisan molekul gas yang berfungsi untuk menyerap radiasi sinar ultraviolet yang berada di atmosfer bumi.')
    
    with st.expander('Data Source'):
        st.write('Dataset yang dipakai untuk analisis dashboard ini diambil dari [Jakarta Open Data (2017 - 2021)](https://data.jakarta.go.id/organization/badan-pengelolaan-lingkungan-hidup-daerah?q=indeks+standar+pencemaran+udara&sort=1)')
