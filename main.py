#选用FastAPI为后端，Streamlit为前端
from fastapi import FastAPI
import uvicorn
from controller.router import router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True)