from sqlalchemy import Column, Integer, String, PickleType, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base


class Contract(Base):
    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(Integer, ForeignKey("user.id"), nullablse=False)
    consumer = relationship("User", back_populates="contracts_by_user")
    spec_id = Column(Integer, ForeignKey("spec.id"), nullable=False)
    spec = relationship("Spec", back_populates="contracts_by_spec")
    token = Column(String, nulable=False, unique=True)
    data = Column(PickleType, nullable=False)
