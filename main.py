from fastapi import FastAPI, HTTPException, Request
from routes.events import events_router
from fastapi.responses import JSONResponse

app = FastAPI(title="Event Booking", debug=True)
app.include_router(events_router)

@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
