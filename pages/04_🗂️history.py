import streamlit as st 
import pandas as pd
import os

st.set_page_config(page_title="History_page", page_icon="🗂️", layout="wide")

def display_history():
    csv_path = "Datafiles/history.csv"
    csv_exists = os.path.exists(csv_path)
    
    if csv_exists:
        history = pd.read_csv(csv_path)
        st.dataframe(history)
        
        
if __name__ == "__main__":
    st.title("History page")
    display_history()