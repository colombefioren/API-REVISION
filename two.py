import json
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

app = FastAPI()


@app.get("/")
def read_root(request : Request):
    key_value = request.headers.get("x-api-key")
    if key_value != "SECURE2025":
        return JSONResponse({"message" : "API key invalid!"},403)
    return JSONResponse({"message" : "Hello World"},200)


class Event(BaseModel):
    name : str
    description : str
    start_date : str
    end_date : str

events_store : List[Event] = []

def serialized_stored_events():
    converted_events = []
    for event in events_store:
        converted_events.append(event.model_dump())
    return converted_events

@app.get("/events")
def get_events():
    return Response(content=json.dumps({"events" : serialized_stored_events()}),status_code=200,media_type="application/json")

@app.post("/events")
def post_event(list_event : List[Event]):
    for event in list_event:
        found = False
        for original_event in events_store:
            if event.name == original_event.name:
                found = True
        if not found:
            events_store.append(event)
    return Response(content=json.dumps({"events": serialized_stored_events()}),status_code=200,media_type="application/json")

@app.put("/events")
def modify_event(list_event: List[Event]):
    for event in list_event:
        found = False
        for i,initial_event in enumerate(events_store):
            if initial_event.name == event.name:
                events_store[i] = event
                found = True
        if not found:
            events_store.append(event)
    return Response(content=json.dumps({"events": serialized_stored_events()}),status_code=200,media_type="application/json")

@app.delete("/events/{event_name}")
def delete_event(event_name : str):
    for event in events_store:
        if event.name == event_name:
            events_store.remove(event)
            return Response(content=json.dumps({"events":serialized_stored_events()}), status_code=200, media_type="application/json")
    return Response(content=json.dumps({"message":"Event not found"}),status_code=404,media_type="application/json")

@app.get("/events/date/{day}")
def get_events_by_day(day : str):
    events_by_day = []
    for event in events_store:
        if event.start_date.split("-")[2] == day or event.end_date.split("-")[2] == day:
            events_by_day.append(event.model_dump())
    return Response(content=json.dumps({"events": events_by_day}),status_code=200,media_type="application/json")

@app.get("/events/by_date/{day}")
def get_events_by_date(day : str,month : str):
    events_by_date = []
    normalized_day = day.zfill(2)
    normalized_month = month.zfill(2)
    for event in events_store:
        event_start_month = event.start_date.split("-")[1]
        event_end_month = event.end_date.split("-")[1]
        event_start_day = event.start_date.split("-")[2]
        event_end_day = event.end_date.split("-")[2]
        if (event_start_day == normalized_day or event_end_day == normalized_day) and (event_start_month == normalized_month or event_end_month == normalized_month):
            events_by_date.append(event.model_dump())
    return Response(content=json.dumps({"events_filtered": events_by_date}),status_code=200,media_type="application/json")

@app.get("/events/names/day/{day}")
def get_event_names_by_day(day: str):
    day = day.zfill(2)
    names = []
    for event in events_store:
        start_day = event.start_date.split("-")[2]
        end_day = event.end_date.split("-")[2]
        if start_day == day or end_day == day:
            names.append(event.name)  # Just the string name
    return {"event_names": names}
