from typing import Dict

from fastapi import FastAPI, Response, status

from pydantic import BaseModel

from datetime import date

import json

app = FastAPI()


@app.get("/")
def root():
    return {"start": "1970-01-01"}


class HelloResp(BaseModel):
    msg: str


@app.get("/hello/{name}", response_model=HelloResp)
def read_item(name: str):
    return HelloResp(msg=f"Hello {name}")


@app.get("/method", status_code=200)
def method_get():
    return {"method": "GET"}

@app.put("/method", status_code=200)
def method_put():
    return {"method": "PUT"}

@app.options("/method", status_code=200)
def method_options():
    return {"method": "OPTIONS"}

@app.delete("/method", status_code=200)
def method_delete():
    return {"method": "DELETE"}

@app.post("/method", status_code=201)
def method_post():
    return {"method": "POST"}

class GiveMeSomethingRq(BaseModel):
    first_key: str


class GiveMeSomethingResp(BaseModel):
    received: Dict
    constant_data: str = "python jest super"


@app.post("/dej/mi/coś", response_model=GiveMeSomethingResp)
def receive_something(rq: GiveMeSomethingRq):
    return GiveMeSomethingResp(received=rq.dict())

class HelloResp2(BaseModel):
    name: str
    number: int



@app.get("/day", status_code=200)
def method_get(name: str, number: int, response: Response):
    weekday = {"monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 7}
    if name.lower() not in weekday or weekday[name.lower()] != number:
        response.status_code = status.HTTP_400_BAD_REQUEST





class Item(BaseModel):
    date: str
    event: str

@app.put("/events", status_code=201)
def method_get(item: Item, response: Response):
    try:
        file = open("events.json", "r")
    except:
        file = open("events.json", "w")
        file.write(json.dumps([]))
    finally:
        file.close()
    file = open("events.json", "r")
    temp_event_list = file.read()
    file.close()
    event_list = json.loads(temp_event_list)
    event_list.append({"id": len(event_list),
                       "event": item.event,
                       "date": item.date,
                       "date_added": date.today()})
    file = open("events.json", "w")
    file.write(json.dumps(event_list))
    file.close()
    file = open("events.json", "r")
    temp_event_list = file.read()
    file.close()
    event_list = json.loads(temp_event_list)
    return event_list[len(event_list) - 1]

@app.get("/events", status_code=201)
def method_get(response: Response):
    try:
        file = open("events.json", "r")
    except:
        file = open("events.json", "w")
        file.write(json.dumps([]))
    finally:
        file.close()
    file = open("events.json", "r")
    temp_event_list = file.read()
    file.close()
    event_list = json.loads(temp_event_list)
    return event_list
