from typing import Dict
from fastapi import Depends, FastAPI, Response, status, HTTPException, Header
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from datetime import date, datetime
import json
from os.path import exists
import aiosqlite

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


def check_file_exist_2():
    if not exists("strings.json"):
        file = open("strings.json", "w")
        file.write(json.dumps([]))
        file.close()
    file = open("strings.json", "r")
    strings_list = file.read()
    file.close()
    return json.loads(strings_list)


@app.get("/save/{string}", status_code=404)
def get_string(string: str):
    string_list = check_file_exist_2()
    if string in string_list:
        return RedirectResponse("https://delfin7.herokuapp.com/info", status_code=status.HTTP_301_MOVED_PERMANENTLY)


@app.put("/save/{string}", status_code=200)
def put_string(string: str):
    string_list = check_file_exist_2()
    if string not in string_list:
        string_list.append(string)
    file = open("strings.json", "w")
    file.write(json.dumps(string_list))
    file.close()


@app.delete("/save/{string}", status_code=200)
def delete_string(string: str):
    string_list = check_file_exist_2()
    if string in string_list:
        string_list.remove(string)
    file = open("strings.json", "w")
    file.write(json.dumps(string_list))
    file.close()


@app.on_event("startup")
async def startup():
    app.db_connection = await aiosqlite.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    await app.db_connection.close()


@app.get("/suppliers", status_code=200)
async def suppliers():
    lista = []
    cursor = await app.db_connection.execute("SELECT SupplierID, CompanyName FROM Suppliers;")
    suppliers = await cursor.fetchall()
    for supplier in suppliers:
        lista.append({"SupplierID": supplier[0], "CompanyName": supplier[1]})
    return lista


@app.get("/suppliers/{id}", status_code=200)
async def suppliers(id: int):
    lista = []
    cursor = await app.db_connection.execute(f"SELECT * FROM Suppliers WHERE SupplierID = {id}")
    supplier = await cursor.fetchall()
    for info in supplier:
        for details in info:
            lista.append(details)
    print(lista)
    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"SupplierID": lista[0],
            "CompanyName": lista[1],
            "ContactName": lista[2],
            "ContactTitle": lista[3],
            "Address": lista[4],
            "City": lista[5],
            "Region": lista[6],
            "PostalCode": lista[7],
            "Country": lista[8],
            "Phone": lista[9],
            "Fax": lista[10],
            "HomePage": lista[11], }

@app.get("/suppliers/{id}/products", status_code=200)
async def products(id: int):
    lista = []
    cursor = await app.db_connection.execute(f"SELECT Products.ProductID, Products.ProductName, Products.CategoryID, c.CategoryName, Products.Discontinued FROM Products INNER JOIN Categories c ON Products.CategoryID =c.CategoryID  WHERE SupplierID = {id} ORDER BY Products.ProductID DESC ;")
    products = await cursor.fetchall()
    for product in products:
        lista.append({"ProductID": product[0], "ProductName": product[1], "Category": {"CategoryID": product[2], "CategoryName": product[3]}, "Discontinued": int(product[4]),})
    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return lista

class Suppliers(BaseModel):
    CompanyName: str
    ContactName: str = "NULL"
    ContactTitle: str = "NULL"
    Address: str = "NULL"
    City: str = "NULL"
    PostalCode: str = "NULL"
    Country: str = "NULL"
    Phone: str = "NULL"

@app.post("/suppliers", status_code=201)
async def products(suppliers_data: Suppliers):
    lista = []
    cursor = await app.db_connection.execute("SELECT SupplierID FROM Suppliers ;")
    next_id = len(await cursor.fetchall()) + 1
    cursor = await app.db_connection.execute(f"INSERT INTO Suppliers  VALUES  ({next_id}, '{suppliers_data.CompanyName}' , '{suppliers_data.ContactName}' , '{suppliers_data.ContactTitle}' , '{suppliers_data.Address}' , '{suppliers_data.City}' , NULL, '{suppliers_data.PostalCode}' , '{suppliers_data.Country}' , '{suppliers_data.Phone}' ,NULL,NULL);")
    cursor = await app.db_connection.execute(
        f"SELECT SupplierID, CompanyName, ContactName, ContactTitle, Address, City, PostalCode, Country, Phone, Fax, HomePage FROM Suppliers WHERE SupplierID = {next_id};")
    wynik = await cursor.fetchall()
    for info in wynik:
        for details in info:
            lista.append(details)
    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"SupplierID": lista[0],
            "CompanyName": lista[1],
            "ContactName": lista[2],
            "ContactTitle": lista[3],
            "Address": lista[4],
            "City": lista[5],
            "PostalCode": lista[6],
            "Country": lista[7],
            "Phone": lista[8],
            "Fax": lista[9],
            "HomePage": lista[10], }
