import streamlit as st
import pandas as pd
from utils import fetch_data, send_data, find_changes, mustAssigment


# Ключи API сохраняются в данных, русские названия задаются только для интерфейса.
COLUMN_LABELS = {
    'name': 'Имя Менеджера',
    'chat_id': 'ID чата',
    'is_active': 'Активен',
    'lead_count': 'Лимит лидов (кроме инст)',
    'is_allow_over_limit': 'Превышать лимит',
    'is_distribute_top_leads': 'ТОП',
    'top_lead_count': 'Лимит ТОП (весь трафик)',
    'is_allow_over_limit_top': 'Превышать лимит ТОП',
    'is_distribute_top_men_leads': 'ТОП МУЖ',
    'top_men_lead_count': 'Лимит ТОП МУЖ (весь трафик)',
    'is_allow_over_limit_topman': 'Превышать лимит МУЖ',
    'is_distribute_instform_leads': 'ИНСТ (л/формы)',
    'inst_form_count': 'Лимит ИНСТ (л/формы)',
    'is_allow_over_limit_inst_form': 'Превышать лимит ИНСТ (л/формы)',
    'is_distribute_instdialog_leads': 'ИНСТ (диалоги)',
    'inst_dialog_count': 'Лимит ИНСТ (диалоги)',
    'is_allow_over_limit_inst_dialog': 'Превышать лимит ИНСТ (диалоги)',
    'timezone': 'Часовой пояс',
}


def show():
    st.title('Управление списком менеджеров')

    # После обновления кода старые данные с русскими ключами нужно загрузить заново.
    if 'data' in st.session_state and 'Имя Менеджера' in st.session_state['data'].columns:
        st.session_state.pop('data', None)
        st.session_state.pop('original_data', None)

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button('Обновить список менеджеров'):
            data = fetch_data()
            st.session_state['data'] = data
            st.session_state['original_data'] = data.copy()
    with col2:
        if st.button('Принудительное распределение'):
            mustAssigment()

    if 'data' in st.session_state:
        if st.session_state['data'].empty:
            st.info('Нет данных для отображения.')
            return

        # Порядок полей API сохраняется; номер строки существует только в интерфейсе.
        data_to_display = st.session_state['data'].drop(columns=['id']).copy()
        data_to_display.insert(0, 'row_number', range(1, len(data_to_display) + 1))

        num_rows = data_to_display.shape[0]
        row_height = 35
        total_height = num_rows * row_height + 35

        column_config = {
            column: st.column_config.Column(label=label)
            for column, label in COLUMN_LABELS.items()
        }
        column_config['row_number'] = st.column_config.NumberColumn(
            label='№', disabled=True,
        )
        column_config['is_allow_over_limit_inst_form'] = st.column_config.CheckboxColumn(
            label='Превышать ИНСТ л/ф',
            width=160,
            help=COLUMN_LABELS['is_allow_over_limit_inst_form'],
        )

        edited_data = st.data_editor(
            data_to_display,
            height=total_height,
            hide_index=True,
            column_config=column_config,
        )

        if st.button('Сохранить настройки'):
            edited_data_for_sending = pd.concat([
                st.session_state['data']['id'].reset_index(drop=True),
                edited_data.drop(columns=['row_number']).reset_index(drop=True),
            ], axis=1)
            changes = find_changes(st.session_state['original_data'], edited_data_for_sending)
            send_data(changes)
