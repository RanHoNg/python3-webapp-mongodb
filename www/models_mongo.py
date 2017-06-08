# -*- coding: utf-8 -*-

__author__ = 'RanHoNg'

'''
model_mongo
'''

import time, uuid

from orm_mongo import Model

def next_id():
	return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
	# __table__ = 'users'

	# id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
	# email = StringField(ddl='varchar(50)')
	# passwd = StringField(ddl='varchar(50)')
	# admin = BooleanField()
	# name = StringField(ddl='varchar(50)')
	# image = StringField(ddl='varchar(500)')
	# created_at = FloatField(default=time.time)
	def __init__(self, **kw):
		super(User, self).__init__(**kw)
		self['collection'] = 'users'
		
class User(object):
	def __init__(self, **kw):
		self.id = kw.get('id', next_id)

		