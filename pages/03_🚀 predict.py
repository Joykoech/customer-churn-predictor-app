import streamlit as st
import joblib
import pandas as pd
import datetime
import os
import xgboost
from sklearn.ensemble import RandomForestClassifier


# Set page config
st.set_page_config(page_title="Customer Churn Prediction", page_icon="🚀", layout="wide")

# Cache the model loading
@st.cache_resource(show_spinner="Loading Random Forest Model...")
def load_random_model():
    model = joblib.load(r'models/random.joblib')
    return model

@st.cache_resource(show_spinner="Loading XGBoost Model...")
def load_xgb():
    model = joblib.load(r'models/xgb.joblib')
    return model

# Function to select model
def select_model():
    col1, _ = st.columns(2)
    with col1:
        model_choice = st.selectbox("Select Model", options=["RandomForest", "Xgboost"], key="selected_model")

    if st.session_state["selected_model"] == "RandomForest":
        model = load_random_model()
    else:
        model = load_xgb()
        
    encoder = joblib.load(r'models/encoder.joblib')
    
    return model, encoder

# Initialize session state
if 'prediction' not in st.session_state:
    st.session_state["prediction"] = None
    
if "probability" not in st.session_state:
    st.session_state["probability"] = None

# Function to make predictions and save to history
def make_predictions(model, encoder):
    user_input = {
        "gender": st.session_state["gender"],
        "seniorcitizen": st.session_state["seniorcitizen"],
        "partner": st.session_state["partner"],
        "dependents": st.session_state["dependents"],
        "phoneservice": st.session_state["phoneservice"],
        "multiplelines": st.session_state["multiplelines"],
        "internetservice": st.session_state["internetservice"],
        "onlinesecurity": st.session_state["onlinesecurity"],
        "onlinebackup": st.session_state["onlinebackup"],
        "tenure": st.session_state["tenure"],
        "deviceprotection": st.session_state["deviceprotection"],
        "techsupport": st.session_state["techsupport"],
        "streamingtv": st.session_state["streamingtv"],
        "streamingmovies": st.session_state["streamingmovies"],
        "contract": st.session_state["contract"],
        "paperlessbilling": st.session_state["paperlessbilling"],
        "paymentmethod": st.session_state["paymentmethod"],
        "monthlycharges": st.session_state["monthlycharges"],
        "totalcharges": st.session_state["totalcharges"]
    }

    df = pd.DataFrame([user_input])
    df["Prediction_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["model_used"] = st.session_state["selected_model"]

    # Make predictions
    try:
        pred = model.predict(df)
        pred = int(pred[0])
        prediction = encoder.inverse_transform([pred])[0]
        
        # Show probability
        probability = model.predict_proba(df)
        
        # Update session state
        st.session_state["prediction"] = prediction
        st.session_state["probability"] = probability
        
        # Save prediction to history
        save_to_history(df, prediction, probability)
        
    except Exception as e:
        st.error(f"Error making predictions: {e}")
        return None, None

    return prediction, probability

# Function to save prediction results to history file
def save_to_history(df, prediction, probability):
    df["prediction"] = prediction
    df["probability"] = probability[0][1] if prediction == "Yes" else probability[0][0]
    
    csv_path = os.path.join("Datafiles", "history.csv")
    if not os.path.exists("Datafiles"):
        os.makedirs("Datafiles")
    
    # Save the dataframe to CSV, append mode with no header if file exists
    df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)

# Function to display the form and handle user inputs
def display_form():
    model, encoder = select_model()

    if model and encoder:
        with st.form("input-features"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("#### **PERSONAL INFORMATION 🙍🏽**")
                st.radio("Select gender:", ("Male", "Female"), key="gender")
                st.radio("Are you a senior citizen: (1- yes, 0- no)", (1, 0), key="seniorcitizen")
                st.radio("Do you have a partner?", options=["Yes", "No"], key="partner")
                st.radio("Do you have dependents?", ("Yes", "No"), key="dependents")
                st.radio("Do you have phone service?", ("Yes", "No"), key="phoneservice")
                st.number_input("How many months has the customer stayed?", key="tenure", min_value=1, max_value=72, step=1)
            
            with col2:
                st.write("#### **SERVICE USAGE 📲**")
                st.radio("Do you have multiple lines?", options=["Yes", "No", "No phone service"], key="multiplelines")
                st.radio("Which internet service provider do you have?", options=["DSL", "Fiber optic", "No"], key="internetservice")
                st.radio("Do you have online security?", options=["Yes", "No", "No internet service"], key="onlinesecurity")
                st.radio("Do you have online backup?", options=["Yes", "No", "No internet service"], key="onlinebackup")
                st.radio("Do you have device protection?", options=["Yes", "No", "No internet service"], key="deviceprotection")
                st.radio("Do you have tech support?", options=["Yes", "No", "No internet service"], key="techsupport")

            with col3:
                st.write("#### **STREAMING SERVICES 📺**")
                st.radio("Do you have streaming TV?", options=["Yes", "No", "No internet service"], key="streamingtv")
                st.radio("Do you have streaming movies?", options=["Yes", "No", "No internet service"], key="streamingmovies")
                st.write("#### **CONTRACT TYPE**")
                st.radio("Which contract do you have?", options=["Month-to-month", "One year", "Two year"], key="contract")
                st.radio("Do you use paperless billing?", options=["Yes", "No"], key="paperlessbilling")
                st.radio("Select payment method:", options=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], key="paymentmethod")
                st.write("#### **BILLING INFORMATION**")
                st.number_input("Enter your monthly charges:", key="monthlycharges", min_value=0, step=1)
                st.number_input("Enter your total charges:", key="totalcharges", min_value=0, step=1)

            st.form_submit_button("Predict", on_click=make_predictions, kwargs=dict(model=model, encoder=encoder))


# Main block to run the app
if __name__ == "__main__":
    st.title("Customer Churn Prediction")
    display_form()

    prediction = st.session_state["prediction"]
    probability = st.session_state["probability"]
    
    if prediction is not None and probability is not None:
        st.divider()
        if prediction == "Yes":
            probability_of_yes = probability[0][1] * 100
            st.markdown(f"The customer is likely to leave with a probability of **{round(probability_of_yes, 2)}%**.")
        else:
            probability_of_no = probability[0][0] * 100
            st.markdown(f"The customer is likely to stay with a probability of **{round(probability_of_no, 2)}%**.")
    else:
        st.write("Please fill the form and click 'Predict' to see the prediction.")
