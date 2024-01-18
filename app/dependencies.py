from fastapi import Response, HTTPException
import time


count = 0
start_time = time.time()
time_interval = 10
limit = 50


def rate_limit(response: Response) -> Response:
    global start_time, count

    if time.time() >= start_time + time_interval:
        count = 0
        start_time = time.time()

    if count >= limit:
        raise HTTPException(status_code=429, detail={
            "error": "You exceed the limit",
            "timeout": f"{round(start_time + time_interval - time.time(), 2) + 0.01}"
        })

    count += 1
    response.headers["X_app_rate_limit"] = f"{count}:{limit}"
    return Response
