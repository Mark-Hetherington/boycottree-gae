'''
Created on 06/08/2013

@author: mark
'''
from google.appengine.ext import db

class Boycott(db.Model):
    name = db.StringProperty()
    content = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    started = db.DateTimeProperty()
    finished = db.DateTimeProperty()