from app.models.spec import Spec
from app.repositories.base_repository import BaseRepository
from app.schemas.spec import SpecCreate, SpecUpdate


class ContractRepository(BaseRepository[Spec, SpecCreate, SpecUpdate]):
    ...


spec = ContractRepository(Spec)
