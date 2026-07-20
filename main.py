import streamlit as st
from pages import edit_limits, statistics, manager_links
from utils import load_env_variables

def main():
    load_env_variables()
    
    st.set_page_config(page_title='Управление менеджерами', page_icon=':dizzy:', layout='wide')
    
    # Отключаем автоматическое создание меню
    st.set_option('client.showSidebarNavigation', False)
    
    st.sidebar.title('Меню')
    page = st.sidebar.radio("Выберите страницу:", ['📝 Изменить лимиты', '📈 Статистика', '🔗 Ссылки'])

    if page == '📝 Изменить лимиты':
        edit_limits.show()
    elif page == '📈 Статистика':
        statistics.show()
    elif page == '🔗 Ссылки.':
        manager_links.show()

if __name__ == '__main__':
    main()
