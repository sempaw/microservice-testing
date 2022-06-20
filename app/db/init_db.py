import logging

from sqlalchemy.orm import Session

from app import repositories, schemas
from app.core.settings import settings
from app.data import CONTRACTS, SPECS
from app.db import base  # noqa: F401
from app.db.base_class import Base
from app.db.session import engine


logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # To create tables manually uncomment following line
    Base.metadata.create_all(bind=engine)  # type: ignore
    if settings.FIRST_SUPERUSER:
        user = repositories.user.get_by_login(db, login=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                login=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER,
                token=settings.FIRST_SUPERUSER,
                is_superuser=True,
            )
            user = repositories.user.create(db, obj_in=user_in)  # noqa: F841
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
                repositories.spec.create(db=db, obj_in=spec_in)
        if not user.contracts:
            for contract in CONTRACTS:
                contract_in = schemas.ContractCreate(
                    token=contract["token"],
                    data=contract["data"],
                    consumer_id=user.id,
                    spec_id=contract["spec_id"],
                )
                repositories.contract.create(db, obj_in=contract_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
