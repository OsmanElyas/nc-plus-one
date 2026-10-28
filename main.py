from fastapi import FastAPI, HTTPException, Request
from app.routes.events import events_router
from app.routes.auth import auth_router
from fastapi.responses import JSONResponse

app = FastAPI(title="Event Booking", debug=True)
app.include_router(events_router)
app.include_router(auth_router)

@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


if __name__ == "__main":
    pass