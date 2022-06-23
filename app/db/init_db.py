import logging

from sqlalchemy.orm import Session

from app import schemas
from app.core.settings import settings
from app.data import CONTRACTS, SPECS
from app.db import base  # noqa: F401
from app.db.base_class import Base
from app.db.session_async import engine
from app.repositories.contract_repository_async import contract_repo_async
from app.repositories.spec_repository_async import spec_repo_async
from app.repositories.user_repository_async import user_repo_async


logger = logging.getLogger(__name__)


async def init_db(db: Session) -> None:
    # To create tables manually uncomment following line
    Base.metadata.create_all(bind=engine)  # type: ignore
    if settings.FIRST_SUPERUSER:
        user = await user_repo_async.get_by_login(db=db, login=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                login=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER,
                token=settings.FIRST_SUPERUSER,
                is_superuser=True,
            )
            user_id = await user_repo_async.create(db=db, obj_in=user_in)
            user = await user_repo_async.get(db=db, obj_id=user_id)  # type: ignore
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
        if not user.specs:
            for spec in SPECS:
                spec_in = schemas.SpecCreate(
                    provider_id=user.id,
                    token=spec["token"],
                    data=spec["data"],
                    is_deprecated=spec["is_deprecated"],
                )
                await spec_repo_async.create(db=db, obj_in=spec_in)
        if not user.contracts:
            for contract in CONTRACTS:
                contract_in = schemas.ContractCreate(
                    token=contract["token"],
                    data=contract["data"],
                    consumer_id=user.id,
                    spec_id=contract["spec_id"],
                )
                await contract_repo_async.create(db=db, obj_in=contract_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
