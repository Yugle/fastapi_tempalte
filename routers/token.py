from fastapi import status
import base64
import json
import requests
from conf.config import config
from schemas.base import APIRouter, HTTPException

from schemas.token import TokenResBody
from utils.utils import create_access_token

router = APIRouter(
    prefix="/token",
    tags=["token"]
)


@router.get("/", response_model=TokenResBody)
async def get_token(code: str):
    form = config.sso.dict()
    form["code"] = code
    del form["url_to_get_token"]

    res = requests.post(config.sso.url_to_get_token, data=form)
    resBody = res.json()
    if res.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=res.status_code, message=resBody)

    id_token = resBody["id_token"].split(
        ".")[1].replace("-", "+").replace("_", "/")
    info_dict = json.loads(
        base64.b64decode(id_token).decode("utf-8"))

    resBody["access_token"] = create_access_token(
        {"sub": info_dict["samaccountname"]})
    resBody["nt_account"] = info_dict["samaccountname"]
    resBody["email"] = info_dict["upn"]

    return resBody
