import json

from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()

@app.get("/hello")
def hello():
    return Response(content=json.dumps({"message":"Hello there bitch!"}),status_code=200,media_type="application/json")