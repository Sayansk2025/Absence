import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

# Функция для создания столбчатой диаграммы
def plot_absences_by_class(data, date):
    # Фильтруем данные по выбранной дате
    daily_data = data[data["Дата"] == date]
    
    if not daily_data.empty:
        # Группируем по классам и суммируем показатели
        class_stats = daily_data.groupby("Класс").agg({
            "Всего отсутствует": "sum",
            "По болезни (количество)": "sum",
            "По уважительной причине (количество)": "sum",
            "По неуважительной причине (количество)": "sum"
        }).reset_index()
        
        # Сортируем классы для правильного отображения
        class_stats = class_stats.sort_values("Класс")
        
        # Создаем график
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Ширина столбцов
        width = 0.2
        x = range(len(class_stats["Класс"]))
        
        # Столбцы для каждого типа пропусков
        ax.bar(x, class_stats["По болезни (количество)"], width, label='По болезни', color='#1f77b4')
        ax.bar([i + width for i in x], class_stats["По уважительной причине (количество)"], 
               width, label='Уважительная причина', color='#ff7f0e')
        ax.bar([i + width*2 for i in x], class_stats["По неуважительной причине (количество)"], 
               width, label='Неуважительная причина', color='#d62728')
        ax.bar([i + width*3 for i in x], class_stats["Всего отсутствует"], 
               width, label='Всего отсутствует', color='#2ca02c', alpha=0.3)
        
        # Настройки графика
        ax.set_xlabel('Классы')
        ax.set_ylabel('Количество учеников')
        ax.set_title(f'Динамика пропусков по классам на {date}')
        ax.set_xticks([i + width*1.5 for i in x])
        ax.set_xticklabels(class_stats["Класс"], rotation=45)
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Нет данных для выбранной даты")

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
                st.subheader("Выберите параметры для анализа:")
                
                # Выбор временного периода
                date_range = st.selectbox("Период анализа:", 
                                         ["За день", "За неделю", "За месяц", "За весь период"])
                
                # Выбор даты/диапазона дат
                if date_range == "За день":
                    selected_date = st.selectbox("Дата", sorted(data["Дата"].unique(), reverse=True))
                    date_filter = [selected_date]
                elif date_range == "За неделю":
                    # Упрощенная реализация - выбор одной даты и берем 7 дней назад
                    base_date = st.selectbox("Дата окончания недели", 
                                           sorted(data["Дата"].unique(), reverse=True))
                    date_filter = sorted([d for d in data["Дата"].unique() 
                                        if pd.to_datetime(d) >= pd.to_datetime(base_date) - pd.Timedelta(days=7) 
                                        and pd.to_datetime(d) <= pd.to_datetime(base_date)])
                elif date_range == "За месяц":
                    base_date = st.selectbox("Месяц и год", 
                                           sorted(data["Дата"].unique(), reverse=True))
                    date_filter = [d for d in data["Дата"].unique() 
                                 if pd.to_datetime(d).month == pd.to_datetime(base_date).month 
                                 and pd.to_datetime(d).year == pd.to_datetime(base_date).year]
                else:  # За весь период
                    date_filter = data["Дата"].unique()

                # Фильтрация по классу
                classes = data["Класс"].unique()
                selected_class = st.selectbox("Класс", ["Все"] + list(classes))

                analyze_button = st.form_submit_button("Проанализировать")

            if analyze_button:
                filtered_data = data[data["Дата"].isin(date_filter)]
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
                    
                    if date_range == "За день":
                        st.write(f"Дата: {date_filter[0]}")
                    else:
                        st.write(f"Период: {date_range}")
                    
                    st.write(f"Класс: {selected_class if selected_class != 'Все' else 'Все классы'}")
                    st.write(f"Всего отсутствует: {total_absent}")
                    st.write(f"По болезни: {sick_count} ({sick_count/total_absent*100:.1f}%)")
                    st.write(f"По уважительной причине: {valid_count} ({valid_count/total_absent*100:.1f}%)")
                    st.write(f"По неуважительной причине: {invalid_count} ({invalid_count/total_absent*100:.1f}%)")
                    
                    # Отображение графиков
                    st.subheader("Визуализация данных")
                    
                    if date_range == "За день":
                        # Столбчатая диаграмма по классам для выбранного дня
                        plot_absences_by_class(data, date_filter[0])
                    else:
                        # Линейный график динамики за период
                        st.write("Динамика пропусков за выбранный период:")
                        
                        # Группируем по датам и суммируем показатели
                        period_stats = filtered_data.groupby("Дата").agg({
                            "Всего отсутствует": "sum",
                            "По болезни (количество)": "sum",
                            "По уважительной причине (количество)": "sum",
                            "По неуважительной причине (количество)": "sum"
                        }).sort_index()
                        
                        # Создаем график
                        fig, ax = plt.subplots(figsize=(12, 6))
                        period_stats.plot(ax=ax, marker='o')
                        ax.set_title(f"Динамика пропусков за период")
                        ax.set_xlabel("Дата")
                        ax.set_ylabel("Количество учеников")
                        ax.grid(True)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                        # Дополнительно: столбчатая диаграмма по классам за весь период
                        if selected_class == "Все":
                            st.subheader("Сравнение классов за период")
                            class_stats = filtered_data.groupby("Класс").agg({
                                "Всего отсутствует": "sum",
                                "По болезни (количество)": "sum",
                                "По уважительной причине (количество)": "sum",
                                "По неуважительной причине (количество)": "sum"
                            }).sort_index()
                            
                            fig, ax = plt.subplots(figsize=(12, 6))
                            class_stats.plot(kind='bar', ax=ax, stacked=True)
                            ax.set_title(f"Пропуски по классам за период")
                            ax.set_xlabel("Класс")
                            ax.set_ylabel("Количество учеников")
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                            st.pyplot(fig)
                else:
                    st.warning("Нет данных для выбранных параметров.")
        else:
            st.warning("Нет данных для анализа.")

if __name__ == "__main__":
    main()
