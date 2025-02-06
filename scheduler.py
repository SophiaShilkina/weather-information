from cities import generator
from db import database_implementation
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database_implementation()
    scheduler.add_job(generator, IntervalTrigger(minutes=15))

    scheduler.start()

    yield

    scheduler.shutdown()
