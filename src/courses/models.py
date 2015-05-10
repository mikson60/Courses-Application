# -*- coding: utf-8 -*-
"""
    playtech.courses.models
    ~~~~~~~~~~~~~~~~~~~~~~

    Courses models
"""

from ..core import db
from ..helpers import JsonSerializer

teachers_courses = db.Table(
    'teachers_courses',
    db.Column('teacher_id', db.Integer(), db.ForeignKey('courses.id')),
    db.Column('course_id', db.Integer(), db.ForeignKey('teachers.id')))

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    code = db.Column(db.String(100), unique=True)
    capacity = db.Column(db.Integer)
    teachers = db.relationship('Teacher', secondary=teachers_courses,
                            backref=db.backref('courses', lazy='dynamic'))

    def __repr__(self):
        return '<Course %r>' % self.name

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    def __eq__(self, other):
        return (self.first_name == other or
                self.first_name == getattr(other, 'first_name', None))

    def __ne__(self, other):
        return (self.first_name != other and
                self.first_name != getattr(other, 'first_name', None))

    def __repr__(self):
        return '<Teacher %r>' % self.first_name