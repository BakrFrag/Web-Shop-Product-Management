import logging
from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from apis import user_router, product_router

logger = logging.getLogger("web_shop")
limiter = Limiter(key_func= get_remote_address, default_limits=["20/minute"])
app = FastAPI(root_path="/api")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.include_router(user_router)
app.include_router(product_router)

if __name__ == "__main__":
    import uvicorn
    logger.info("start listening for web shop application port 8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload = True)