from sqlalchemy.orm import Session

from src.database.models import Category
from src.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    model = Category