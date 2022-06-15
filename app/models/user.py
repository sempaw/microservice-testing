from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    token = Column(String, nullable=False)
    contracts = relationship(
        "Contract", cascade="all,delete-orphan", back_populates="consumer", uselist=True
    )
    specs = relationship(
        "Spec", cascade="all,delete-orphan", back_populates="provider", uselist=True
    )
