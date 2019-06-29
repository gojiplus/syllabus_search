from . import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Sequence, ForeignKey, Table, \
    Integer, SmallInteger, Text, Date, Enum, Float, String
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR

__all__ = [
    'Course',
    'Session',
    'Assessment',
    'Instructor',
    'Category'
]

Terms = ['Fall', 'Winter', 'Spring', 'Summer']


course_category = Table(
    'course_category', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


course_instructor = Table(
    'course_instructor', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('instructor_id', Integer, ForeignKey('instructors.id'))
)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, Sequence('categories_seq'), primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    courses = relationship('Course', secondary=course_category,
                           back_populates='categories')


class Instructor(Base):
    __tablename__ = 'instructors'

    id = Column(Integer, Sequence('instructors_seq'), primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    degrees = Column(ARRAY(Text))
    courses = relationship('Course', secondary=course_instructor,
                           back_populates='instructors')


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, Sequence('courses_seq'), primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    full_name = Column(Text, nullable=False, unique=True)
    year = Column(SmallInteger)
    term = Column(Enum(*Terms, name='term'))
    faculty = Column(Text)
    credits = Column(Float)
    outcomes = Column(ARRAY(Text))
    tas = Column(ARRAY(Text))
    num_sessions = Column(Integer, default=0)
    num_assessments = Column(Integer, default=0)
    document = Column(TSVECTOR)
    sessions = relationship('Session', back_populates='course')
    assessments = relationship('Assessment', back_populates='course')
    categories = relationship('Category', secondary=course_category,
                              back_populates='courses', lazy='joined')
    instructors = relationship('Instructor', secondary=course_instructor,
                               back_populates='courses', lazy='joined')


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, Sequence('sessions_seq'), primary_key=True)
    title = Column(Text)
    section = Column(String(128))
    location = Column(String(128))
    guest_teachers = Column(ARRAY(Text))
    type = Column(String(32))
    length = Column(SmallInteger)
    date = Column(Date)
    teaching_strategies = Column(ARRAY(Text))
    instruction_type = Column(String(20))
    topics = Column(ARRAY(Text))
    objectives = Column(ARRAY(Text))
    document = Column(TSVECTOR)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='sessions')


class Assessment(Base):
    __tablename__ = 'assessments'

    id = Column(Integer, Sequence('assessments_seq'), primary_key=True)
    title = Column(Text)
    type = Column(String(20))
    format = Column(String(50))
    weight = Column(SmallInteger)
    cumulative = Column(String(20))
    due_date = Column(Date)
    objectives = Column(ARRAY(Text))
    document = Column(TSVECTOR)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='assessments')
