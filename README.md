# Rate Limiter 실습 1 (AI 주도 개발 방법론 기반)

## 개요

이 리포지토리는 **AI 주도 개발 방법론**을 바탕으로 **Rate Limiter 구현 및 테스트** 한 실습 1이다. FastAPI + SlowAPI를 사용하여 `/hello` API에 **Rate Limit (1분당 10회)**을 추가하고, 그 기능이 정확히 동작하는지 **테스트 코드 및 결과**를 포함한다. 

---

## 1. 코드

### main.py

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/hello")
@limiter.limit("10/minute")
async def hello(request: Request):
    return {"msg": "hello world"}
``` 


## Execution Result (Rate Limit)

### First 10 requests
HTTP/1.1 200 OK
{"msg":"hello world"}

### After exceeding limit
HTTP/1.1 429 Too Many Requests
{"detail":"Rate limit exceeded. Try again later."}

## Selected Algorithm (Rate Limiting)

This project uses the **Fixed Window Counter** rate limiting algorithm.

### How it works
- A fixed time window is defined (e.g., **1 minute**).
- Each client (identified by IP address) has a request counter.
- If the number of requests within the current window exceeds the limit, the server blocks the request.
- Once the time window expires, the counter resets and requests are allowed again.

### Policy used in this project
- Limit: **10 requests per minute**
- Key: **Client IP address**
- Endpoint: `/hello`

### Reason for choosing this algorithm
The Fixed Window algorithm is simple, easy to implement, and efficient for basic rate limiting requirements.  
It is suitable for this practice project because it clearly demonstrates request blocking behavior (HTTP 429).

### Architecture
```python
  +----------------+
  |    Client      |
  +--------+-------+
           |
           v
  +----------------+
  |  FastAPI App   |
  |                |
  |  /hello Route  |
  +--------+-------+
           |
           v
 +---------------------+
 | SlowAPI Middleware  |
 |   (Rate Limiter)    |
 +---------------------+
           |
           v
  +----------------+
  | Response Layer |
  | 200 or 429     |
  +----------------+
``` 

### Limitation
Fixed Window may allow burst requests at the boundary of two windows (e.g., requests at 59s and 1s).