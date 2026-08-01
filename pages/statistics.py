import streamlit as st
from datetime import datetime, time
from utils import fetch_statistics
import pandas as pd

def process_data(raw_data):
    managers = {}
    all_statuses = {}
    
    # Собираем данные по менеджерам и статусам
    for manager in raw_data:
        manager_id = manager['manager_id']
        manager_name = manager['manager_name']
        managers[manager_id] = {'Имя': manager_name}
        for status in manager['statuses']:
            status_id = status['id']
            status_name = status['name']
            managers[manager_id][status_name] = status['lead_count']
            all_statuses[status_name] = status_id
    
    # Создаем DataFrame
    df = pd.DataFrame.from_dict(managers, orient='index')
    
    # Добавляем отсутствующие статусы со значением 0
    for status in all_statuses:
        if status not in df.columns:
            df[status] = 0
    
    # Сортируем колонки по id статуса
    sorted_statuses = sorted(all_statuses.items(), key=lambda x: x[1])
    column_order = ['Имя'] + [status[0] for status in sorted_statuses]
    df = df.reindex(columns=column_order)
    
    return df

def show():
    st.title('Статистика')
    
    start_date_value = st.date_input("Дата начала", datetime.today())
    end_date_value = st.date_input("Дата окончания", datetime.today())
    start_datetime = datetime.combine(start_date_value, time.min)
    end_datetime = datetime.combine(end_date_value, time.max)
    
    lead_types = {"Обычный": "standart", "TOP": "top", "TOP MAN": "top_men"}
    
    if st.button('Получить аналитику'):
        # Отображение индикатора загрузки данных
        with st.spinner('Загрузка данных...'):
            results = {}
            for lead_type_name, lead_type_key in lead_types.items():
                raw_data = fetch_statistics(start_datetime, end_datetime, lead_type_key)
                if raw_data:
                    results[lead_type_name] = process_data(raw_data)
        
        if results:
            for lead_type_name, processed_df in results.items():
                st.subheader(f"Тип лида - {lead_type_name}:")
                
                # Добавление порядкового номера
                processed_df = processed_df.reset_index(drop=True)
                processed_df.index += 1
                processed_df.index.name = '№'
                
                # Отображение таблицы
                st.dataframe(processed_df, height=processed_df.shape[0] * 35 + 35)  # высота по количеству строк
            
        else:
            st.error("Не удалось получить данные или данные отсутствуют.")
