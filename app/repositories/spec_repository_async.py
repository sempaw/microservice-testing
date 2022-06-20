from app.models.spec import Spec
from app.repositories.base_repository_async import BaseRepositoryAsync
from app.schemas.spec import SpecCreate, SpecUpdate


class SpecRepositoryAsync(BaseRepositoryAsync[Spec, SpecCreate, SpecUpdate]):
    ...


spec = SpecRepositoryAsync(Spec)
