from faker import Faker
import random
import uuid
import json
from datetime import datetime

fake = Faker()

TRANSACTION_TYPES = [
    "PURCHASE",
    "REFUND",
    "PAYMENT",
    "TRANSFER",
    "WITHDRAWAL",
]

STATUSES = [
    "SUCCESS",
    "FAILED",
    "PENDING",
]

MERCHANT_CATEGORIES = [
    "Grocery",
    "Restaurant",
    "Online Shopping",
    "Transportation",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Retail",
]


def generate_transaction():
    transaction_type = random.choice(TRANSACTION_TYPES)

    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"CUST-{random.randint(1, 100000):06d}",
        "customer_name": fake.name(),
        "transaction_type": transaction_type,
        "merchant": fake.company(),
        "merchant_category": random.choice(MERCHANT_CATEGORIES),
        "amount": round(random.uniform(50, 50000), 2),
        "currency": "PHP",
        "status": random.choice(STATUSES),
        "reference_number": fake.bothify(
            text="TXN-##########"
        ),
        "city": fake.city(),
        "email": fake.email(),
        "timestamp": datetime.now().isoformat(),
    }

    return transaction


if __name__ == "__main__":
    transaction = generate_transaction()

    print(json.dumps(transaction, indent=2))