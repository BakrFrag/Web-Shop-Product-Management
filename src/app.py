from fastapi import FastAPI
from apis.users import user_router
from core.logger import setup_logging

setup_logging()
app = FastAPI()
app.include_router(user_router,prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)