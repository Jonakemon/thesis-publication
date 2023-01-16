import logging
import uuid

from sqlalchemy import Column, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class UUIDModel(Base):
    __abstract__ = True
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        try:
            return cls.query.get(uuid.UUID(record_id))
        except ValueError:
            logging.warning(f"Record-ID not a valid UUID: {record_id}")
            return None


def reference_col(
    tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None
):
    """Column that adds primary key foreign key reference.
    Usage: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )


class PersonVerdict(UUIDModel):
    __tablename__ = "person_verdict"
    verdict_id = reference_col("verdict", column_kwargs={"primary_key": False})
    person_id = reference_col("person", column_kwargs={"primary_key": False})
    role = Column(Text, nullable=True)
    verdict = relationship("Verdict", back_populates="people")
    person = relationship("Person", back_populates="verdicts")


class Person(UUIDModel):
    __tablename__ = "person"
    titles = Column(Text, nullable=True)
    initials = Column(Text, nullable=True)
    first_name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=True)
    gender = Column(Text, nullable=True)
    toon_naam = Column(Text, nullable=True, unique=True)
    toon_naam_kort = Column(Text, nullable=True)
    rechtspraak_id = Column(Text, nullable=False, unique=True)
    last_scraped_at = Column(DateTime, nullable=True)
    protected = Column(Boolean, default=False)

    professional_details = relationship("ProfessionalDetail", back_populates="person")
    side_jobs = relationship("SideJob", back_populates="person")
    verdicts = relationship("PersonVerdict", back_populates="person", uselist=False)


class ProfessionalDetail(UUIDModel):
    __tablename__ = "professional_detail"
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    main_job = Column(Boolean, default=False)
    function = Column(Text, nullable=False)
    organisation = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    person_id = reference_col("person", nullable=False)
    person = relationship("Person", lazy="select")
    institution_id = reference_col("institution", nullable=True)
    institution = relationship(
        "Institution", backref="professional_detail", lazy="select"
    )


class SideJob(UUIDModel):
    __tablename__ = "side_job"
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    function = Column(Text, nullable=False)
    place = Column(Text, nullable=True)
    paid = Column(Text, nullable=True)
    organisation_name = Column(Text, nullable=True)
    organisation_type = Column(Text, nullable=True)
    person_id = reference_col("person", nullable=False)
    person = relationship("Person", lazy="select")


class Verdict(UUIDModel):
    __tablename__ = "verdict"
    ecli = Column(Text, nullable=False, unique=True)
    title = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    issued = Column(DateTime, nullable=True)
    zaak_nummer = Column(Text, nullable=True)
    type = Column(Text, nullable=True)
    coverage = Column(Text, nullable=True)
    subject = Column(Text, nullable=True)
    spatial = Column(Text, nullable=True)
    procedure = Column(Text, nullable=True)
    last_scraped_at = Column(DateTime, nullable=True)
    people = relationship("PersonVerdict", back_populates="verdict", uselist=False)
    contains_beslissing = Column(Boolean, nullable=False, default=False)
    beslissings_text = Column(Text, nullable=True)
    institution_id = reference_col("institution", nullable=True)
    institution = relationship("Institution", backref="verdict", lazy="select")
    procedure_type_id = reference_col("procedure_type", nullable=True)
    procedure_type = relationship("ProcedureType", backref="verdict", lazy="select")
    legal_area_id = reference_col("legal_area", nullable=True)
    legal_area = relationship("LegalArea", backref="verdict", lazy="select")


class Institution(Base):
    __tablename__ = "institution"
    id = Column(Text, primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    abbrevation = Column(Text, nullable=True)
    type = Column(Text, nullable=False)
    begin_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)


class ProcedureType(Base):
    __tablename__ = "procedure_type"
    id = Column(Text, primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)


class LegalArea(Base):
    __tablename__ = "legal_area"
    id = Column(Text, primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)
