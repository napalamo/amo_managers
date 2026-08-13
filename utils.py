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
        df.rename(columns={
            'name': 'Имя Менеджера', 
            'chat_id':'ID чата', 
            'is_active': 'Активен', 
            'lead_count': 'Лимит лидов (кроме инст)', 
            'inst_form_count': 'Лимит ИНСТ (л/формы)',
            'is_distribute_instform_leads': 'ИНСТ (л/формы)',
            'inst_dialog_count': 'Лимит ИНСТ (диалоги)',
            'is_distribute_instdialog_leads': 'ИНСТ (диалоги)',
            'top_lead_count': 'Лимит ТОП (весь трафик)',
            'is_distribute_top_leads': 'ТОП', 
            'top_men_lead_count': 'Лимит ТОП МУЖ (весь трафик)', 
            'is_distribute_top_men_leads': 'ТОП МУЖ', 
            'is_allow_over_limit': 'Превышать лимит',
            'is_allow_over_limit_inst_form': 'Превышать лимит ИНСТ (л/формы)',
            'is_allow_over_limit_inst_dialog': 'Превышать лимит ИНСТ (диалоги)',
            'is_allow_over_limit_top': 'Превышать лимит ТОП' ,
            'is_allow_over_limit_topman': 'Превышать лимит МУЖ',
            'timezone': 'Часовой пояс'
        }, inplace=True)
        #df = df.sort_values(by='Активен', ascending=False)
        df['Активен'] = df['Активен'].astype(bool)
        df['Превышать лимит'] = df['Превышать лимит'].astype(bool)
        df['Превышать лимит ТОП'] = df['Превышать лимит ТОП'].astype(bool)
        df['Превышать лимит ИНСТ (л/формы)'] = df['Превышать лимит ИНСТ (л/формы)'].astype(bool)
        df['Превышать лимит ИНСТ (диалоги)'] = df['Превышать лимит ИНСТ (диалоги)'].astype(bool)
        df['Превышать лимит МУЖ'] = df['Превышать лимит МУЖ'].astype(bool)
        df['ТОП'] = df['ТОП'].astype(bool)
        df['ТОП МУЖ'] = df['ТОП МУЖ'].astype(bool) 
        df['ИНСТ (л/формы)'] = df['ИНСТ (л/формы)'].astype(bool)
        df['ИНСТ (диалоги)'] = df['ИНСТ (диалоги)'].astype(bool)
        df.index = range(1, len(df) + 1)
        df.reset_index(inplace=True)
        df.rename(columns={'index': '№'}, inplace=True)
        #return df.sort(key=lambda x: x['Активен'], reverse=True)
        return df
    else:
        st.error('Ошибка при получении данных')
        return pd.DataFrame()

# Функция для отправки измененных данных обратно на сервер
def send_data(data_list):

    # Словарь для обратного переименования
    reverse_column_names = {
        'Имя Менеджера': 'name',
        'ID чата': 'chat_id',
        'Активен': 'is_active',
        'Лимит лидов (кроме инст)': 'lead_count',
        'Лимит ИНСТ (л/формы)': 'inst_form_count',
        'ИНСТ (л/формы)': 'is_distribute_instform_leads',
        'Лимит ИНСТ (диалоги)': 'inst_dialog_count',
        'ИНСТ (диалоги)': 'is_distribute_instdialog_leads',
        'Лимит ТОП (весь трафик)': 'top_lead_count',
        'ТОП': 'is_distribute_top_leads',
        'Лимит ТОП МУЖ (весь трафик)': 'top_men_lead_count',
        'ТОП МУЖ': 'is_distribute_top_men_leads',
        'Превышать лимит': 'is_allow_over_limit',
        'Превышать лимит ИНСТ (л/формы)': 'is_allow_over_limit_inst_form',
        'Превышать лимит ИНСТ (диалоги)': 'is_allow_over_limit_inst_dialog',
        'Превышать лимит ТОП': 'is_allow_over_limit_top',
        'Превышать лимит МУЖ': 'is_allow_over_limit_topman',
        'Часовой пояс': 'timezone',

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
      
def mustAssigment():
    response = requests.post(API_FORCE_URL)
    if response.status_code == 200:
        st.success('Принудительное распределение запущено')
    else:
        st.error('Ошибка при запуске распределения')
