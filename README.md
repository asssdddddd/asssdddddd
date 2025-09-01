# Prorab Bot

Telegram bot for connecting workers with employers. Built with [aiogram](https://docs.aiogram.dev) and
async SQLAlchemy. The project uses a modular architecture with routers, services and storage layers.

## Running locally

1. Create and fill `.env` based on `.env.example`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run bot in polling mode:
   ```bash
   python -m app.main
   ```

## Tests

Run unit tests with:

```bash
pytest
```
