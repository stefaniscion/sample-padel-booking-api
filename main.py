from fastapi import FastAPI
from routes import match, token, book


# http server
app = FastAPI()
app.include_router(token.router)
app.include_router(match.router)
app.include_router(book.router)