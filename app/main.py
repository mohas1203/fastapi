from fastapi import FastAPI
from .routers import post, user, auth, vote
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


# Initializing fastapi
app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setting up routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Gateway route
@app.get("/", response_class=HTMLResponse)
def gateway():
    return "<h1><u>API ACCESS GATEWAY</u></h1>"
