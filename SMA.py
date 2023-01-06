import pandas as pd
import scipy as sp
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

Path=st.file_uploader('Excel')
skip_rows,time,intensity=3,"Time","Intensity"

if Path is not None:
    Data=pd.ExcelFile(Path)
    Sheet_names=Data.sheet_names
    ions=st.multiselect("Ions",Sheet_names,Sheet_names)

    span=st.slider("SMA span",1,121,1,2)
    standardization=st.checkbox('Standardization',value=False)
    fig,ax=plt.subplots()

    for Sheet_name in ions:
        df=pd.read_excel(Path,sheet_name=Sheet_name,skiprows=skip_rows)
        df["SMA"]=df[intensity].rolling(window=span,center=True).mean()
        if standardization==False:
            plt.plot(df[time]*60,df["SMA"],label=Sheet_name)
            plt.ylabel("Absolute Intensity")
        else:
            mu=sp.mean(df["SMA"])
            sigma=sp.std(df["SMA"],ddof=1)
            df["STD"]=(df["SMA"])/sigma
            plt.plot(df[time]*60,df["STD"],label=Sheet_name)
            plt.ylabel("Standardized Intensity")
    
    plt.xlabel("Time(s)")
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.ticklabel_format(useOffset=False,useMathText=True)
    st.pyplot(fig)
