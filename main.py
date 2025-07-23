import json
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
    accept_type = request.headers.get("accept")
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