import pandas as pd
from faker import Faker
import random
from sqlalchemy import create_engine, text

fake = Faker('uk_UA')
Faker.seed(42)
random.seed(42)

def generate_loan_types():
    print("Генерація типів позик...")
    types = [
        {'loan_type_id': 1, 'type_name': 'Швидкий кредит', 'interest_rate': 45.0, 'max_term_days': 30},
        {'loan_type_id': 2, 'type_name': 'Споживчий кредит', 'interest_rate': 28.5, 'max_term_days': 365},
        {'loan_type_id': 3, 'type_name': 'Кредит на техніку', 'interest_rate': 22.0, 'max_term_days': 730},
        {'loan_type_id': 4, 'type_name': 'Мікропозика', 'interest_rate': 60.0, 'max_term_days': 14},
        {'loan_type_id': 5, 'type_name': 'Кредит під заставу', 'interest_rate': 18.0, 'max_term_days': 1095},
    ]
    return pd.DataFrame(types)

def generate_credit_scores(n=300):
    print(f"Генерація {n} кредитних рейтингів...")
    data = []
    for i in range(1, n + 1):
        score = random.randint(300, 850)
        if score >= 750:
            category = 'Excellent'
        elif score >= 650:
            category = 'Good'
        elif score >= 550:
            category = 'Fair'
        else:
            category = 'Poor'
        data.append({
            'score_id': i,
            'score_value': score,
            'score_category': category,
            'updated_at': fake.date_time_between(start_date='-1y', end_date='now')
        })
    return pd.DataFrame(data)

def generate_borrowers(n=800):
    print(f"Генерація {n} позичальників (з 'брудними' даними)...")
    data = []
    for i in range(1, n + 1):
        email = fake.email() if random.random() > 0.12 else None
        data.append({
            'borrower_id': i,
            'full_name': fake.name(),
            'email': email,
            'phone': fake.phone_number(),
            'city': fake.city(),
            'registration_date': fake.date_between(start_date='-3y', end_date='today'),
            'score_id': random.randint(1, 300)
        })
    df = pd.DataFrame(data)
    duplicates = df.sample(frac=0.05)
    df = pd.concat([df, duplicates], ignore_index=True)
    return df

def generate_issued_loans(n, borrower_ids, loan_type_ids):
    print(f"Генерація {n} виданих кредитів...")
    data = []
    for i in range(1, n + 1):
        issue_date = fake.date_time_between(start_date='-18m', end_date='now')
        term_days = random.choice([14, 30, 90, 180, 365])
        data.append({
            'loan_id': str(fake.uuid4()),
            'borrower_id': random.choice(borrower_ids),
            'loan_type_id': random.choice(loan_type_ids),
            'amount': round(random.uniform(1000, 150000), 2),
            'issue_date': issue_date,
            'term_days': term_days,
            'status': random.choices(
                ['active', 'closed', 'overdue', 'defaulted'],
                weights=[55, 30, 10, 5]
            )[0]
        })
    return pd.DataFrame(data)

def generate_repayments(n, loan_ids):
    print(f"Генерація {n} погашень...")
    data = []
    for i in range(1, n + 1):
        data.append({
            'repayment_id': str(fake.uuid4()),
            'loan_id': random.choice(loan_ids),
            'payment_date': fake.date_time_between(start_date='-18m', end_date='now'),
            'amount': round(random.uniform(200, 25000), 2),
            'payment_method': random.choice(['card', 'cash', 'bank_transfer', 'online']),
            'comment': fake.sentence(nb_words=8) if random.random() > 0.15 else None
        })
    return pd.DataFrame(data)

DB_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/microcredit_dwh"
engine = create_engine(DB_URL)

def load_data_to_dwh(df_loan_types, df_credit_scores, df_borrowers, df_issued_loans, df_repayments):
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()

    print("Завантаження loan_types...")
    df_loan_types.to_sql('loan_types', engine, schema='raw', if_exists='replace', index=False)

    print("Завантаження credit_scores...")
    df_credit_scores.to_sql('credit_scores', engine, schema='raw', if_exists='replace', index=False)

    print("Завантаження borrowers...")
    df_borrowers.to_sql('borrowers', engine, schema='raw', if_exists='replace', index=False)

    print("Завантаження issued_loans...")
    df_issued_loans.to_sql('issued_loans', engine, schema='raw', if_exists='replace', index=False)

    print("Завантаження repayments...")
    df_repayments.to_sql('repayments', engine, schema='raw', if_exists='replace', index=False)

    print("Дані успішно завантажені у схему 'raw'!")

if __name__ == "__main__":
    print("Починаємо генерацію даних для варіанту 10 (Мікрокредитування)...")

    df_loan_types = generate_loan_types()
    df_credit_scores = generate_credit_scores(300)
    df_borrowers = generate_borrowers(800)

    unique_borrower_ids = df_borrowers['borrower_id'].dropna().unique().tolist()
    loan_type_ids = df_loan_types['loan_type_id'].tolist()

    df_issued_loans = generate_issued_loans(4000, unique_borrower_ids, loan_type_ids)
    loan_ids = df_issued_loans['loan_id'].tolist()

    df_repayments = generate_repayments(6000, loan_ids)

    print(f"\nЗгенеровано:")
    print(f"  loan_types     → {len(df_loan_types)}")
    print(f"  credit_scores  → {len(df_credit_scores)}")
    print(f"  borrowers      → {len(df_borrowers)}")
    print(f"  issued_loans   → {len(df_issued_loans)}")
    print(f"  repayments     → {len(df_repayments)}")

    load_data_to_dwh(df_loan_types, df_credit_scores, df_borrowers, df_issued_loans, df_repayments)