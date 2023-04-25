```python
import pandas as pd
import streamlit as st

# Use st.cache_data to cache the processed dataframe
@st.cache_data
def process_data(file):
    df = pd.read_excel(file, engine='openpyxl')
    st.write("Original Dataframe:")
    st.write(df)
    try:
        df = df.drop_duplicates(subset='url', keep='first')
        df = df[df['actionDetails'].notna()]
        df['serverTimePretty'] = pd.to_datetime(df['serverTime'], unit='ms').dt.date.astype(str)
        df['url'] = df['url'].str.wrap(50)
        df = df[['serverTimePretty', 'url', 'email', 'referrerTypeName', 'referrerName', 'referrerKeyword']]
        df = df.dropna(subset=['url'])
        df.insert(1, '', '')
        df.insert(4, '', '')
        df.insert(7, '', '')
        df.insert(8, 'eventAction', '')
        event_actions = ['signup-online', 'signup-onpremise', 'contact-us']
        for action in event_actions:
            if action in df['action'].values:
                df.loc[df['action'] == action, 'eventAction'] = action
                break
        df = df.drop(['action', 'actionDetails'], axis=1)
        df = df.reset_index(drop=True)
        st.write("Processed Dataframe:")
        st.write(df)
        return df
    except Exception as e:
        st.write(f"Error: {e}")
        return None

def main():
    st.set_page_config(page_title='User Journey Streamlit App', layout='wide')
    st.title('User Journey Streamlit App')

    # Use st.cache_resource to cache the uploaded file
    uploaded_file = st.cache_resource(st.file_uploader('Choose an Excel file', type=['xlsx', 'xls']))

    if uploaded_file is not None:
        df = process_data(uploaded_file)
        if df is not None:
            st.table(df)

if __name__ == '__main__':
    main()
```
