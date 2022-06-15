from sqlalchemy import Boolean, Column, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class Spec(Base):
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    provider = relationship("User", back_populates="specs")
    token = Column(String, nullable=False, unique=True)
    is_deprecated = Column(Boolean, nullable=False, default=False)
    data = Column(PickleType, nullable=False)
    contracts_by_spec = relationship(
        "Contract", cascade="all,delete-orphan", back_populates="spec", uselist=True
    )
