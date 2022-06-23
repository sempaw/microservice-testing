from app.models.spec import Spec
from app.repositories.base_repository_async import BaseRepositoryAsync
from app.schemas.spec import SpecCreateDB, SpecUpdate


class SpecRepositoryAsync(BaseRepositoryAsync[Spec, SpecCreateDB, SpecUpdate]):
    ...


spec_repo_async = SpecRepositoryAsync(Spec)
