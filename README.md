## Дисклеймер

Это задание выполненно без использования LLMs, агентов 
и других нейросетевых технологий. Весь тест-дизайн, а так же 
архитектурный дизайн тест-фреймворка, тестов, GitHub Actions Workflow
были разработаны мной основываясь на моём опыте, экспертизе, которые я приобрёл
в процессе работы, учёбы.

# API-тесты для проекта https://qa-internship.avito.com/

### Запуск предпоследнего workflow (пайплайна) на GitHub Actions

https://funkerone.github.io/qa-internship-advert/14/index.html

## Запуск тестов

1. Склонируйте репозиторий
2. Перейдите в корень проекта

```bash
cd path/to/dir
```
3. Создайте виртуальноe окружение:

Unix-подобные ОС
```bash
python3 -m venv .venv
```
Windows
```powershell
python -m venv .venv
```
4. Активируйте .venv:

```bash
source .venv/bin/activate
```
Windows
```powershell
.\.venv\Scripts\Activate.ps1
```
5. Подтяните необходимые зависимости через команду в корне проекта:

```bash
pip install -r requirements.txt
```
6. Для запуска всех тестов достаточно выполнить команду в корне проекта:

```bash
pytest --alluredir=allure-results
```
## Открытие Allure отчёта
1. Перейти в директорию allure-report
```bash
cd allure-report
```
2. Запустите файл index.html в вашем любимом браузере

## Запуск реформата ruff
```bash
ruff format . --line-length=100
```

## Запуск линтера ruff
```bash
ruff check . --fix --line-length=100
```