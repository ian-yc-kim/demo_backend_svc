from fastapi import FastAPI
from demo_backend_svc.routers.signup import router as signup_router

app = FastAPI(debug=True)

# Include the signup router with a prefix to expose the endpoint at /signup
app.include_router(signup_router, prefix='/signup')
