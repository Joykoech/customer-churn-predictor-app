
import streamlit as st

# Set up Home page
st.set_page_config(
    page_title="CUSTOMER CHURN PREDICTION APPLICATION",
    page_icon='🏠',
    layout="wide"
)
st.markdown("<h1 style='color: skyblue;'>CUSTOMER CHURN PREDICTION APP</h1>", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.header("Insights",)
    st.write("Predict if a customer is about to churn based on known characteristics using Machine Learning.")
    
    st.header("Key Features",)
    st.write("""
    - **Data**: Access data from Vodafone Telecom.
    - **Dashboard**: Explore interactive data visualizations for insghts.
    - **Predict**: Instantly see predictions for customer attrition.
    - **History**: See past predictions made.

    """)
    
    st.header("Machine Learning Integration",)
    st.write("""
             - **Accurate Predictions**: Integrate advanced ML algorithms for accurate predictions.
             - **Data-Driven Decisions**: Leverage comprehensive customer data to inform strategic initiatives.
             - **Variety**: Choose between two advanced ML algorithms for predictions""")


with col2:
    st.header("User Benefits",)
    st.write("""
    - **Accurate Prediction**: Reduce churn rate.
    - **Data-Driven Decisions**: Inform strategic initiatives.
    - **Enhanced Insights**: Understand customer behavior.
    """)
    
    with st.expander("Need Help?", expanded=False):
        st.write("""
    
        - **Support**: Contact us at joykoech2000@gmail.com
        """)

    st.subheader("About Developer")
    st.write("""
    I am a Data Analyst who transforms complex data into actionable insights to enhance decision-making and drive business success.
    """)

  