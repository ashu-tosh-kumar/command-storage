from pydantic import BaseModel


class Error(BaseModel):
    """Pydantic model to define User Interface application wide errors"""

    name: str
    code: int
    description: str
