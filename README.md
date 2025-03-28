# Приложение для учета отсутствующих учеников

## Описание проекта
Это веб-приложение, созданное с использованием **Streamlit**, позволяет вести учет данных об отсутствующих учениках в школе. Пользователи могут вносить данные о пропусках по разным причинам (болезнь, уважительная причина, неуважительная причина) и анализировать их с помощью различных фильтров и визуализаций.

## Функциональность
### Основные возможности:
1. **Внесение данных**:
   - Ввод информации о дате, классе и количестве отсутствующих учеников.
   - Разделение отсутствий по категориям: болезнь, уважительная причина, неуважительная причина.
   - Автоматическая проверка корректности введенных данных (сумма отсутствий по всем причинам не должна превышать общее количество).
2. **Анализ данных**:
   - Выбор периода анализа: за день, неделю, месяц или весь период.
   - Фильтрация данных по классам.
   - Подсчет статистики: общее количество отсутствий, процентное соотношение по категориям.
   - Визуализация данных:
     - Столбчатая диаграмма для сравнения пропусков по классам.
     - Линейный график для отображения динамики пропусков за выбранный период.
     - Стековая столбчатая диаграмма для анализа пропусков по классам за период.
3. **Сохранение данных**:
   - Данные сохраняются в файл `school_absences.xlsx` в формате Excel.
   - Если файл уже существует, новые данные добавляются к существующим.
---
## Установка и запуск
### Требования
- Python 3.8 или выше.
- Установленные библиотеки: `streamlit`, `pandas`, `matplotlib`.
### Установка зависимостей
Установите необходимые библиотеки с помощью pip:
pip install streamlit pandas matplotlib openpyxl

## Запуск приложения    
1. Создайте файл приложения :  
2. Сохраните код в файл с именем Project_1.py.  
3. Запустите приложение :  
4. Откройте терминал и перейдите в директорию, где находится файл Project_1.py.  
5. Выполните команду:  streamlit run Project_1.py  
6. Откройте приложение в браузере :  
7. После запуска команды в терминале появится ссылка на локальный сервер (например, http://localhost:8501).  
8. Откройте ссылку в браузере.  

