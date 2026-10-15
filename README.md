# Modern Data Stack — Мікрокредитування (Варіант 10)

Лабораторна робота №1: Data Lake + Ingestion (Extract & Load)

## Опис
Побудова сирого (raw) шару аналітичного сховища даних для мікрокредитної компанії.

### Таблиці
**Виміри:**
- `loan_types` — типи позик
- `credit_scores` — кредитні рейтинги
- `borrowers` — позичальники

**Факти:**
- `issued_loans` — видані кредити
- `repayments` — погашення

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