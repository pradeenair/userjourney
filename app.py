import pandas as pd
import streamlit as st
from pandas import ExcelFile
import openpyxl

@st.cache
def process_data(file):
    df = pd.read_excel(file, engine='openpyxl')
    df = df.drop_duplicates(subset='url', keep='first')
    df = df[df['actionDetails'].notna()]
    df['serverTimePretty'] = pd.to_datetime(df['serverTime'], unit='ms').dt.date.astype(str)
    df['url'] = df['url'].str.wrap(50)
    df = df[['serverTimePretty', 'url', 'email', 'referrerTypeName', 'referrerName', 'referrerKeyword']]
    df = df.dropna(how='all')
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
    return df

def main():
    st.set_page_config(page_title='User Journey Streamlit
