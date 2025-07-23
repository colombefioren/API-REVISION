import json
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, RedirectResponse

app = FastAPI()

@app.get("/")
def redirection():
    return RedirectResponse(url="/hello",status_code=302)

@app.get("/hello")
def hello(request : Request,name:str = "Non défini(e)",is_teacher:bool = False):
    accept_type = request.headers.get("Accept")
    if accept_type not in ("text/plain","text/html"):
        return "You won't see shit bitch!"
    else:
        if is_teacher is True:
            return JSONResponse({"message" : f"Hello there teacher {name}!"})
        else:
            if name != "Non défini(e)":
                return JSONResponse({"message": f"Hello there {name}!"})
            return Response(content=json.dumps({"message":"Hello there bitch!"}),status_code=200,media_type="application/json")


@app.get("/secret")
def verify_user(request : Request):
    user_secret_key = request.headers.get("Authorization")
    if user_secret_key == "my_secret_key":
        return JSONResponse({"message" : "You entered the right key!"},200)
    return JSONResponse({"message" : f"{user_secret_key} is not the right key! You are not allowed here!"},403)

class Code(BaseModel):
    secret_code: int

@app.post("/code")
def verify_code(code: Code):
    if len(str(code.secret_code)) == 4:
        return JSONResponse({"message" : f"You entered the right code of 4 length : {code.secret_code}!"},200)
    return JSONResponse({"message" : f"{code.secret_code} is not the right code! You are not allowed here!"},400)

@app.get("/welcome")
def welcome(request: Request):
    accept_type = request.headers.get("Accept")
    key_value = request.headers.get("x-api-key")
    if not ("text/plain" in accept_type or "text/plain" in accept_type):
        return Response(content=json.dumps({"message" : f"Media type not supported : {accept_type}"}),status_code=400,media_type="application/json")
    with open("welcome.html","r",encoding="utf-8") as file:
        html_content=file.read()
        if key_value != "12345678":
            return Response(content=json.dumps({"message":"The api key was not recognized!"}),status_code=403,media_type="text/html")
        return Response(content=html_content,status_code=200,media_type="text/html")


class Event(BaseModel):
    name: str
    description: str
    start_date : str
    end_date : str

events_store: List[Event] = []

def serialized_stored_events():
    events_converted = []
    for event in events_store:
        events_converted.append(event.model_dump())
    return events_converted

@app.get("/events")
def get_event():
    return Response(content=json.dumps({"events" : serialized_stored_events()}),status_code=200,media_type="application/json")

@app.post("/events")
def post_event(list_event : List[Event]):
    for event in list_event:
        for initial_event in events_store:
            if initial_event.name == event.name:
                return Response(content=json.dumps({"message":"An event with the same name already exists!"}),status_code=400,media_type="application/json")
        events_store.append(event)
    return Response(content=json.dumps({serialized_stored_events()}),status_code=200,media_type="application/json")


@app.get("{full_path:path}")
def catch_all(full_path: str):
    with open("not_found.html","r",encoding="utf-8") as file:
        html_content=file.read()
        return Response(content=html_content,status_code=404,media_type="text/html")


