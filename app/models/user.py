from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..db.base_class import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    token = Column(String, nullable=False)
    contracts = relationship("Contract", backref="user")
    specs = relationship("Spec", backref="user")
    # contracts = relationship(
    #     "Contract",
    #     cascade="all,delete-orphan",
    #     back_populates="consumer",
    #     uselist=True
    # )
    # specs = relationship(
    #     "Spec",
    #     cascade="all,delete-orphan",
    #     back_populates="spec",
    #     uselist=True
    # )
