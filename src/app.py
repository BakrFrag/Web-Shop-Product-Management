from fastapi import FastAPI
from apis.users import user_router
from apis.prtoducts import product_router
from core.logger import setup_logging

setup_logging()
app = FastAPI(root_path="/api")
app.include_router(user_router)
app.include_router(product_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)