# -*- coding: utf-8 -*-
"""
    veoautod.users.forms
    ~~~~~~~~~~~~~~~~~~~~~

    User forms
"""

from flask_wtf import Form
from wtforms import TextField, TextAreaField, RadioField
from wtforms.validators import Required, Length, Email

__all__ = ['NewQueryForm']


class NewQueryForm(Form):
    name = TextField('Nimi', validators=[Required(), Length(max=100)])
    email = TextField('E-mail', validators=[Required(), Email()])
    location = RadioField('Asukoht', choices=[('value_one','Tartu'),('value_two','Tallinn'), ('value_three','Pärnu')])
    query_text = TextAreaField('Taotlus', validators=[Required(), Length(max=1000)])