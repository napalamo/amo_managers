import os
from dotenv import load_dotenv
import requests
import pandas as pd
import streamlit as st
import json

def load_env_variables():
    load_dotenv()
    global API_FETCH_URL, API_UPDATE_URL, API_ANALYTICS_URL, API_FORCE_URL
    API_FETCH_URL = os.getenv('API_FETCH_URL')
    API_UPDATE_URL = os.getenv('API_UPDATE_URL')
    API_ANALYTICS_URL = os.getenv('API_ANALUTICS_URL')
    API_FORCE_URL = os.getenv('API_FORCE_URL')

def fetch_data():
    response = requests.post(API_FETCH_URL)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        boolean_columns = [
            'is_active',
            'is_allow_over_limit',
            'is_allow_over_limit_top',
            'is_allow_over_limit_inst_form',
            'is_allow_over_limit_inst_dialog',
            'is_allow_over_limit_topman',
            'is_distribute_top_leads',
            'is_distribute_top_men_leads',
            'is_distribute_instform_leads',
            'is_distribute_instdialog_leads',
        ]
        for column in boolean_columns:
            if column in df.columns:
                df[column] = df[column].astype(bool)
        return df
    else:
        st.error('Ошибка при получении данных')
        return pd.DataFrame()

# Функция для отправки измененных данных обратно на сервер
def send_data(data_list):

    json_data = json.dumps(data_list)

    # Отправляем строку JSON как form-data
    response = requests.post(API_UPDATE_URL, data={'data': json_data})

    if response.status_code == 200:
        st.success('Настройки сохранены')
    else:
        st.error('Ошибка при сохранении данных')

# Функция для нахождения изменений
def find_changes(original_data, edited_data):
    changes = []
    for edited_row in edited_data.to_dict('records'):
        original_row = original_data.loc[original_data['id'] == edited_row['id']].to_dict('records')[0]
        if edited_row != original_row:
            changes.append(edited_row)
    return changes

def fetch_statistics(start_date, end_date, type_lead):
    response = requests.post(API_ANALYTICS_URL, data={'start_date': start_date, 'end_date': end_date, 'type_lead': type_lead})
    if response.status_code == 200:
        raw_data = response.json()
        return raw_data
    else:
        st.error('Ошибка при получении статистики')
        return None
      
def mustAssigment():
    response = requests.post(API_FORCE_URL)
    if response.status_code == 200:
        st.success('Принудительное распределение запущено')
    else:
        st.error('Ошибка при запуске распределения')
