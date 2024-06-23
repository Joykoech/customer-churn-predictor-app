import pandas as pd
import plotly.express as px
import streamlit as st

        

# Function to load data
def load_data():
    df = pd.read_csv(r"Data/train_data.csv")
    return df

# Function for EDA dashboard
def eda_dashboard(df):
    st.markdown("### EXPLORATORY DATA ANALYSIS (EDA)")

    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

    # Display histograms
    if 'tenure' in numeric_columns and 'MonthlyCharges' in numeric_columns:
        chart1, chart2 = st.columns(2)
        with chart1:
            st.markdown("**Histogram of Tenure**")
            fig1 = px.histogram(df, x='tenure', title='Histogram of Tenure')
            st.plotly_chart(fig1)

        with chart2:
            st.markdown("**Histogram of Monthly Charges**")
            fig2 = px.histogram(df, x='MonthlyCharges', title='Histogram of Monthly Charges')
            st.plotly_chart(fig2)

    # Display correlation matrix if numeric columns are available
    if len(numeric_columns) > 1:
        st.markdown("**Heatmap of Feature Correlations**")
        correlation_matrix = df[numeric_columns].corr()
        fig = px.imshow(correlation_matrix, text_auto=True, title="Correlation Heatmap")
        st.plotly_chart(fig)
    else:
        st.warning("No numeric columns available for correlation analysis.")

# Function for KPI dashboard
def kpi_dashboard(df):
    st.markdown("### KEY PERFORMANCE INDICATORS (KPIs)")
    
    st.markdown("#### KEY METRICS")

    # KPIs Section
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    # Compute key metrics from the DataFrame
    avg_tenure = df['tenure'].mean()
    avg_monthly_charges = df['MonthlyCharges'].mean()
    churn_rate = df['Churn'].value_counts(normalize=True).get('Yes', 0) * 100
    contract_count = df['Contract'].value_counts()

    # Display KPIs
    kpi1.metric("Average Tenure", f"{avg_tenure:.2f} months", delta=-24)  
    kpi2.metric("Average Monthly Charges", f"${avg_monthly_charges:.2f}", delta=+18.0)  
    kpi4.metric("Total Customers", len(df), delta=len(df) - 1000)  

    st.markdown("#### VISUALIZATIONS")
    
    # Create a bar chart for gender distribution with churn
    st.markdown("**Gender Distribution by Monthly Charges and Churn**")
    chart1 = px.bar(df, x="gender", y="MonthlyCharges", color="Churn",
                    title="Monthly Charges by Gender and Churn",
                    barmode='group')
    st.plotly_chart(chart1)

    # Create a pie chart for Contract distribution
    st.markdown("**Customer Distribution by Contract Type**")
    chart2 = px.pie(df, names='Contract', title="Distribution of Customers by Contract Type")
    st.plotly_chart(chart2)

    # Create a bar chart for Payment Method distribution
    st.markdown("**Payment Method Distribution**")
    chart3 = px.bar(df, x='PaymentMethod', title="Payment Method Usage",
                    color='PaymentMethod', height=400)
    st.plotly_chart(chart3)



# Main section
def main():
    st.set_page_config(
        page_title="Churn Predictor Dashboard",
        page_icon="📊",
        layout="wide"
    )

    # Initialize session state
    if 'selected_dashboard_type' not in st.session_state:
        st.session_state.selected_dashboard_type = "EDA"  # Default value

    df = load_data()

    # Sidebar
    st.sidebar.title("Navigation")
    dashboard_type = st.sidebar.radio("Choose Dashboard", ("EDA", "KPIs"), key='selected_dashboard_type')

    # Render selected dashboard
    if dashboard_type == "EDA":
        eda_dashboard(df)
    elif dashboard_type == "KPIs":
        kpi_dashboard(df)

if __name__ == "__main__":
    main()
