from typing import Dict
from fastapi import Depends, FastAPI, Response, status, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from datetime import date, datetime
import json
from os.path import exists

app = FastAPI()

security = HTTPBasic()


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


@app.get("/day", status_code=200)
def day_check(name: str, number: int, response: Response):
    weekday = {"monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 7}
    if name.lower() not in weekday or weekday[name.lower()] != number:
        response.status_code = status.HTTP_400_BAD_REQUEST


class Item(BaseModel):
    date: str
    event: str


def check_file_exist():
    if not exists("events.json"):
        file = open("events.json", "w")
        file.write(json.dumps([]))
        file.close()
    file = open("events.json", "r")
    event_list = file.read()
    file.close()
    return json.loads(event_list)


@app.put("/events", status_code=200)
def add_event(item: Item, response: Response):
    try:
        datetime.strptime(item.date, '%Y-%m-%d')
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 0
    event_list = check_file_exist()
    event_list.append({"id": len(event_list),
                       "name": item.event,
                       "date": item.date,
                       "date_added": str(date.today())})
    file = open("events.json", "w")
    file.write(json.dumps(event_list))
    file.close()
    file = open("events.json", "r")
    temp_event_list = file.read()
    file.close()
    event_list = json.loads(temp_event_list)
    return event_list[len(event_list) - 1]


@app.get("/events/{date}", status_code=200)
def check_events(date: str, response: Response):
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 0
    event_list = check_file_exist()
    get_event_list = []
    for record in event_list:
        if record["date"] == date:
            get_event_list.append(record)
    if not get_event_list:
        response.status_code = status.HTTP_404_NOT_FOUND
        return 0
    else:
        return event_list


@app.get("/start", response_class=HTMLResponse)
def index_static():
    return "<h1>The unix epoch started at 1970-01-01</h1>"


good_age = 365 * 16


@app.post("/check", response_class=HTMLResponse)
def age_verification(credentials: HTTPBasicCredentials = Depends(security)):
    try:
        datetime.strptime(credentials.password, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    age = (date.today() - datetime.strptime(credentials.password, '%Y-%m-%d').date()).days
    if age < good_age:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return "<h1>Welcome " + credentials.username + "! You are " + str(age // 365) + "</h1>"


@app.get("/info")
def info(format: str | None = '', user_agent: str | None = Header(default=None)):
    if format == 'json':
        return {"user_agent": user_agent}
    elif format == 'html':
        html_content = '<input type="text" id=user-agent name=agent value="' + user_agent + '">'
        return HTMLResponse(content=html_content, status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@app.get("/save/{string}", status_code=200)
def get_string():
    pass