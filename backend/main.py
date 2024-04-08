from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, List

import csv
import sqlite3
con = sqlite3.connect("npi.db")


# To create the database with the calculations table, uncomment the lines below
# cur = con.cursor()
# cur.execute("create table calculations(operation, result)")


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def save_in_db(operation:str, result:str) -> None:
    cur = con.cursor()
    cur.execute(f"INSERT INTO calculations VALUES ('{operation}', '{result}')")
    con.commit()

@app.post("/calc/")
async def calc(q: List[str]) -> Union[float, str]:
    result_stack = []
    for item in q:
        if item.isdigit():
            result_stack.append(int(item))
        elif item in ['+', '-', '*', '/']:
            if len(result_stack) < 2:
                result = 'Not enough operands for operation'
                save_in_db(" ".join(q), result)
                return result
            b = result_stack.pop()
            a = result_stack.pop()
            if item == '+':
                result_stack.append(a + b)
            elif item == '-':
                result_stack.append(a - b)
            elif item == '*':
                result_stack.append(a * b)
            elif item == '/':
                result_stack.append(a / b)
        else:
            result = 'Invalid item (check if you have negative integers)'
            save_in_db(" ".join(q), result)
            return result
    
    if len(result_stack) != 1:
        result = 'Invalid expression'
        save_in_db(" ".join(q), result)
        return result
    
    save_in_db(" ".join(q), str(result_stack[0]))
    return result_stack[0]



@app.post("/save-data/")
async def save() -> str:
    with open("data.csv", "w", newline='') as file:
        cur = con.cursor()
        res = cur.execute("SELECT * FROM calculations")
        data = res.fetchall()
        writer = csv.writer(file)
        writer.writerows(data)
    return "well done"