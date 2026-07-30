from fastapi.templating import Jinja2Templates

from app.core.config import PROJECT_ROOT


templates = Jinja2Templates(directory=PROJECT_ROOT / "app" / "templates")
