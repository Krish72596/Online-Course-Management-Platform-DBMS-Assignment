from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import auth
from app.routers import course
from app.routers import topic

app = FastAPI()

app.include_router(auth.router)
app.include_router(course.router)
app.include_router(topic.router)


@app.get("/")
def root():
	return RedirectResponse(url="/docs")