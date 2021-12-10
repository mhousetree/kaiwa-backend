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
                'cn': cur[3],
                'en': cur[4],
                'es': cur[5],
                'ru': cur[6],
                'jp': cur[7],
                'de': cur[8],
                'fr': cur[9],
                'kr': cur[10],
                'it': cur[11],
                'tr': cur[12],
                'idn': cur[13],
                'gr': cur[14]
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
                    'cn': expression[3],
                    'en': expression[4],
                    'es': expression[5],
                    'ru': expression[6],
                    'jp': expression[7],
                    'de': expression[8],
                    'fr': expression[9],
                    'kr': expression[10],
                    'it': expression[11],
                    'tr': expression[12],
                    'idn': expression[13],
                    'gr': expression[14]
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
                    'cn': expression[3],
                    'en': expression[4],
                    'es': expression[5],
                    'ru': expression[6],
                    'jp': expression[7],
                    'de': expression[8],
                    'fr': expression[9],
                    'kr': expression[10],
                    'it': expression[11],
                    'tr': expression[12],
                    'idn': expression[13],
                    'gr': expression[14]
                    }

        except Exception as e:
            raise

    return expressions_list



# @app.post("/data/")
# def update_data(post_data: MyPostData):
#     test_data[post_data.name] = post_data.mean
#     return {"message": "post success!!"}