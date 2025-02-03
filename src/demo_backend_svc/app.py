from fastapi import FastAPI
from demo_backend_svc.routers.signup import router as signup_router

app = FastAPI(debug=True)

app.include_router(signup_router)
