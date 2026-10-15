import pandas as pd
from faker import Faker
import random
from sqlalchemy import create_engine, text

fake = Faker('uk_UA')
Faker.seed(42)
random.seed(42)

def generate_branches():
    print("Генерація відділень...")
    branches = [
        {'branch_id': 1, 'branch_name': 'Київ Центральний', 'city': 'Київ', 'region': 'Київська'},
        {'branch_id': 2, 'branch_name': 'Львів Головний', 'city': 'Львів', 'region': 'Львівська'},
        {'branch_id': 3, 'branch_name': 'Одеса Приморська', 'city': 'Одеса', 'region': 'Одеська'},
        {'branch_id': 4, 'branch_name': 'Харків Сумська', 'city': 'Харків', 'region': 'Харківська'},
        {'branch_id': 5, 'branch_name': 'Дніпро Набережна', 'city': 'Дніпро', 'region': 'Дніпропетровська'},
        {'branch_id': 6, 'branch_name': 'Вінниця Центр', 'city': 'Вінниця', 'region': 'Вінницька'},
    ]
    return pd.DataFrame(branches)

def generate_clients(n=1000):
    print(f"Генерація {n} клієнтів (з 'брудними' даними)...")
    data = []
    for i in range(1, n + 1):
        email = fake.email() if random.random() > 0.12 else None  # 12% NULL
        data.append({
            'client_id': i,
            'full_name': fake.name(),
            'email': email,
            'phone': fake.phone_number(),
            'city': fake.city(),
            'registration_date': fake.date_between(start_date='-3y', end_date='today'),
            'branch_id': random.randint(1, 6)
        })
    df = pd.DataFrame(data)
    # 5% дублікатів
    duplicates = df.sample(frac=0.05)
    df = pd.concat([df, duplicates], ignore_index=True)
    return df

def generate_accounts(n, client_ids):
    print(f"Генерація {n} рахунків...")
    data = []
    for i in range(1, n + 1):
        data.append({
            'account_id': i,
            'client_id': random.choice(client_ids),
            'account_number': fake.iban(),
            'account_type': random.choice(['current', 'savings', 'credit']),
            'balance': round(random.uniform(0, 250000), 2),
            'currency': random.choice(['UAH', 'USD', 'EUR']),
            'opened_date': fake.date_between(start_date='-3y', end_date='today'),
            'is_active': random.choice([True, True, True, False])
        })
    return pd.DataFrame(data)

def generate_transfers(n, account_ids):
    print(f"Генерація {n} переказів...")
    data = []
    for i in range(1, n + 1):
        data.append({
            'transfer_id': str(fake.uuid4()),
            'from_account_id': random.choice(account_ids),
            'to_account_id': random.choice(account_ids),
            'amount': round(random.uniform(50, 50000), 2),
            'transfer_date': fake.date_time_between(start_date='-18m', end_date='now'),
            'status': random.choices(
                ['completed', 'pending', 'failed', 'cancelled'],
                weights=[80, 10, 5, 5]
            )[0],
            'description': fake.sentence(nb_words=6) if random.random() > 0.2 else None
        })
    return pd.DataFrame(data)

def generate_loan_payments(n, client_ids):
    print(f"Генерація {n} платежів по кредитах...")
    data = []
    for i in range(1, n + 1):
        data.append({
            'payment_id': str(fake.uuid4()),
            'client_id': random.choice(client_ids),
            'payment_date': fake.date_time_between(start_date='-18m', end_date='now'),
            'amount': round(random.uniform(500, 30000), 2),
            'loan_type': random.choice(['consumer', 'mortgage', 'auto', 'micro']),
            'status': random.choices(['paid', 'overdue', 'partial'], weights=[70, 20, 10])[0]
        })
    return pd.DataFrame(data)

DB_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/microcredit_dwh"
engine = create_engine(DB_URL)

def load_data_to_dwh(df_branches, df_clients, df_accounts, df_transfers, df_loan_payments):
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()

    print("Завантаження branches...")
    df_branches.to_sql('branches', engine, schema='raw', if_exists='replace', index=False)

    print("Завантаження clients...")
    df_clients.to_sql('clients', engine, schema='raw', if_exists='replace', index=False)

    print("Завантаження accounts...")
    df_accounts.to_sql('accounts', engine, schema='raw', if_exists='replace', index=False)

    print("Завантаження transfers...")
    df_transfers.to_sql('transfers', engine, schema='raw', if_exists='replace', index=False)

    print("Завантаження loan_payments...")
    df_loan_payments.to_sql('loan_payments', engine, schema='raw', if_exists='replace', index=False)

    print("Дані успішно завантажені у схему 'raw'!")

if __name__ == "__main__":
    print("Починаємо генерацію даних для варіанту 7 (Необанк P2P)...")

    df_branches = generate_branches()
    df_clients = generate_clients(1000)

    unique_client_ids = df_clients['client_id'].dropna().unique().tolist()

    df_accounts = generate_accounts(1500, unique_client_ids)
    account_ids = df_accounts['account_id'].tolist()

    df_transfers = generate_transfers(5000, account_ids)
    df_loan_payments = generate_loan_payments(2000, unique_client_ids)

    print(f"\nЗгенеровано:")
    print(f"  branches       → {len(df_branches)}")
    print(f"  clients        → {len(df_clients)}")
    print(f"  accounts       → {len(df_accounts)}")
    print(f"  transfers      → {len(df_transfers)}")
    print(f"  loan_payments  → {len(df_loan_payments)}")

    load_data_to_dwh(df_branches, df_clients, df_accounts, df_transfers, df_loan_payments)