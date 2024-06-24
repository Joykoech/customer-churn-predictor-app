import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="History Page",
    page_icon="🗂️",
    layout="wide"
)

# Function to display history
def display_history():
    csv_path = os.path.join("Data", "history.csv")
    
    # Check if the CSV file exists
    if os.path.exists(csv_path):
        try:
            # Read the CSV file
            history = pd.read_csv(csv_path)
            
            # Check if the file is empty
            if history.empty:
                st.info("No history data available.")
            else:
                # Display the history in a table
                st.write("### 📜 Prediction History")
                st.dataframe(history, use_container_width=True)
                
                # Provide option to download the history as a CSV file
                csv = history.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download History as CSV", 
                    data=csv, 
                    file_name="prediction_history.csv", 
                    mime='text/csv'
                )
                
                # Provide option to clear the history
                if st.button("🗑️ Clear History"):
                    os.remove(csv_path)
                    st.success("History cleared.")
                    st.experimental_rerun()  # Refresh the page to update the display

        except Exception as e:
            st.error(f"Error reading history file: {e}")
    else:
        st.info("No history file found. Predictions will appear here once they are made.")

# Main function to run the app
if __name__ == "__main__":
    st.title("📜 History Page")
    st.markdown("View and manage the prediction history below.")
    display_history()
