def validate_contact(contact: str) -> bool:
    return bool(contact and len(contact) >= 3)


def validate_pay(pay: str) -> bool:
    return bool(pay)
