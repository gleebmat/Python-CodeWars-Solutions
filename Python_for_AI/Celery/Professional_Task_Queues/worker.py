import datetime
import os
import time
import random
from urllib import response
from celery import Celery
from openai import OpenAI
from pydance import BaseModel

from celery.schedules import schedule, crontab

OUTPUT_PATH = "/data/timestamp.txt"


# app = Celery(
#     "random_number",
#     broker=os.getenv("CELERY_BROKER_URL"),
#     backend=os.getenv("CELERY_BACKEND_URL"),
#     broker_connection_retry_on_startup=True,
# )


# @app.task
# def random_number(max_value):
#     time.sleep(5)  # Simulate a time-consuming task
#     return random.randint(0, max_value)

app = Celery(
    "movie_info",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL"),
)


@app.task
def write_timestamp():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "a") as f:
        f.write(datetime.now().isoformat() + "\n")


app.conf.beat_schedule = {
    "timestamp_writer": {
        "task": "worker.write_timestamp",
        "schedule": crontab(minute=1),
    }
}

client = OpenAI()


class Movie(BaseModel):
    title: str
    release_year: int
    direction: str
    genre: str


@app.task
def movie_info(prompt):
    response = client.beta.chat.completions.parse(
        model="gpt-40-mini",
        messages=[
            {"role": "system", "content": "You provide movie information"},
            {"role": "user", "content": prompt},
        ],
        response_format=Movie,
    )

    movie = Movie.model_validate_json(response.choices[0].message.content)

    return movie.model_dump()
