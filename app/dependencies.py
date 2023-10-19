from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="app/templates")
