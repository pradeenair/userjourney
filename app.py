import streamlit as st
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")
st.beta_set_page_config(page_title="User Journey Analysis")
st.title("User Journey Analysis")

# add this line to install openpyxl
st.set_option('deprecation.showfileUploaderEncoding', False)
!pip install openpyxl
import streamlit as st
import pandas as pd

# Define a function to process the input data and generate the final output
def process_data(file):
    # Read the input Excel file into a pandas dataframe
    df = pd.read_excel(file)

    # Filter the dataframe to only display the required columns
    df = df.filter(regex='(actionDetails|Keyword|eventAction|eventName)')

    # Remove duplicate URLs and keep the first occurrence only
    df = df.loc[df['url'].drop_duplicates().index]

    # Ignore blank columns
    df = df.dropna(how='all', axis=1)

    # Add a new column to display the serverTimePretty value as date only
    df['Date'] = pd.to_datetime(df['serverTimePretty']).dt.date

    # Display the email address, Referrer Type, Referrer Name, Referrer Keyword, City and Country
    df['Email'] = df['visitorId'].str.extract(r'(\S+@\S+\.\S+)', expand=False)
    df[['Referrer Type', 'Referrer Name', 'Referrer Keyword']] = df[['referrerTypeName', 'referrerName', 'referrerKeyword']]

    # Add a new column for the first occurrence of either "signup-online", "signup-onpremise" or "contact-us" under the eventAction column
    event_actions = ['signup-online', 'signup-onpremise', 'contact-us']
    event_col = 'eventAction'
    for action in event_actions:
        if action in df[event_col].values:
            df[event_col] = action
            break

    # Drop the rows with no URLs
    df = df.dropna(subset=['url'])

    # Display the final table output
    st.table(df)

# Create the Streamlit app
def main():
    st.title("Excel Data Processor")

    # Add a file upload component to allow the user to upload an Excel file
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

    # If a file is uploaded, process the data and display the final output
    if uploaded_file is not None:
        process_data(uploaded_file)

if __name__ == '__main__':
    main()
