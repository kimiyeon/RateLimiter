from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse

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

@app.get("/hello")
@limiter.limit("10/minute")
async def hello(request: Request):
    return {"msg": "hello world"}

@app.get("/")
async def root():
    return {"status": "ok"}