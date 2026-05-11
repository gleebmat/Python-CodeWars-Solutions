import time
from celery.result import AsyncResult

from worker import random_number, app, movie_info


# time.sleep(5)

# result_future = random_number.delay(100)
# result = AsyncResult(result_future.id, app=app)

# print("Submetted task")
# print(result.state)

# while True:
#     if result.ready():
#         print(result.get())
#         break
#     else:
#         print(result.state)
#         time.sleep(1)


time.sleep(5)

result_future1 = movie_info.delay("Tell me about the movie Inception")
result_future2 = movie_info.delay("Tell me about the movie The Matrix")


result_future = [result_future1, result_future2]
results = [AsyncResult(rf.id, app=app) for rf in result_future]

while True:
    if not results:
        break
    for r in results:
        if r.ready():
            print(r.get())
            results.remove(r)
    time.sleep(1)
