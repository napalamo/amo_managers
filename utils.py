import os
from dotenv import load_dotenv
import requests
import pandas as pd
import streamlit as st
import json

def load_env_variables():
    load_dotenv()
    global API_FETCH_URL, API_UPDATE_URL, API_ANALYTICS_URL
    API_FETCH_URL = os.getenv('API_FETCH_URL')
    API_UPDATE_URL = os.getenv('API_UPDATE_URL')
    API_ANALYTICS_URL = os.getenv('API_ANALUTICS_URL')

def fetch_data():
    response = requests.post(API_FETCH_URL)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        df.rename(columns={
            'name': 'Имя Менедежра', 
            'chat_id':'ID чата',
            'is_active': 'Активен', 
            'lead_count': 'Лимит лидов', 
            'top_lead_count': 'Лимит Топ',
            'is_distribute_top_leads': 'Топ', 
            'top_men_lead_count': 'Лимит Топ Муж', 
            'is_distribute_top_men_leads': 'Топ Муж', 
            'is_allow_over_limit': 'Превышать лимит',
            'timezone': 'Часовой пояс'
        }, inplace=True)
        df['Активен'] = df['Активен'].astype(bool)       
        df['Превышать лимит'] = df['Превышать лимит'].astype(bool)
        df['Топ'] = df['Топ'].astype(bool)
        df['Топ Муж'] = df['Топ Муж'].astype(bool) 
        df.index = range(1, len(df) + 1)
        df.reset_index(inplace=True)
        df.rename(columns={'index': '№'}, inplace=True)
        return df
    else:
        st.error('Ошибка при получении данных')
        return pd.DataFrame()

# Функция для отправки измененных данных обратно на сервер
def send_data(data_list):

    # Словарь для обратного переименования
    reverse_column_names = {
        'Имя Менедежра': 'name', 
        'Активен': 'is_active',
        'Лимит лидов': 'lead_count',
        'Лимит Топ': 'top_lead_count', 
        'Топ': 'is_distribute_top_leads',     
        'Лимит Топ Муж': 'top_men_lead_count',
        'Топ Муж': 'is_distribute_top_men_leads',
        'Превышать лимит': 'is_allow_over_limit',
        'Часовой пояс': 'timezone'
    }

    # Обновляем ключи в каждом словаре в списке
    updated_data_list = []
    for item in data_list:
        updated_item = {reverse_column_names.get(k, k): v for k, v in item.items()}
        updated_data_list.append(updated_item)

    # Отправляем обновлённые данные
    # Сериализуем список словарей в строку JSON
    json_data = json.dumps(updated_data_list)

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
      
