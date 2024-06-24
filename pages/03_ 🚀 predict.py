import streamlit as st 
import  streamlit as st
import joblib
import pandas as pd
import numpy as np 
import datetime
import os
import xgboost
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Predict_page", page_icon="🚀", layout="wide")

@st.cache_resource( show_spinner="Model loading...")
def load_random_model():
    model= joblib.load(r'models\random.joblib')
    return model


@st.cache_resource(show_spinner="Model loading...")
def load_xgb():
    model=joblib.load(r'models\xgb.joblib')
    return model


## Create a select model box function
# @st.cache_resource(show_spinner="Model_loading...")
def select_model():
    col1,col2 = st.columns(2)
    with col1:
        st.selectbox("Select Model", options=["RandomForest", "Xgboost"], key="selected_model")
        
    with col2:
        pass
    
    if st.session_state["selected_model"] == "RandomForest":
        model=load_random_model()
    else:
        model=load_xgb()
        
    encoder=joblib.load(r'models\encoder.joblib')
     
    return model,encoder

## Intialize session state
if 'prediction' not in st.session_state:
    st.session_state["prediction"] = None
    
if "probability" not in st.session_state:
    st.session_state["probability"] = None

def make_predictions(model,encoder):
    
    gender= st.session_state["gender"]
    seniorcitizen= st.session_state["seniorcitizen"]
    partner= st.session_state["partner"]
    dependents= st.session_state["Dependents"]
    phoneservice= st.session_state["phoneservice"]
    multiplelines= st.session_state["multiplelines"]
    internetservice= st.session_state["internetservice"]
    onlinesecurity= st.session_state["onlinesecurity"]
    onlinebackup= st.session_state["onlinebackup"]
    tenure= st.session_state["tenure"]
    deviceprotection= st.session_state["deviceprotection"]
    techsupport= st.session_state["techsupport"]
    streamingtv= st.session_state["streamingtv"]
    streamingmovies= st.session_state["streamingmovies"]
    contract= st.session_state["contract"]
    paperlessbilling= st.session_state["paperlessbilling"]
    paymentmethod= st.session_state["paymentmethod"]
    monthlycharges= st.session_state["monthlycharges"]
    totalcharges= st.session_state["totalcharges"]
    
    ## Create a dataframe
    data= [[gender, seniorcitizen, partner, 
            dependents, phoneservice, multiplelines, 
            internetservice, onlinesecurity, onlinebackup,tenure, 
            deviceprotection, techsupport, streamingtv, 
            streamingmovies, contract, paperlessbilling, paymentmethod,monthlycharges, totalcharges]]
    columns= ['gender', 'seniorcitizen', 'partner', 
            'dependents', 'phoneservice', 'multiplelines', 
            'internetservice', 'onlinesecurity', 'onlinebackup','tenure', 
            'deviceprotection', 'techsupport', 'streamingtv', 
            'streamingmovies', 'contract', 'paperlessbilling', 'paymentmethod','monthlycharges' ,'totalcharges']
    
    df= pd.DataFrame(data, columns=columns)
    
    df["Prediction_time"]= datetime.date.today()
    df["model_used"]= st.session_state["selected_model"]
    
    # df.to_csv("./Datafiles/history.csv", mode="a", header=not os.path.exists("./Datafiles/history.csv"), index=False)
    
    ## make predictions
    pred = model.predict(df)
    pred= int(pred[0])
    prediction = encoder.inverse_transform([pred])
    
    ## show probability 
    probability=model.predict_proba(df)
    
    ## Update session state
    st.session_state["prediction"]=prediction
    st.session_state["probability"]=probability
    
    return prediction,probability
    
       
def display_form():
    
    model,encoder = select_model()
    
    with st.form("input-features"):
        
        col1,col2,col3 = st.columns(3)
        
        with col1:
            st.write("#### **PERSONAL INFORMATION 🙍🏽**")
            st.radio("Select gender:",("Male", "Female"), key="gender")
            st.radio("Are you a senior citizen: (1- yes, 0- no)",(1,0),key="seniorcitizen")
            st.radio("Do you have a partner", options=["Yes", "No",], key="partner")
            st.radio("Do you have a dependent",("Yes", "No"), key="Dependents")
            st.radio("Do you have a phone service?", ("Yes", "No"),key="phoneservice")
            st.number_input("How many months has the customer stayed?", key="tenure", min_value=1, max_value=72, step=1)
                
        with col2:
            st.write("#### **SERVICE USAGE 📲**")
            st.radio("Do you have multiplelines?", options=["Yes", "No", "No phone service"], key="multiplelines")
            st.radio("Which internet service provider do you have?", options=["DSL", "Fiber optic", "No"], key="internetservice")
            st.radio("Do you have online security", options=["Yes", "No", "No internet service"], key="onlinesecurity")
            st.radio("Do you have an online backup?", options=["Yes", "No", "No internet service"], key="onlinebackup")
            st.radio("Do you have device protection?", options=["Yes", "No", "No internet service"], key="deviceprotection")
            st.radio("Do you have tech support?", options=["Yes", "No", "No internet service"], key="techsupport")
        
        with col3:
            st.write("#### **STREAMING SERVICES   📺**")
            st.radio("Do you have streaming tv?", options=["Yes", "No", "No internet service"], key="streamingtv")
            st.radio("Do you have streaming movies?", options=["Yes", "No", "No internet service"], key="streamingmovies")
            st.write("#### **CONTRACT TYPE**")
            st.radio("Which contract do you have?", options=["Month-to-month", "One year", "Two year"], key="contract")
            st.radio("Do you have paperless billing?", options=["Yes", "No"], key="paperlessbilling")
            st.radio("Do you have payment method?", options=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], key="paymentmethod")
            st.write("#### **BILLING INFORMATION**")
            st.number_input("Enter your monthly charges?", key="monthlycharges", min_value=1, step=1)
            st.number_input("Enter your total charges?", key="totalcharges", min_value=1, step=1)
            
        st.form_submit_button("Predict", on_click=make_predictions, kwargs=dict(model=model, encoder=encoder))            


if __name__ == "__main__":
    st.title("Predictions")
    display_form()
    
    prediction=st.session_state["prediction"]
    probability=st.session_state["probability"]
    
    if not prediction:
        st.write("Show predictions")
        st.divider()
    elif prediction =="Yes":
        probability_of_yes=probability[0][1]*100
        st.markdown(f"The customer is likely to leave with a probability of {round(probability_of_yes,2)}%")
    else:
        probability_of_no=probability[0][0]*100
        st.markdown(f"The customer is likely to stay with a probability of {round(probability_of_no,2)}%")
