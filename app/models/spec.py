from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Spec(Base):
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    provider = relationship("User", back_populates="specs")
    token = Column(String, nullable=False)
    is_deprecated = Column(Boolean, nullable=False, default=False)
    data = Column(JSON, nullable=False)
    contracts_by_spec = relationship(
        "Contract", cascade="all,delete-orphan", back_populates="spec", uselist=True
    )
