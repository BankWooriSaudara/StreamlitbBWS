import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from matplotlib import pyplot as plt

st.set_page_config(page_title='BWS')

st.title('Risk Management')

plt.style.use("ggplot")

@st.cache
def get_data(filename):
    getData = pd.read_csv(filename)

    return getData

data = {
    "num": [x for x in range(1, 11)],
    "square": [x**2 for x in range(1, 11)],
    "twice": [x*2 for x in range(1, 11)],
    "thrice": [x*3 for x in range(1, 11)]
}

rad = st.sidebar.radio("Navigation", ["Data1", "Data2", "Data3", "Graph"])

if rad == "Graph":

    st.header('Function Graph')

    df = pd.DataFrame(data=data)

    col = st.sidebar.multiselect("Select a Column ", df.columns)

    plt.plot(df['num'], df[col])

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


if rad == "Data2":
    excel_file = 'data/data.csv'

    st.header('Branch Sales Rating')
    st.text('Filter data by branch.')

    df = get_data(excel_file)

    kota = df['Kota'].unique().tolist()
    sales = df['Sales'].unique().tolist()

    sales_selection = st.slider('sales:',
                                min_value=min(sales),
                                max_value=max(sales),
                                value=(min(sales), max(sales)),
                                # step=30
                                )

    kota_selection = st.multiselect('Kota:',
                                    kota,
                                    default=kota)

    mask = (df['Sales'].between(*sales_selection)
            ) & (df['Kota'].isin(kota_selection))
    number_of_result = df[mask].shape[0]
    st.markdown(f'*Available Result: {number_of_result}*')

    df_grouped = df[mask].groupby(by=['Rating']).count()[['Sales']]
    df_grouped = df_grouped.rename(columns={'Sales': 'Votes'})
    df_grouped = df_grouped.reset_index()

    st.dataframe(df[mask])

    bar_chart = px.bar(df_grouped,
                       x='Rating',
                       y='Votes',
                       text='Votes',
                       color_discrete_sequence=['#F63366']*len(df_grouped),
                       template='plotly_white')
    st.plotly_chart(bar_chart)


if rad == "Data1":
    excel_file2 = 'data/data2.csv'

    st.header('Branch Data')

    df_participants = get_data(excel_file2)
    df_participants.dropna(inplace=True)

    col1, col2 = st.columns(2)
    image = Image.open('images/bws.png')
    col1.image(image,
               caption='Bank Woori Saudara',
               #  use_column_width=True)
               width=300)
    col2.dataframe(df_participants.head())

    pie_chart = px.pie(df_participants,
                       title='Total No. of Branch',
                       values='Total',
                       names='Nama')
    st.plotly_chart(pie_chart)


if rad == "Data3":
    excel_file3 = 'data/green_tripdata.csv'
    st.header('NYC Taxi Dataset')
    st.text('I found this dataset from www1.nyc.gov.')

    taxi_data = get_data(excel_file3)
    st.write(taxi_data.head())

    st.subheader('Pick-up location ID distribution on the NYC dataset')
    pulocation_dist = pd.DataFrame(
        taxi_data['PULocationID'].value_counts()).head(50)
    st.bar_chart(pulocation_dist)