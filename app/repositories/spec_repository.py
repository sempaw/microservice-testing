from app.models.spec import Spec
from app.repositories.base_repository import BaseRepository
from app.schemas.spec import SpecCreate, SpecUpdate


class SpecRepository(BaseRepository[Spec, SpecCreate, SpecUpdate]):
    ...


spec = SpecRepository(Spec)
