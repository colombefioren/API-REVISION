import json
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root(request : Request):
    accept_type = request.headers.get("Accept")
    key_value = request.headers.get("x-api-key")
    if accept_type != "text/html" and accept_type != "text/plain":
        return Response(content=json.dumps({"message": f"Media type not supported : {accept_type}"}),status_code=400,media_type="application/json")
    if key_value is None or key_value != "12345678":
        return Response(content=json.dumps({"message":"The api key was not recognized!"}),status_code=403,media_type="text/html")
    return Response(content=json.dumps({"message": "Hello World"}),status_code=200,media_type="application/json")

# B-2 je ne sais pas

class Event(BaseModel):
    id : int
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
        events_store.append(event)
    return Response(content=json.dumps({"events": serialized_stored_events()}),status_code=200,media_type="application/json")

@app.put("/events")
def modify_event(list_event: List[Event]):
    for event in list_event:
        found = False
        for i,initial_event in enumerate(events_store):
            if initial_event.id == event.id:
                events_store[i] = event
                found = True
        if not found:
            events_store.append(event)
    return Response(content=json.dumps({"events": serialized_stored_events()}),status_code=200,media_type="application/json")

#PUT est indempotent parce que PUT aura toujours le même effet peut importe combien de fois on l'appelle, contrairement à POST.

@app.delete("/events/{event_id}")
def delete_event(event_id : int):
    for event in events_store:
        if event.id == event_id:
            events_store.remove(event)
            return Response(content=json.dumps({"events":serialized_stored_events()}), status_code=200, media_type="application/json")
    return Response(content=json.dumps({"message":"Event not found"}),status_code=404,media_type="application/json")

@app.patch("/events/{event_id}")
def patch_event(event_id : int,event : Event):
    for event_stored in events_store:
        if event_stored.id == event_id:
            event_stored.name = event.name
            event_stored.description = event.description
            event_stored.start_date = event.start_date
            event_stored.end_date = event.end_date
            return Response(content=json.dumps({"events":serialized_stored_events()}), status_code=200, media_type="application/json")
    return Response(content=json.dumps({"message":"Event not found"}),status_code=404,media_type="application/json")


# PUT pour une modification intégrale tandis que PATCH c'est pour une modification partielle.
@app.get("/events/{event_id}")
def get_specific_event(event_id : int):
    for event in events_store:
        if event.id == event_id:
            return Response(content=json.dumps({"event":event.model_dump()}),status_code=200,media_type="application/json")
    with open("not_found.html","r",encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content,status_code=404,media_type="text/html")

class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

@app.patch("/events/{event_id}")
def update_event(event_id: int, updates: EventUpdate):
    for event in events_store:
        if event.id == event_id:
            # Mise à jour SEULEMENT des champs fournis
            if updates.name is not None:
                event.name = updates.name
            if updates.description is not None:
                event.description = updates.description
            if updates.start_date is not None:
                event.start_date = updates.start_date
            if updates.end_date is not None:
                event.end_date = updates.end_date
            return {"status": "partial_update"}
    return {"error": "Event not found"}, 404

@app.get("{full_path:path}")
def catch_all(full_path: str):
    with open("not_found.html","r",encoding="utf-8") as file:
        html_content=file.read()
    return Response(content=html_content,status_code=404,media_type="text/html")


