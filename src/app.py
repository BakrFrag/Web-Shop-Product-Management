from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from apis.users import user_router
from apis.products import product_router
from core.logger import setup_logging

setup_logging()
limiter = Limiter(key_func= get_remote_address, default_limits=["10/minute"])
app = FastAPI(root_path="/api")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.include_router(user_router)
app.include_router(product_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)