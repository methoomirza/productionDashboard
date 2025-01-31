import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui
import config as conf
from visualization import visualPlot


getColorCodes, hexColors, monthsName = conf.constVariables()

# ========== MAIN RECEIPE ===========================
st.set_page_config(page_title='Production Analysis')
# st.header('Production Analysis Year 2024')

pageTitle = ('<div style="font-family:sans-serif; color:Green; font-size: 42px; border:1px solid blue; border-radius:10px; padding:4px; display:flex; justify-content: center; align-items: center;">Production Analysis Year 2024</div><div style="margin-bottom:36px; color:#ccc; display:flex; justify-content: center; align-items: center;">By: Muhammad Shahid Mirza.</div>')
st.markdown(pageTitle, unsafe_allow_html=True)
# st.markdown(new_title, unsafe_allow_html=True)

data = conf.getLoadData("data/productionOrder-2024.xlsx")

data['colorCodes'] = data['color'].map(getColorCodes)
data['hexColor'] = data['colorCodes'].map(hexColors)
hexColorsList = data['hexColor'].unique().tolist()
# st.write(data['hexColor'].unique().tolist())
# st.write(data)

catList = data['category'].unique().tolist()
monts = data['month'].unique().tolist()
monthsNamelist = data['monthName'].unique().tolist()
yearsList = data['year'].unique().tolist()
leftCol, middleCol, rightCol = st.columns(3)
# singleCol = st.columns(1)

# =========== Top Summary Production - [ Metrics ]
dataSummary = data.groupby(['category', 'unit'], dropna=True, as_index=False)['actual'].sum()
topWerkSummary = data[data['type'] == 'ShotBlast'].groupby(['category', 'type', 'unit'], dropna=True, as_index=False)['actual'].sum()
#topwerkLabel = st.expander("TopWerk\n(Interlock-(M2) + Kerbstone-(Nos)")

# ============== FIRST ROW ==============
with leftCol:
    st.metric(
        label='Interlocks - (M2)',
        value = f"{dataSummary[dataSummary['category']=='Interlocks']['actual'].sum():,.0f}",
        delta = "REC/SQ/Uni Block",
        border=True
    )
with middleCol:
    st.metric(
        label='Kerbstone - (Nos)',
        # value=data[data['category'] == 'Kerbstone']['actual'].sum(),
        value = f"{dataSummary[dataSummary['category']=='Kerbstone']['actual'].sum():,.0f}",
        delta = "{Kerbstone / Tiles}",
        border=True
    )
with rightCol:
    st.metric(
        label= "TopWerk\n(Interlock/Kerbstone)",
        value = f"{topWerkSummary[topWerkSummary['category']=='Interlocks']['actual'].sum() + topWerkSummary[topWerkSummary['category']=='Kerbstone']['actual'].sum():,.0f}", 
        delta = f"{topWerkSummary[topWerkSummary['category']=='Interlocks']['actual'].sum()} / {topWerkSummary[topWerkSummary['category']=='Kerbstone']['actual'].sum()}", 
        # help='Interlock and Kerbstone',
        border=True
    )
# ============== SECOND ROW ==============
with leftCol:
    st.metric(
        label= "Cable Cover - (Nos)",
        value = f"{dataSummary[dataSummary['category']=='Cable Cover']['actual'].sum():,.0f}", 
        delta = "", 
        # help='Interlock and Kerbstone',
        border=True
    )
with middleCol:
    st.metric(
        label='Blocks - (M2)',
        value = f"{dataSummary[dataSummary['category']=='Blocks']['actual'].sum():,.0f}",
        delta = "",
        border=True
    )
with rightCol:
    st.metric(
        label='Heel Kerb - (Nos)',
        value = f"{dataSummary[dataSummary['category']=='Heel Kerb']['actual'].sum():,.0f}",
        delta = "",
        border=True
    )
# ============== THIRD ROW ==============
# with singleCol[0]:
#     st.metric(
#         label= "TopWerk\n(Interlock/Kerbstone)",
#         value = f"{topWerkSummary[topWerkSummary['category']=='Interlocks']['actual'].sum() + topWerkSummary[topWerkSummary['category']=='Kerbstone']['actual'].sum():,.0f}", 
#         delta = f"{topWerkSummary[topWerkSummary['category']=='Interlocks']['actual'].sum()} / {topWerkSummary[topWerkSummary['category']=='Kerbstone']['actual'].sum()}", 
#         # help='Interlock and Kerbstone',
#         border=True
#     )



dataRecord = data.groupby(['category', 'unit']).agg({'actual':'sum'}).sort_values(by='actual', ascending=False).reset_index()
visualPlot(df=dataRecord, 
           x='category', 
           y='actual', 
           title="Overview Production By Category", 
           xlabel='unit', 
           plotOpt='SBarPlot'
           )

getTabs = st.tabs(['Interlocks', 'Kerbstone']) # Configure for Tabs
with getTabs[0]:
    st.header(':red[Interlocks]')

    # Interlock Products By Colors
    xdata = data.copy()
    xdata['colors'] = xdata['colorCodes'] + ' - (' + xdata['color'] + ')'
    dataFiltered = (
        xdata.groupby(['colors', 'hexColor'], dropna=True,  as_index=False)['actual']
        .sum().sort_values(by='actual', ascending=False)
        )
    visualPlot(df=dataFiltered, 
           x='colors', 
           y='actual', 
           title="Overview Production By Colors", 
           xlabel='hexColor', 
           plotOpt='ColorBarPlot'
           )

    # Interlock Products By Thickness
    dataFiltered = (
        data.groupby(['thickness', 'unit'], dropna=True, as_index=False)['actual']
        .sum().sort_values(by='actual', ascending=False)
        )
    visualPlot(df=dataFiltered,
                x='thickness',
                y='actual',
                title='Overview Production By Thickness',
                xlabel='unit',
                plotOpt='SBarPlot'
                )
    
    # Interlock Products By MixType and Thickness
    dataFiltered = (
        data.groupby(['type', 'thickness', 'unit'], dropna=True, as_index=False)['actual']
        .sum().sort_values(by='actual', ascending=False)
        )
    visualPlot(df=dataFiltered,
                x='type',
                y='actual',
                hue='thickness',
                title='Overview Production By\nMixType and Thickness',
                xlabel='unit',
                plotOpt='histPlot'
    )

    # Interlock Products of TopWerks
    dataTopWerk = data[data['type'] == 'ShotBlast']
    dataTopWerk.loc[dataTopWerk['items'].str.contains('ShotBlast-Curl'), 'type'] = 'ShotBlast-Curl' # Extracting Type of Products as ShotBlast-Curl
    dataTopWerk.loc[dataTopWerk['items'].str.contains('ShotBlast-Curl-Coat'), 'type'] = 'ShotBlast-Curl-Coat' # Extracting Type of Products as ShotBlast-Curl-Coat
    # st.write(dataTopWerk)
    # st.write(dataTopWerk.shape)
    dataFiltered = (
        dataTopWerk.groupby(['category', 'type', 'unit'], dropna=True, as_index=False)['actual']
        .sum().sort_values(by='actual', ascending=False)
        )
    visualPlot(df=dataFiltered,
                x='type',
                y='actual',
                title='Overview Production By\nTopWerks',
                xlabel='unit',
                hue='category',
                plotOpt='histPlot'
                )
    
    # Top-10 Interlock Products
    dataFiltered = ( data[data['category'] == 'Interlocks']
        .groupby(['category', 'items', 'unit', 'hexColor'], dropna=True, as_index=False)['actual']
        .sum().sort_values(by='actual', ascending=False).head(10)
        )
    visualPlot(df=dataFiltered,
                x='items',
                y='actual',
                title='Top-10 Interlock Products',
                xlabel='hexColor', 
                plotOpt='ColorBarPlot'
                )
    # st.write(dataFiltered)


with getTabs[1]:
    st.header(':blue[Kerbstone]')

    dataKs = data[data['category'] == 'Kerbstone']
    # st.write(dataKs)
    
    # Kerbstone Products By Shape
    dataFiltered = (
        dataKs.groupby(['items', 'unit'], dropna=True, as_index=False)['actual']
        .sum().sort_values(by='actual', ascending=False).head(10)
        )
    visualPlot(df=dataFiltered,
                x='items',
                y='actual',
                title='Top-10 Kerbstone Products',
                xlabel='unit',
                plotOpt='SBarPlot'
                )
    
    # Kerbstone Products By Size/Length
    dataKs['size'] = dataKs['items'].str.split(' ').str[1]
    dataKs['length'] = dataKs['size'].str.split('x').str[0]
    # st.write(dataFiltered)
    dataFiltered = (
        dataKs.groupby(['length', 'unit'], dropna=True, as_index=False)['actual']
        .sum().sort_values(by='actual', ascending=False)
        )
    visualPlot(df=dataFiltered,
                x='length',
                y='actual',
                title='Overview Production By Length',
                xlabel='unit',
                plotOpt='SBarPlot'
                )
    
    # Kerbstone Products By Type
    dataFiltered = (
        dataKs.groupby(['type', 'unit'], dropna=True, as_index=False)['actual']
        .sum().sort_values(by='actual', ascending=False)
        )
    visualPlot(df=dataFiltered,
                x='type',
                y='actual',
                title='Overview Production By Type',
                xlabel='unit',
                plotOpt='SBarPlot'
                )
    # st.write(dataFiltered)

pageFooter = ('<div style="font-family:sans-serif; color:#ccc; font-size:14px; border-top:1px solid #ccc; padding:4px; margin-top:36px; display:flex; justify-content: center; align-items: center;">By: Muhammad Shahid Mirza</div>')
st.markdown(pageFooter, unsafe_allow_html=True)
