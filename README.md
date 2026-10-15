# Modern Data Stack — Необанк P2P (Варіант 7)

Лабораторна робота №1: Data Lake + Ingestion (Extract & Load)

## Опис
Побудова сирого (raw) шару аналітичного сховища даних для необанку (P2P перекази).

### Таблиці
**Виміри:**
- `clients` — клієнти
- `accounts` — рахунки
- `branches` — відділення / регіони

**Факти:**
- `transfers` — перекази
- `loan_payments` — платежі по кредитах

## Архітектура
- **Extract**: Python + Faker
- **Load**: SQLAlchemy → PostgreSQL (схема `raw`)
- **Infrastructure**: Docker Compose (PostgreSQL 15)

## Як запустити

1. Клонувати репозиторій
2. Створити віртуальне середовище:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt