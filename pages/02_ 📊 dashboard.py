import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Set page configuration
st.set_page_config(
    page_title="Dashboard Page",
    page_icon="📊",
    layout="wide"
)

# Load data with caching to improve performance
@st.cache_data
def load_data():
    df = pd.read_csv(r"Data\train_data.csv")
    return df

# Load the dataset
df = load_data()

def eda_dashboard(df):
    st.markdown("### 🔍 Exploratory Data Analysis Dashboard")
    
    with st.expander("📊 Univariate Analysis", expanded=True):
        fig = px.histogram(df, x='tenure', nbins=30, color='churn',
                           title="Distribution of Tenure with Churn",
                           color_discrete_sequence=['lightsalmon', 'lightblue'])
        st.plotly_chart(fig)
        
        fig = px.histogram(df, x='monthlycharges', nbins=30, color='churn',
                           title="Distribution of Monthly Charges with Churn",
                           color_discrete_sequence=['lightsalmon', 'lightblue'])
        st.plotly_chart(fig)

    with st.expander("📈 Categorical Distributions"):
        pie = px.pie(df, names='churn', title="Churn Rate",
                     color_discrete_sequence=['lightsalmon', 'lightskyblue'])
        st.plotly_chart(pie)

        bar = px.pie(df, names="internetservice", title="Internet Service Providers",
                     color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(bar)
        
        pie = px.pie(df, names='contract', title="Contract Distribution",
                     color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(pie)

    with st.expander("📊 Distribution Analysis"):
        violin = px.violin(df, x='contract', y='monthlycharges',
                           title="Monthly Charges Distribution by Contract",
                           color_discrete_sequence=['lightsalmon', 'lightskyblue'])
        st.plotly_chart(violin)
        
        violin = px.violin(df, x='paymentmethod', y='monthlycharges',
                           title='Monthly Charges Distribution by Payment Method',
                           color_discrete_sequence=['lightsalmon', 'lightskyblue'])
        st.plotly_chart(violin)
        
        box = px.box(df, x='internetservice', y='monthlycharges',
                     title='Monthly Charges Distribution by Internet Service',
                     color_discrete_sequence=['lightsalmon', 'lightskyblue'])
        st.plotly_chart(box)
    
    with st.expander("📉 Correlation Analysis"):
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_columns) > 1:
            correlation_matrix = df[numeric_columns].corr()
            fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='peach',
                            title="Correlation Matrix", width=500, height=500)
            st.plotly_chart(fig)

def kpi_dashboard(df):
    st.markdown("### 📊 Key Performance Indicators")

    # Calculate key metrics
    avg_tenure = df['tenure'].mean()
    avg_monthly_charges = df['monthlycharges'].mean()
    churn_rate = df['churn'].value_counts(normalize=True).get('Yes', 0) * 100

    # Display key metrics with KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("📅 Average Tenure", f"{round(avg_tenure, 2)} months")
    col2.metric("💵 Average Monthly Charges", f"${round(avg_monthly_charges, 2)}")
    col3.metric("📉 Churn Rate", f"{round(churn_rate, 2)}%")

    # Visualization Section
    st.markdown("#### 📊 Visual Insights")

    col1, col2 = st.columns(2)
    
    with col1:
        churn_gender_counts = df.groupby(['gender', 'churn']).size().reset_index(name='count')
        fig = px.bar(churn_gender_counts, x='gender', y='count', color='churn', barmode='group',
                     color_discrete_map={'No': 'mediumseagreen', 'Yes': 'mediumvioletred'})
        fig.update_layout(title='Churn Distribution by Gender')
        st.plotly_chart(fig)

        partner_churn_counts = df.groupby(['partner', 'churn']).size().reset_index(name='totalcount')
        pie = px.pie(partner_churn_counts, names='churn', values='totalcount', color='churn',
                     title="Impact of Partner Relationship on Churn",
                     color_discrete_map={'No': 'mediumseagreen', 'Yes': 'mediumvioletred'})
        st.plotly_chart(pie)
    
    with col2:
        charges_vs_churn = px.box(df, x='churn', y='monthlycharges', color='churn',
                                  title='Impact of Monthly Charges on Churn',
                                  color_discrete_sequence=['mediumseagreen', 'mediumvioletred'])
        st.plotly_chart(charges_vs_churn)

        internet_vs_churn = px.bar(df, x='internetservice', y='churn', color='churn',
                                   title="Impact of Internet Service on Churn",
                                   color_discrete_sequence=['mediumseagreen', 'mediumvioletred'])
        st.plotly_chart(internet_vs_churn)

        payment_vs_churn = px.bar(df, x='paymentmethod', y='churn', color='churn',
                                  title='Influence of Payment Methods on Churn',
                                  color_discrete_sequence=['mediumseagreen', 'mediumvioletred'])
        st.plotly_chart(payment_vs_churn)

if __name__ == "__main__":
    st.title("📊 Dashboard")

    # Tabs for better navigation between EDA and KPIs
    tab1, tab2 = st.tabs(["Exploratory Data Analysis", "Key Performance Indicators"])
    
    with tab1:
        eda_dashboard(df)
    
    with tab2:
        kpi_dashboard(df)
