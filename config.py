import pandas as pd
import numpy as py
import streamlit as st

def constVariables():
  color_codes = {
                  'Grey' : 'GY10', 'Dark Grey' : 'GY12', 
                  'Silver Grey' : 'GY11', 'Black' : 'BK10', 
                  'Charcoal Black' : 'BK11', 'White' : 'WT10', 
                  'Silver White' : 'WT11', 'Red' : 'RD10', 
                  'Green' : 'GN10', 'Brown' : 'BN10', 'Tan' : 'TN10', 
                  'Yellow' : 'YW10', 'Light Yellow' : 'YW11',
                  'Beige' : 'BG10', 'M.CLR(Beige-Black)' : 'M.CLR(BG10-BK10)' 
                }
  hex_colors = {
      'GY10' : '#808080',   # Grey
      'GY11' : '#8E969D',   # Silver Grey
      'GY12' : '#63666A',   # Dark Grey
      'BK10' : '#000000',   # Black
      'BK11' : '#36454F',   # Charcoal Black
      'WT10' : '#ffffff',   # White
      'WT11' : '#C0C0C0',   # Silver White
      'RD10' : '#FF0000',   # Red
      'GN10' : '#008000',   # Green
      'BN10' : '#A52A2A',   # Brown
      'TN10' : '#d2b48c',   # Tan
      'BG10' : '#F5F5DC',   # Beige
      'YW10' : '#FFFF00',   # Yellow
      'YW11' : '#FFFFE0'    # Light Yellow
  }
  monthsName = {
  '01' : 'January',
  '02' : 'February',
  '03' : 'March',
  '04' : 'April',
  '05' : 'May',
  '06' : 'June',
  '07' : 'July',
  '08' : 'August',
  '09' : 'September',
  '10' : 'October',
  '11' : 'November',
  '12' : 'December'
  }

  return color_codes, hex_colors, monthsName


@st.cache_data # with this rum only once
def getLoadData(fileLocation):
  dfload = pd.ExcelFile(fileLocation, None) # Excel file for Report
  df = dfload.parse(dfload.sheet_names[0])
  # -------- SELECTING FEATURED COLUMNS AND RENAME FOR EASY ACCESS -------
  xdf = df[~df['Production orders'].isna()][['Item description', 'Actual', 'Unit', 'Start date']].rename(
      columns={
          'Item description':'items', 
          'Actual':'actual', 
          'Unit':'unit', 
          'Start date':'date'
      })
  data = getNewFeatures(xdf) # CALL FUNCTION FOR EXTRACTING NEW FEATURES FROM ITEMS_NAME COLUMNS
  return data



#catNames = ['Inrerlocks', 'Kerbstone', 'Heel Kerb', 'Block', 'Cable Cover', 'Tiles']
def getNewFeatures(df):

  # -------- EXTRACTING NEW FEATURES FROM DATE [MONTH AND YEAR].
  df = df.assign(
      month = lambda xdf: xdf['date'].str.split('/').str[1],
      year = lambda xdf: xdf['date'].str.split('/').str[2],
  )
  [_, _, monthList] = constVariables()
  df['monthName'] = df['month'].map(monthList)
  
  # # -------- EXTRACTING NEW FEATURES FROM DATE [MONTH AND YEAR].
  # df = df.assign(
  #   month = lambda xdf: pd.to_datetime(pd.to_datetime(xdf['date']).dt.strftime('%d/%m/%Y')).dt.month,
  #   monthName = lambda xdf: pd.to_datetime(pd.to_datetime(xdf['date']).dt.strftime('%d/%m/%Y')).dt.month_name(),
  #   year = lambda xdf: pd.to_datetime(pd.to_datetime(xdf['date']).dt.strftime('%d/%m/%Y')).dt.year,
  # )


  # Identify the Main Category of the Products i.e ['Interlock', 'Kerbstone', 'Heel Kerb', 'Block', 'Cable Cover']
  df.loc[~(df['items'].str.contains('Kerbstone')) &
                      ~(df['items'].str.contains('Heel Kerb')) &
                      #~(df['items'].str.contains('Block')) &
                      ~(df['items'].str.contains('Cable Cover')), 'category'] = 'Interlocks'

  df.loc[df['items'].str.contains('Kerbstone'), 'category'] = 'Kerbstone'
  df.loc[df['items'].str.contains('Heel Kerb'), 'category'] = 'Heel Kerb'
  df.loc[df['items'].str.contains('Cable Cover'), 'category'] = 'Cable Cover'


  # ------- Following 3-lines of Code for Blocks ----------------------------------------
  df.loc[(df['items'].str.contains('Hollow')) | (df['items'].str.contains('Solid')) | 
         (df['items'].str.contains('Insulate')) | (df['items'].str.contains('Block')), 'category'] = 'Blocks'

  # ------- Following 3-lines of Code for Tiles -----------------------------------------
  df.loc[(df['items'].str.contains('tile')) | 
                      (df['items'].str.contains('Tile')), 'category'] = 'Tiles'
  
  # ------- Extracting Color of the Products --------------------------------------------
  df['color'] = df.loc[(df['category'] != 'Kerbstone') & (df['category'] != 'Cable Cover') & 
                        (df['category'] != 'Tiles') & (df['category'] != 'Heel Kerb') ]['items'].str.split('/').str[2]
  df.loc[df['items'].str.contains('Tac'), 'color'] = df.loc[df['items'].str.contains('Tac')]['items'].str.split(' ').str[2]
  df.loc[df['items'].str.contains('Roof'), 'color'] = df.loc[df['items'].str.contains('Roof')]['items'].str.split(' ').str[4]
  df.loc[df['items'].str.contains('Heel'), 'color'] = df.loc[df['items'].str.contains('Heel')]['items'].str.split(' ').str[3]

  # ------- Extracting Type of Products --------------------------------------------
  df.loc[(df['items'].str.contains('Single')), 'type'] = 'Single Mix' # Extracting type as Single Mix
  df.loc[(df['category'] == 'Interlocks') & (df['type'].isna()), 'type'] = 'Double Mix' # if not Single Mix the it should be Double Mix
  df.loc[(df['category'] == 'Blocks') & (df['type'].isna()), 'type'] = 'Double Mix' # if not Single Mix the it should be Double Mix
  df['items'].replace('B/N', 'BN', inplace=True, regex=True) # Replacing B/N to BN
  df['items'].replace('-LM', '', inplace=True, regex=True) # Replacing -LM to LM
  df.loc[(df['category'] == 'Kerbstone') & (df['type'].isna()), 'type'] = df.loc[(df['category'] == 'Kerbstone')]['items'].str.split(' ').str[2]
  df.loc[df['items'].str.contains('10 Gutter'),'type'] = '10 Gutter' # Replacing the 10 to 10Gutter for Identification
  df.loc[df['unit'].str.contains('LM'),'unit'] = 'Nos' # Verify the unit
  df['type'] = df['type'].str.replace('Flush-LM', 'Flush') # Replacing LM to Flush
  df['thickness'] = df['items'].str.split('/').str[1] # Extracting Thickness of Products
  df.loc[df['items'].str.contains('ShotBlast'), 'type'] = 'ShotBlast' # Extracting Type of Products as ShotBlast
  # df.loc[df['items'].str.contains('ShotBlast-Curl'), 'type'] = 'ShotBlast-Curl' # Extracting Type of Products as ShotBlast-Curl
  # df.loc[df['items'].str.contains('ShotBlast-Curl-Coat'), 'type'] = 'ShotBlast-Curl-Coat' # Extracting Type of Products as ShotBlast-Curl-Coat

  return(df)





