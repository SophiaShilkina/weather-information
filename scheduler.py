from service.cities import generator
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(generator, IntervalTrigger(minutes=15))

    scheduler.start()
    yield
    scheduler.shutdown()
