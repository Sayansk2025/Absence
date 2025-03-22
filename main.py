import pandas as pd
import streamlit as st
import os

# Функция для внесения данных
def input_data():
    st.header("Внесение данных")
    
    # Поле для названия мероприятия
    event_name = st.text_input("Название мероприятия")
    if not event_name:
        st.warning("Пожалуйста, введите название мероприятия.")
        return
    
    # Поле для уровня мероприятия
    event_level = st.selectbox("Уровень мероприятия", ["Областной", "Региональный", "Городской", "Школьный"])
    
    # Поле для выбора типа мероприятия
    event_type = st.radio("Тип мероприятия", ["Индивидуальный", "Групповой"])
    
    # Поле для выбора результата участия
    result_options = [
        "Победитель", "Призер (2 место)", "Призер (3 место)", "Участник",
        "Диплом 1 степени", "Диплом 2 степени", "Диплом 3 степени",
        "Лауреат", "Гран-при", "Дипломант", "Специальный приз"
    ]
    event_result = st.selectbox("Результат участия", result_options)
    
    participants = []
    classes = []
    
    # Внесение участников в зависимости от типа мероприятия
    if event_type == "Индивидуальный":
        participants_input = st.text_area("Введите имена участников (каждое имя с новой строки)")
        participants = [name.strip() for name in participants_input.split("\n") if name.strip()]
        
        # Поле для ввода класса для индивидуального мероприятия
        class_input = st.text_input("Введите класс участника (например, 10А)")
        if class_input:
            classes = [class_input] * len(participants)
        else:
            st.warning("Пожалуйста, введите класс участника.")
            return
    else:
        # Множественный выбор классов для группового мероприятия
        class_options = [f"{i}{j}" for i in range(1, 12) for j in ['А', 'Б', 'В']]
        selected_classes = st.multiselect("Выберите классы", class_options)
        
        if not selected_classes:
            st.warning("Пожалуйста, выберите хотя бы один класс.")
            return
        
        for cls in selected_classes:
            # Поле для ввода количества учеников в каждом классе
            count = st.number_input(f"Количество учеников в классе {cls}", min_value=1, max_value=50, value=1, key=f"count_{cls}")
            
            # Текстовые поля для ввода имен учеников
            st.write(f"Введите имена учеников для класса {cls}:")
            for i in range(1, count + 1):
                student_name = st.text_input(f"Ученик {i} из {cls}", key=f"student_{cls}_{i}")
                if student_name:  # Если имя введено, добавляем его в список участников
                    participants.append(student_name)
                    classes.append(cls)
    
    if not participants:
        st.warning("Пожалуйста, введите хотя бы одного участника.")
        return
    
    # Кнопка для сохранения данных и создания таблицы
    if st.button("Сохранить данные"):
        save_data(event_name, event_level, event_type, event_result, participants, classes)

# Функция для анализа данных
def analyze_data():
    st.header("Анализ данных")
    
    # Загрузка данных из файла
    try:
        df = pd.read_excel("events_data.xlsx")
    except FileNotFoundError:
        st.warning("Файл с данными не найден. Пожалуйста, сначала внесите данные.")
        return
    
    # Выбор анализа: по классу или по ученику
    analysis_type = st.radio("Выберите тип анализа", ["По классу", "По ученику"])
    
    if analysis_type == "По классу":
        # Анализ по классу
        class_options = df["Класс"].dropna().unique()
        selected_class = st.selectbox("Выберите класс", class_options)
        
        # Фильтрация данных по выбранному классу
        class_data = df[df["Класс"] == selected_class]
        
        # Группировка по результату участия
        result_counts = class_data["Результат участия"].value_counts().reset_index()
        result_counts.columns = ["Результат", "Количество"]
        
        st.write(f"### Результаты для класса {selected_class}")
        st.write(result_counts)
        
        # Список мероприятий для класса
