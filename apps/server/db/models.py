# apps/server/db/models.py
from datetime import datetime
import uuid
from sqlalchemy import (
    Column, String, DateTime, Boolean, Text, Enum, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

# ----- enums as plain strings for now -----
STEP_ENUM = ("planner", "designer", "author", "executor", "curator")
MODULE_ENUM = ("uiux", "functional", "api", "smoke", "regression")
SUITE_ENUM = ("smoke", "regression", "generated")
ARTIFACT_KIND_ENUM = ("feature", "steps", "asset")

class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    module: Mapped[str] = mapped_column(String(32), nullable=False)

    # relationships
    decisions: Mapped[list["Decision"]] = relationship("Decision", back_populates="session", cascade="all, delete-orphan")
    plans: Mapped[list["Plan"]] = relationship("Plan", back_populates="session", cascade="all, delete-orphan")
    artifacts: Mapped[list["Artifact"]] = relationship("Artifact", back_populates="session", cascade="all, delete-orphan")
    runs: Mapped[list["Run"]] = relationship("Run", back_populates="session", cascade="all, delete-orphan")

class Decision(Base):
    __tablename__ = "decisions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    step: Mapped[str] = mapped_column(String(24))  # one of STEP_ENUM
    accepted: Mapped[bool] = mapped_column(Boolean, default=True)
    note: Mapped[str | None] = mapped_column(Text)

    session: Mapped["Session"] = relationship("Session", back_populates="decisions")

class Plan(Base):
    __tablename__ = "plans"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255))
    bullets: Mapped[dict] = mapped_column(JSONB, default=dict)  # { bullets: [...] }

    session: Mapped["Session"] = relationship("Session", back_populates="plans")

class Artifact(Base):
    __tablename__ = "artifacts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    kind: Mapped[str] = mapped_column(String(24))  # 'feature' | 'steps' | 'asset'
    toolchain: Mapped[str] = mapped_column(String(64), default="cypress-cucumber")
    feature_path: Mapped[str | None] = mapped_column(String(255))
    step_path: Mapped[str | None] = mapped_column(String(255))
    feature_text: Mapped[str | None] = mapped_column(Text)
    step_text: Mapped[str | None] = mapped_column(Text)

    session: Mapped["Session"] = relationship("Session", back_populates="artifacts")

class Run(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    suite: Mapped[str] = mapped_column(String(24))  # one of SUITE_ENUM
    status: Mapped[str] = mapped_column(String(24), default="queued")  # queued|running|passed|failed
    summary: Mapped[dict | None] = mapped_column(JSONB)

    session: Mapped["Session"] = relationship("Session", back_populates="runs")
