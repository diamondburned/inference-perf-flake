#!/usr/bin/env python3
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import asyncio
import random
import os
import sys

SLEEP_LOWER_BOUND = float(os.getenv("SLEEP_LOWER_BOUND", 0.0))
SLEEP_UPPER_BOUND = float(os.getenv("SLEEP_UPPER_BOUND", 0.0))

if SLEEP_LOWER_BOUND > SLEEP_UPPER_BOUND:
    print("SLEEP_LOWER_BOUND cannot be greater than SLEEP_UPPER_BOUND", file=sys.stderr)
    sys.exit(1)

app = FastAPI()


@app.api_route("/{tail:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def echo_handler(request: Request):
    method = request.method
    path = request.url.path
    query_params = dict(request.query_params)
    headers = dict(request.headers)

    await asyncio.sleep(random.uniform(SLEEP_LOWER_BOUND, SLEEP_UPPER_BOUND))

    try:
        body_bytes = await request.body()
        body = body_bytes.decode("utf-8") if body_bytes else None
    except Exception as e:
        body = f"Error reading body: {e}"

    response_data = {"method": method, "path": path, "query_params": query_params, "headers": headers, "body": body}
    return JSONResponse(content=response_data)


# To run this server with N workers, you can use gunicorn from the project root:
# gunicorn -w <N> -k uvicorn.workers.UvicornWorker s2:app
#
# For example, to run with 4 workers:
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker s2:app
#
# You can also specify the sleep bounds via environment variables:
# SLEEP_LOWER_BOUND=0.5 SLEEP_UPPER_BOUND=2.5 gunicorn -w 4 -k uvicorn.workers.UvicornWorker s2:app
