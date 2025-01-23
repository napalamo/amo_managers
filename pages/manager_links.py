import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Функция для отправки POST запроса и получения данных о менеджерах
def fetch_managers_data(url):
    response = requests.post(url, data={'action': 'get_managers'})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Ошибка при получении данных о менеджерах.")
        return []

def show():
    # URL-адрес для получения данных о менеджерах
    url_fetch = os.getenv('API_FETCH_URL')
    
    # Получение данных о менеджерах
    managers = fetch_managers_data(url_fetch)

    st.title('Ссылки для постановки на смену')
    st.write('Ниже представлены ссылки для постановки на смену у менеджеров:')
    
    # Подготовка данных для таблицы
    table_data = []
    for manager in managers:
        if 'name' in manager and 'id' in manager:
            manager_name = manager['name']
            manager_id = manager['id']
            link = f"https://working-hours-lifestylegroup2jhgjh.streamlit.app?manager_id={manager_id}"
            #link = f"<a href='https://working-hours-lifestylegroup2jhgjh.streamlit.app?manager_id={manager_id}' target='_blank' rel='noopener noreferrer'>https://working-hours-lifestylegroup2jhgjh.streamlit.app?manager_id={manager_id}</a>"
            table_data.append({'Имя менеджера': manager_name, 'Ссылка': link})
    
    # Создание DataFrame для отображения в таблице
    if table_data:
        df = pd.DataFrame(table_data)
        
        # Рассчитываем высоту на основе количества строк в данных
        num_rows = df.shape[0]
        row_height = 35  # Высота одной строки в пикселях (примерная)
        total_height = num_rows * row_height + 35  # Добавляем 35 пикселей для заголовка

        # Отображение таблицы без индекса и с динамической высотой и шириной
        st.dataframe(df, use_container_width=True, height=total_height)
    else:
        st.warning("Нет доступных менеджеров для отображения.")

if __name__ == "__main__":
    show()
