from sqlalchemy import Column, Integer, String, PickleType, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base


class Spec(Base):
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("user.id"), nullablse=False)
    provider = relationship("User", back_populates="specs")
    token = Column(String, nulable=False, unique=True)
    data = Column(PickleType, nullable=False)
    contracts = relationship(
        "Contract",
        cascade="all,delete-orphan",
        back_populates="contracts_by_spec"
    )
