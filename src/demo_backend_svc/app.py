from fastapi import FastAPI
from demo_backend_svc.routers.signup import router as signup_router
from demo_backend_svc.routers.login import router as login_router
from demo_backend_svc.routers.logout import router as logout_router
from demo_backend_svc.routers.session import router as session_router

app = FastAPI(debug=True)

# Include the signup router with a prefix to expose the endpoint at /auth/signup
app.include_router(signup_router, prefix='/auth/signup')

# Include the login router to expose the /auth/login endpoint
app.include_router(login_router, prefix='/auth/login')

# Include the logout router to expose the /auth/logout endpoint
app.include_router(logout_router, prefix='/auth/logout')

# Include the session router to expose the /auth endpoint
app.include_router(session_router, prefix='/auth')
