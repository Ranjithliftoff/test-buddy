from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from .base import Base

def uuid_pk() -> Mapped[str]:
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

class Session(Base):
    __tablename__ = "sessions"
    id = uuid_pk()
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    module = Column(String, nullable=False)
    source_type = Column(String, nullable=True)
    source_url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="active")

    plans = relationship("Plan", back_populates="session", cascade="all,delete-orphan")
    scenarios = relationship("Scenario", back_populates="session", cascade="all,delete-orphan")
    artifacts = relationship("Artifact", back_populates="session", cascade="all,delete-orphan")
    runs = relationship("Run", back_populates="session", cascade="all,delete-orphan")
    insights = relationship("Insight", back_populates="session", cascade="all,delete-orphan")
    decisions = relationship("Decision", back_populates="session", cascade="all,delete-orphan")

class Plan(Base):
    __tablename__ = "plans"
    id = uuid_pk()
    session_id = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), index=True, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    title = Column(Text, nullable=False)
    bullets = Column(JSONB, nullable=False)

    session = relationship("Session", back_populates="plans")

class Scenario(Base):
    __tablename__ = "scenarios"
    id = uuid_pk()
    session_id = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), index=True, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    title = Column(Text, nullable=False)
    gherkin = Column(Text, nullable=True)
    meta = Column(JSONB, nullable=True)

    session = relationship("Session", back_populates="scenarios")

class Artifact(Base):
    __tablename__ = "artifacts"
    id = uuid_pk()
    session_id = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), index=True, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    toolchain = Column(String, nullable=False, default="cypress-cucumber")
    feature_path = Column(Text, nullable=False)
    feature_text = Column(Text, nullable=False)
    step_path = Column(Text, nullable=False)
    step_text = Column(Text, nullable=False)

    session = relationship("Session", back_populates="artifacts")

class Run(Base):
    __tablename__ = "runs"
    id = uuid_pk()
    session_id = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), index=True, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    summary = Column(JSONB, nullable=False)

    session = relationship("Session", back_populates="runs")

class Insight(Base):
    __tablename__ = "insights"
    id = uuid_pk()
    session_id = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), index=True, nullable=False)
    run_id = mapped_column(UUID(as_uuid=True), ForeignKey("runs.id"), nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    kind = Column(String, nullable=False)
    text = Column(Text, nullable=False)

    session = relationship("Session", back_populates="insights")
    run = relationship("Run")

class Decision(Base):
    __tablename__ = "decisions"
    id = uuid_pk()
    session_id = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), index=True, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    step = Column(String, nullable=False)   # planner | designer | author | executor | curator
    accepted = Column(Boolean, nullable=False, default=True)
    note = Column(Text, nullable=True)

    session = relationship("Session", back_populates="decisions")
