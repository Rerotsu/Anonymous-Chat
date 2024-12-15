from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="anonymous_chat/pages/templates")


@router.get("/log_reg")
async def login_reg_page(request: Request):
    return templates.TemplateResponse(
        name="login_and_reg.html",
        context={"request": request}
    )
