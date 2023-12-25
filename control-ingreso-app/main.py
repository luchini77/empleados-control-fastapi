from fastapi import FastAPI
import uvicorn

from app.database import Base, engine
from app.views import router

def create_tables():
    Base.metadata.create_all(bind=engine)
create_tables()


app = FastAPI()
app.title = 'App de Ingreso.'

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app',port=8000,reload=True)