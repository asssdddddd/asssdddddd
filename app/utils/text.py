from app.utils.enums import ListingType


def render_listing(data: dict) -> str:
    """Format listing data into a text message."""
    if data.get("type") == ListingType.worker_profile:
        return (
            "Ищу подработку\n"
            f"— Навыки/опыт: {data.get('skills', '-') }\n"
            f"— Локация: {data.get('location', '-') }\n"
            f"— Оплата: {data.get('pay', '-') }\n"
            f"— Контакт: {data.get('contact', '-') }\n"
            "#работник #подработка"
        )
    return (
        f"Нужны рабочие: {data.get('title', '-') }\n"
        f"— Что делать: {data.get('description', '-') }\n"
        f"— Локация: {data.get('location', '-') }\n"
        f"— Сроки: {data.get('deadline', '-') }\n"
        f"— Оплата: {data.get('pay', '-') }\n"
        f"— Контакт: {data.get('contact', '-') }\n"
        "#вакансия #работа"
    )
