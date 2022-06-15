from sqlalchemy import Column, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship

from ..db.base_class import Base


# JSON Field psql
class Contract(Base):
    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    consumer = relationship("User", back_populates="contracts")
    spec_id = Column(Integer, ForeignKey("spec.id"), nullable=False)
    spec = relationship("Spec", back_populates="contracts_by_spec")
    token = Column(String, nullable=False, unique=True)
    data = Column(PickleType, nullable=False)
