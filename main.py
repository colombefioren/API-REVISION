import json

from fastapi import FastAPI
from starlette.responses import Response, JSONResponse

app = FastAPI()

@app.get("/hello")
def hello(name:str = "Non défini(e)",is_teacher:bool = False):
    if is_teacher is True:
        return JSONResponse({"message" : f"Hello there teacher {name}!"})
    if is_teacher is False:
        if name != "Non défini(e)":
            return JSONResponse({"message": f"Hello there {name}!"})
    return Response(content=json.dumps({"message":"Hello there bitch!"}),status_code=200,media_type="application/json")