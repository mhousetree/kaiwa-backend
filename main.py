from fastapi import FastAPI
# from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import os
from os.path import join, dirname
from dotenv import load_dotenv

from db import ConnectDb

# class MyPostData(BaseModel):
#     name: str
#     mean: str

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = FastAPI()

origins = [
    os.environ.get("ALLOWED_HOST")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {"message": "hello world"}

@app.get("/expression/")
def read_expression(key: str):
    with ConnectDb() as db:
        try:
            cur = db.execute(f'SELECT * FROM expressions WHERE slug="{key}"').fetchone()
            expression = {
                'id': cur[0],
                'category_id': cur[1] ,
                'slug': cur[2],
                'en': cur[3],
                'ru': cur[4],
                'jp': cur[5],
                'fr': cur[6],
                'it': cur[7]
                }

        except Exception as e:
            raise

    return expression

@app.get("/expressions/")
def read_all_expressions():
    expressions_list = {}

    with ConnectDb() as db:
        try:
            for expression in db.execute('SELECT * FROM expressions ORDER BY id ASC'):
                expressions_list[expression[2]] = {
                    'id': expression[0], 
                    'category_id': expression[1],
                    'slug': expression[2],
                    'en': expression[3],
                    'ru': expression[4],
                    'jp': expression[5],
                    'fr': expression[6],
                    'it': expression[7]
                    }

        except Exception as e:
            raise

    return expressions_list

@app.get("/expressions-in-category")
def read_expressions_in_category(key: str):
    expressions_list = {}

    with ConnectDb() as db:
        try:
            for expression in db.execute(f'SELECT * FROM expressions WHERE category_id="{key}" ORDER BY id ASC'):
                expressions_list[expression[2]] = {
                    'id': expression[0], 
                    'category_id': expression[1],
                    'slug': expression[2],
                    'en': expression[3],
                    'ru': expression[4],
                    'jp': expression[5],
                    'fr': expression[6],
                    'it': expression[7]
                    }

        except Exception as e:
            raise

    return expressions_list



# @app.post("/data/")
# def update_data(post_data: MyPostData):
#     test_data[post_data.name] = post_data.mean
#     return {"message": "post success!!"}