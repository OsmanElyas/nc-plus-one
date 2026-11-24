from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware


from dotenv import load_dotenv
load_dotenv(".env.dev")

from app.routes.events import events_router
from app.routes.auth import auth_router
from app.routes.user import user_router
from app.routes.organisers import organisers_router

from fastapi.responses import JSONResponse

app = FastAPI(title="Event Booking", debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(events_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(organisers_router, prefix="/api")


@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
def handle_validation_error(request: Request, exc: RequestValidationError):
    missing_fields = [
        error["loc"][-1]
        for error in exc.errors()
        if error["type"] == "missing"
    ]
    if missing_fields:
        return JSONResponse(
            status_code=400,
            content={"error": f"Missing required field: {', '.join(missing_fields)}"},
        )
    return JSONResponse(status_code=400, content={"error": "Invalid request"})


@app.get("/api", status_code=200)
def home():
    return {"message": "NC Plus One API"}


if __name__ == "__main":
    pass