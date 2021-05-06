import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

Path=st.sidebar.file_uploader('Excel')
skip_rows,time,intensity=3,"Time","Intensity"

if Path is not None:
    Data=pd.ExcelFile(Path)
    Sheet_names=Data.sheet_names
    mode=st.sidebar.radio('MODE SELECT',("MONO","POLY"))
    ions=st.sidebar.multiselect("Ions",Sheet_names,Sheet_names)

    if mode=="MONO":
        num=st.sidebar.selectbox('SMA lines',[0,1,2,3],index=3)
        span1=st.sidebar.slider("SMA1 span",1,101,3,2)
        span2=st.sidebar.slider("SMA2 span",1,101,11,2)
        span3=st.sidebar.slider("SMA3 span",1,101,21,2)
        for Sheet_name in ions:
            df=pd.read_excel(Path,sheet_name=Sheet_name,skiprows=skip_rows)
            fig,ax=plt.subplots()
            plt.plot(df[time],df[intensity],label="raw")
            if num>=1:
                df["SMA1"]=df[intensity].rolling(window=span1,center=True).mean()
                plt.plot(df[time],df["SMA1"],label="span="+str(span1))
            if num>=2:            
                df["SMA2"]=df[intensity].rolling(window=span2,center=True).mean()
                plt.plot(df[time],df["SMA2"],label="span="+str(span2))
            if num>=3:            
                df["SMA3"]=df[intensity].rolling(window=span3,center=True).mean()
                plt.plot(df[time],df["SMA3"],label="span="+str(span3))
            plt.title(Sheet_name)
            plt.xlabel("Time(min)")
            plt.ylabel("Absolute Intensity")
            plt.legend()
            ax.ticklabel_format(useOffset=False,useMathText=True)
            st.pyplot(fig)
    
    if mode=="POLY":
        span=st.sidebar.slider("SMA span",1,51,1,2)
        fig,ax=plt.subplots()
        for Sheet_name in ions:
            df=pd.read_excel(Path,sheet_name=Sheet_name,skiprows=skip_rows)
            df["SMA"]=df[intensity].rolling(window=span,center=True).mean()
            plt.plot(df[time],df["SMA"],label=Sheet_name)
        if span==1:
            title="raw"
        else:
            title="span="+str(span)
        plt.title(title)
        plt.xlabel("Time(min)")
        plt.ylabel("Absolute Intensity")
        plt.legend()
        ax.ticklabel_format(useOffset=False,useMathText=True)
        st.pyplot(fig)