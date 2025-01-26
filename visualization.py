import streamlit as st
from PIL import Image # type: ignore

# Import Libraries for Visualization 
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import plotly.express as px # type: ignore
import matplotlib as mpl # type: ignore -- # For Y-axis formating


def visualPlot(df, x, y, title, hue='null', xlabel='null', plotOpt='SBarPlot'):
  if (plotOpt == 'SBarPlot'):
    # Graph Between Product Category and Actual Production
    sns.set_style('whitegrid')
    fig = plt.figure(figsize=(10, 8)) # Width, Height
    ax = sns.barplot(x=x, y=y, data=df, ci=None)
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # For Y-axis Formatting
    myUnit = df[xlabel].tolist()

    for i in ax.containers:
        ax.bar_label(i, labels=[f'{x:,.0f} {u}' for x, u in zip(i.datavalues, myUnit)], fontsize=12, padding=4)

    plt.xticks(rotation=90, fontsize=12)
    plt.xlabel(str(x.capitalize()), fontsize=14)
    plt.ylabel(str(y.capitalize()), fontsize=14)
    plt.title(title, fontsize=24)
    #st.pyplot(fig)


  elif (plotOpt == 'ColorBarPlot'):
    # Convert in the list of hex_codes for Visualization
    p_hexColor = df[xlabel].tolist() # It convert the data in the list of hex_codes

    fig, ax = plt.subplots(figsize=(15, 8))
    bar_container = ax.bar(df[x], df[y], align='center', color=p_hexColor, edgecolor='#ccc')
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # For Y-axis Formatting

    ax.grid(False) # It Will Remove Grid Only
    ax.set_title(title, fontsize=24)
    ax.set_ylabel(y.capitalize(), fontsize=14)
    ax.set_xlabel(x.capitalize(), fontsize=14)

    #ax.bar_label(bar_container, df_bycolors['actual'], fontsize=10, padding=4) # without comma Seperated
    for i in ax.containers: # with Comma Seperated
        ax.bar_label(i, labels=[f'{x:,.0f} M2' for x in i.datavalues], 
                     fontsize=10, padding=4, rotation=0)

    plt.xticks(rotation=90, fontsize=12) # Rotate Ticks and set FontSize
    #plt.axis('off') # It will Remove Grid, ticks, a-axis and y-axis
    #plt.grid(b=None) # It Will Remove Grid Only

  elif(plotOpt == 'histPlot'):

    sns.set_style('whitegrid')
    fig = plt.figure(figsize=(8, 8))
    ax = sns.histplot(x=x, weights=y, hue=hue,
                      data = df, multiple='stack', discrete=True)
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) # For Y-axis Formatting

    ax.grid(False) # It Will Remove Grid Only
    # Total of Stackes of Same Category
    y_offset = 1000 # Bottom Space of the Total Label of Stacke
    xlbl = df[x].unique().tolist()
    for itotal in xlbl:
        bar_height = round(df[df[x] == itotal][y].sum(), 0)
        total_label = "{:,} M2".format(round(bar_height))
        ax.text(itotal, bar_height+y_offset, total_label, ha='center', color='blue', fontsize=14)

    # Label of Each category Stacks
    for i in ax.containers: # with Comma Seperated
        ax.bar_label(i, labels=[f'{x:,.0f} M2' for x in i.datavalues], fontsize=12, padding=4, 
                    label_type='center', color='white')
        

    plt.setp(ax.get_legend().get_title(), fontsize='14') # for legend title
    plt.setp(ax.get_legend().get_texts(), fontsize='10') # for legend text

    plt.xticks(rotation=90, fontsize=12)
    plt.xlabel(x.capitalize(), fontsize=14)
    plt.ylabel(y.capitalize(), fontsize=14)
    plt.title(title, fontsize=24)

  st.pyplot(fig)


