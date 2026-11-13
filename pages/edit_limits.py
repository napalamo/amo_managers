import streamlit as st
import pandas as pd
from utils import fetch_data, send_data, find_changes, mustAssigment


# Ключи API сохраняются в данных, русские названия задаются только для интерфейса.
COLUMN_LABEL_LIMIT_CNT = 'Лимит'
COLUMN_LABEL_ALLOW = 'Превышать'

COLUMN_LABELS = {
    'name': 'Имя Менеджера',
    'chat_id': 'ID чата',

    'is_active': 'Активен',
    'lead_count': COLUMN_LABEL_LIMIT_CNT,
    'is_allow_over_limit': COLUMN_LABEL_ALLOW,

    'is_distribute_top_leads': 'ТОП',
    'top_lead_count': COLUMN_LABEL_LIMIT_CNT,
    'is_allow_over_limit_top': COLUMN_LABEL_ALLOW,

    'is_distribute_top_men_leads': 'ТОП МУЖ',
    'top_men_lead_count': COLUMN_LABEL_LIMIT_CNT,
    'is_allow_over_limit_topman': COLUMN_LABEL_ALLOW,

    'is_distribute_instform_leads': 'ИНСТ л/формы',
    'inst_form_count': COLUMN_LABEL_LIMIT_CNT,
    'is_allow_over_limit_inst_form': COLUMN_LABEL_ALLOW,

    'is_distribute_instdialog_leads': 'ИНСТ диалоги',
    'inst_dialog_count': COLUMN_LABEL_LIMIT_CNT,
    'is_allow_over_limit_inst_dialog': COLUMN_LABEL_ALLOW,

    'timezone': 'Часовой пояс',
}

COLUMN_HELPS = {
    'lead_count': 'Лимит лидов (кроме инст)',
    'is_distribute_top_leads': 'ТОП (весь трафик)',
    'is_distribute_top_men_leads': 'ТОП Мужчины (весь трафик)',
    'is_distribute_instform_leads': 'Instagram лид-формы',
    'is_distribute_instdialog_leads': 'Instagram диалоговые лиды',
}

COLUMN_WIDTH_ALLOW = 160
COLUMN_WIDTH_LIMIT_CNT = 80

COLUMN_WIDTHS = {
    'lead_count': COLUMN_WIDTH_LIMIT_CNT,
    'is_allow_over_limit': COLUMN_WIDTH_ALLOW,

    'top_lead_count': COLUMN_WIDTH_LIMIT_CNT,
    'is_allow_over_limit_top': COLUMN_WIDTH_ALLOW,

    'top_men_lead_count': COLUMN_WIDTH_LIMIT_CNT,
    'is_allow_over_limit_topman': COLUMN_WIDTH_ALLOW,

    'inst_form_count': COLUMN_WIDTH_LIMIT_CNT,
    'is_allow_over_limit_inst_form': COLUMN_WIDTH_ALLOW,

    'inst_dialog_count': COLUMN_WIDTH_LIMIT_CNT,
    'is_allow_over_limit_inst_dialog': COLUMN_WIDTH_ALLOW,
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
            column: st.column_config.Column(
                label=label,
                help=COLUMN_HELPS.get(column),
                width=COLUMN_WIDTHS.get(column),
            )
            for column, label in COLUMN_LABELS.items()
        }

        column_config['row_number'] = st.column_config.NumberColumn(
            label='№',
            disabled=True,
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
