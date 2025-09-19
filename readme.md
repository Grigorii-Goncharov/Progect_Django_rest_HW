# Название Проекта

**Краткое описание:**
Этот проект представляет собой [краткое описание того, что делает проект].

---

## Содержание

1.  **Обзор**
2.  **Установка**
3.  **Использование**
Наполнить базу из фикстур:
 - python manage.py loaddata payment_fixture_load.json --ignorenonexistent
 - python manage.py loaddata user_fixture_load.json --ignorenonexistent
- Примеры запросов:
        GET /api/payments/ — список всех платежей
        GET /api/payments/?course=1&ordering=-payment_date — платежи за курс 1, отсортированные по убыванию даты
        GET /api//users/payment/?payment_method=transfer - фильтрация по полю "payment_method"

4.  **Лицензия**
5.  **Контакты**

---

## 1. Обзор

В этом разделе подробно описывается назначение проекта, его основные возможности и преимущества.

---

## 2. Установка

**Шаг 1:** Клонируйте репозиторий:
```bash
git clone https://github.com/Grigorii-Goncharov/Progect_Django_rest_HW