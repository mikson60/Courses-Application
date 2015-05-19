# -*- coding: utf-8 -*-
"""
    src.administration.courses
    ~~~~~~~~~~~~~~~~~~

    Course entries controller
"""
from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask.ext.security import roles_accepted
from flask.ext import restful
from flask.ext.restful import reqparse

from ..models import Course, Teacher
from ..core import db

from . import route

bp = Blueprint('courses', __name__, url_prefix='/courses', template_folder='templates/courses')

api = restful.Api(bp, prefix="/")


@route(bp, '/')
def index():
    return render_template("course_list.html")

@route(bp, '/course_details')
def course_details():
    return render_template("course_details.html")

@route(bp, '/teacher_list')
def teacher_list():
    return render_template("teacher_list.html")

@route(bp, '/teacher_details')
def teacher_details():
    return render_template("teacher_details.html")

@route(bp, '/course_add')
def course_add():
	return render_template("course_add.html")

@route(bp, '/teacher_add')
def teacher_add():
    return render_template("teacher_add.html")



class CourseListRes(restful.Resource):
    def __init__(self):
        p = reqparse.RequestParser()
        p.add_argument("count", type=int, location="args", default=15)
        p.add_argument("page", type=int, location="args", default=1)
        self.get_parser = p


    @roles_accepted("ADMIN")
    def get(self):
        args = self.get_parser.parse_args()

        courses = Course.query.paginate(args["page"], args["count"])
        teachers = Teacher.query.paginate(args["page"], args["count"])

        resp = {}

        coursez = {}
        for c in Course.query.all():
            o = {}
            o["id"] = c.id
            o["name"] = c.name
            o["code"] = c.code
            o["teachers"] = {t.id:t.first_name for t in c.teachers}
            o["capacity"] = c.capacity
            coursez[c.id] = o

        resp["rows"] = coursez
        resp["teachers"] = [{k:getattr(d, k) for k in ('id', 'first_name', 'last_name')} for d in teachers.items]
        resp["total"] = courses.total
        resp["pages"] = courses.pages

        return jsonify(resp)


class CourseRes(restful.Resource):
    def __init__(self):
        p = reqparse.RequestParser()
        p.add_argument("id", type=int, location="args")
        self.get_parser = p

        p2 = reqparse.RequestParser()
        p2.add_argument("course_id", type=int, required=True)
        p2.add_argument("action", type=str, required=True)
        p2.add_argument("teacher_id", type=int)
        self.assign_teacher_parser = p2

    @roles_accepted("ADMIN")
    def get(self):
        args = self.get_parser.parse_args()

        resp = {}
        teachers = {}
        for c in Course.query.all():
            if(c.id == args["id"]):
                o = {}
                o["id"] = c.id
                o["name"] = c.name
                o["code"] = c.code
                o["teachers"] = {t.id:t.first_name for t in c.teachers}
                o["capacity"] = c.capacity
                resp["course"] = o

        return jsonify(resp)

    @roles_accepted("ADMIN")
    def delete(self):
    	args = self.get_parser.parse_args()

    	item = Course.query.filter(Course.id==args["id"]).first_or_404()
    	print(item)
    	db.session.delete(item)
    	db.session.commit()

    	resp = {'status': 'OK'}
    	return jsonify(resp)

    #####################
    @roles_accepted("ADMIN")
    def post(self):
        args = self.assign_teacher_parser.parse_args()
        print(args)

        act = args["action"]
        resp = {}

        if act == "assignTeacher":
            course = Course.query.filter(Course.id==args["course_id"]).first_or_404()
            teacher = Teacher.query.filter(Teacher.id==args["teacher_id"]).first_or_404()



            if teacher not in course.teachers:
                course.teachers.append(teacher)
                db.session.commit()

            resp["teacher"] = teacher.first_name

        elif act == "removeTeacher":
            course = Course.query.filter(Course.id==args["course_id"]).first_or_404()
            teacher = Teacher.query.filter(Teacher.id==args["teacher_id"]).first_or_404()
            if teacher in course.teachers:
                course.teachers.remove(teacher)
                db.session.commit()
        return jsonify(resp)



class TeacherListRes(restful.Resource):
    def __init__(self):
        p = reqparse.RequestParser()
        p.add_argument("count", type=int, location="args", default=15)
        p.add_argument("page", type=int, location="args", default=1)
        self.get_parser = p

    @roles_accepted("ADMIN")
    def get(self):
        args = self.get_parser.parse_args()

        teachers = Teacher.query \
                    .paginate(args["page"], args["count"])

        resp = {}
        resp["rows"] = [{k:getattr(d, k) for k in ('id', 'first_name', 'last_name')} for d in teachers.items]

        resp["total"] = teachers.total
        resp["pages"] = teachers.pages

        return jsonify(resp)



class TeacherRes(restful.Resource):
    def __init__(self):
        p = reqparse.RequestParser()
        p.add_argument("id", type=int, location="args")
        self.get_parser = p

    @roles_accepted("ADMIN")
    def get(self):
        args = self.get_parser.parse_args()

        teachers = Teacher.query.filter(Teacher.id==args["id"]).first_or_404()

        resp = {}
        resp["teacher"] = { k : getattr(teachers, k) for k in ('id', 'first_name', 'last_name') }
        return jsonify(resp)

    @roles_accepted("ADMIN")
    def delete(self):
    	args = self.get_parser.parse_args()

    	item = Teacher.query.filter(Teacher.id==args["id"]).first_or_404()
    	db.session.delete(item)
    	db.session.commit()

    	resp = {'status': 'OK'}
    	return jsonify(resp)


class CourseAddRes(restful.Resource):
    def __init__(self):
       p = reqparse.RequestParser()
       p.add_argument("course_name", type=str) #MIKS location='args' EEMALDAMINE TÖÖLE PANI ASJA?
       p.add_argument("course_code", type=str)
       p.add_argument("course_capacity", type=int)

       self.post_parser = p

    @roles_accepted("ADMIN")
    def get(self):
        return jsonify(resp)

    @roles_accepted("ADMIN")
    def post(self):
        args = self.post_parser.parse_args()

        course_name = args["course_name"]
        course_code = args["course_code"]
        course_capacity = args["course_capacity"]

        print(course_name, course_code, course_capacity)
        if (course_name is not None) and (course_code is not None) and (course_capacity is not None):
            db.session.add(Course(name=course_name, code=course_code, capacity=course_capacity))
            db.session.commit()

class TeacherAddRes(restful.Resource):
    def __init__(self):
       p = reqparse.RequestParser()
       p.add_argument("t_first_name", type=str)
       p.add_argument("t_last_name", type=str)

       self.post_parser = p

    @roles_accepted("ADMIN")
    def get(self):
        return jsonify(resp)

    @roles_accepted("ADMIN")
    def post(self):
        args = self.post_parser.parse_args()

        t_first_name = args["t_first_name"]
        t_last_name = args["t_last_name"]

        print(t_first_name, t_last_name)
        if (t_first_name is not None) and (t_last_name is not None):
            db.session.add(Teacher(first_name=t_first_name, last_name=t_last_name))
            db.session.commit()


api.add_resource(CourseListRes, "course/list")
api.add_resource(CourseRes, "course")

api.add_resource(TeacherListRes, "teacher/list")
api.add_resource(TeacherRes, "teacher")

api.add_resource(CourseAddRes, "course/add")
api.add_resource(TeacherAddRes, "teacher/add")
