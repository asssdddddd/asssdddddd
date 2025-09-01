from aiogram import Router

from app.handlers import start, profile, publish_worker, publish_job


def get_router() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(profile.router)
    router.include_router(publish_worker.router)
    router.include_router(publish_job.router)
    return router
