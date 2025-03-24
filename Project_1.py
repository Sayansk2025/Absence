import streamlit as st
import pandas as pd
from datetime import datetime

# Функция для загрузки данных из Excel
def load_data(filename="school_absences.xlsx"):
    try:
        return pd.read_excel(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Дата", "Класс", "Всего отсутствует",
            "По болезни (количество)", "По уважительной причине (количество)",
            "По неуважительной причине (количество)"
        ])

# Функция для сохранения данных в Excel
def save_data(df, filename="school_absences.xlsx"):
    try:
        df.to_excel(filename, index=False)
    except Exception as e:
        st.error(f"Ошибка при сохранении данных: {e}")

# Инициализация состояния Session State
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Главная функция приложения
def main():
    st.title("Приложение для учета отсутствующих учеников")

    # Выбор режима: Внести данные или Анализировать данные
    mode = st.sidebar.radio("Выберите режим:", ("Внести данные", "Анализировать данные"))

    if mode == "Внести данные":
        st.header("Внести данные")
        with st.form("data_entry_form"):
            date = st.date_input("Дата")
            classes = [f"{i}{letter}" for i in range(1, 12) for letter in "АБВГ"]
            class_selected = st.selectbox("Класс", classes)
            total_absent = st.number_input("Всего отсутствует", min_value=0, step=1)

            # Поля для ввода количества отсутствующих по разным причинам
            sick_count = st.number_input("По болезни (количество)", min_value=0, step=1)
            valid_count = st.number_input("По уважительной причине (количество)", min_value=0, step=1)
            invalid_count = st.number_input("По неуважительной причине (количество)", min_value=0, step=1)

            # Проверка на сумму
            if sick_count + valid_count + invalid_count > total_absent:
                st.error("Сумма отсутствующих по всем причинам превышает общее количество!")

            submit_button = st.form_submit_button("Внести данные")

        # Обработка отправки формы
        if submit_button and sick_count + valid_count + invalid_count <= total_absent:
            new_row = {
                "Дата": date.strftime("%Y-%m-%d"),
                "Класс": class_selected,
                "Всего отсутствует": total_absent,
                "По болезни (количество)": sick_count,
                "По уважительной причине (количество)": valid_count,
                "По неуважительной причине (количество)": invalid_count
            }
            st.session_state.data = pd.concat(
                [st.session_state.data, pd.DataFrame([new_row])], ignore_index=True
            )
            save_data(st.session_state.data)
            st.success("Данные успешно внесены!")

    elif mode == "Анализировать данные":
        st.header("Анализировать данные")
        data = st.session_state.data

        if not data.empty:
            # Форма для анализа данных
            with st.form("analysis_form"):
                st.subheader("Выберите дату для анализа:")
                unique_dates = data["Дата"].unique()
                selected_date = st.selectbox("Дата", unique_dates)

                # Фильтрация по классу
                classes = data[data["Дата"] == selected_date]["Класс"].unique()
                selected_class = st.selectbox("Класс", ["Все"] + list(classes))

                analyze_button = st.form_submit_button("Проанализировать")

            if analyze_button:
                filtered_data = data[data["Дата"] == selected_date]
                if selected_class != "Все":
                    filtered_data = filtered_data[filtered_data["Класс"] == selected_class]

                if not filtered_data.empty:
                    # Подсчет статистики
                    total_absent = int(filtered_data["Всего отсутствует"].sum())
                    sick_count = int(filtered_data["По болезни (количество)"].sum())
                    valid_count = int(filtered_data["По уважительной причине (количество)"].sum())
                    invalid_count = int(filtered_data["По неуважительной причине (количество)"].sum())

                    # Вывод результатов
                    st.subheader("Результаты анализа:")
                    st.write(f"Дата: {selected_date}")
                    st.write(f"Класс: {selected_class if selected_class != 'Все' else 'Все классы'}")
                    st.write(f"Всего отсутствует: {total_absent}")
                    st.write(f"По болезни: {sick_count}")
                    st.write(f"По уважительной причине: {valid_count}")
                    st.write(f"По неуважительной причине: {invalid_count}")
                else:
                    st.warning("Нет данных для выбранной даты и класса.")
        else:
            st.warning("Нет данных для анализа.")

if __name__ == "__main__":
    main()