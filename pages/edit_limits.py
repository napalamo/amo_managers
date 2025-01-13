import streamlit as st
import pandas as pd
from utils import fetch_data, send_data, find_changes

def show():
    st.title('Управление списком менеджеров')

    if st.button('Обновить список менеджеров'):
        data = fetch_data()
        st.session_state['data'] = data
        st.session_state['original_data'] = data.copy()

    if 'data' in st.session_state:
        # Убираем колонку id для отображения
        data_to_display = st.session_state['data'].drop(columns=['id'])
        
        # Рассчитываем высоту на основе количества строк в данных
        num_rows = data_to_display.shape[0]
        row_height = 35  # Высота одной строки в пикселях (примерная)
        total_height = num_rows * row_height + 35  # Добавляем 35 пикселей для заголовка

        # Показываем редактор данных с динамической высотой
        edited_data = st.data_editor(data_to_display, height=total_height, hide_index=True)

        if st.button('Сохранить настройки'):
            # Подготовка данных к отправке
            edited_data_for_sending = pd.concat([st.session_state['data']['id'].reset_index(drop=True), edited_data.reset_index(drop=True)], axis=1)
            # Сравниваем с исходными данными
            changes = find_changes(st.session_state['original_data'], edited_data_for_sending)
            send_data(changes)
