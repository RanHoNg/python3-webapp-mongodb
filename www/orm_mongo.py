# -*- coding: utf-8 -*-

__author__ = 'RanHoNg'

'''
orm_mongo
'''

import logging
import time, uuid
from config import configs

import pymongo
from pymongo import MongoClient

# __db = None

def log(mongo, args=()):
	logging.info('MongoDB: %s' % mongo)

def next_id():
	return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

def create_mongo(**kw):
	logging.info('create MongoClient...')
	# global __db
	client = MongoClient(
		kw.get('host', 'localhost'),
		kw.get('port', 27017)
	)
	__db = client[kw['db']]

	return __db

def get_collection(collection):
	return create_mongo(**configs.db)[collection]

class User(dict):
	collection = get_collection('users')
	def __init__(self, **kw):
		super(User, self).__init__(**kw)
		# self.collection = __db['users']

	def __getattr__(self, key):
		try:
			# return self[key]
			return self.get(key)
		except KeyError as e:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value
		
	@classmethod
	def findAll(cls, where=None, args=None, **kw):
		orderBy = kw.get('orderBy', None)
		limit = kw.get('limit', None)
		rs = []
		if where and not orderBy and not limit :
			rs = get_collection('users').find({where: args[0]})
		if not where and orderBy and limit:
			rs = get_collection('users').find().sort('create_at', pymongo.DESCENDING).limit(limit[1]).skip(limit[0])
		result = []
		for r in rs:
			r.pop('_id')
			result.append(cls(**r))

		return result
			

	@classmethod
	def findNumber(cls, selectField, where=None, args=None):
		return get_collection('users').count()

	@classmethod
	def find(cls, pk):
		print(pk)
		rs = get_collection('users').find_one({"id": pk})

		print('##################################')
		print(rs)
		if rs == None:
			return None
		rs.pop('_id')
		return cls(**rs)

	def save(self):
		post = {
			'id' : self.id,
			'email' : self.email,
			'passwd' : self.passwd,
			'admin' : self.admin,
			'name' : self.name,
			'image' : self.image,
			'create_at' : time.time()
		}
		self.collection.insert_one(post)

	def update(self):
		self.collection.update_one({'id': self.id},{'$set': {
			'email' : self.email,
			'passwd' : self.passwd,
			'admin' : self.admin,
			'name' : self.name,
			'image' : self.image,
			}})

	def remove(self):
		self.collection.delete_one({'id': self.id})


###################################################################

class Blog(dict):
	collection = get_collection('blogs')
	def __init__(self, **kw):
		super(Blog, self).__init__(**kw)
		# self.collection = __db['blogs']

	def __getattr__(self, key):
		try:
			# return self[key]
			return self.get(key)
		except KeyError as e:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value
		
	@classmethod
	def findAll(cls, where=None, args=None, **kw):
		orderBy = kw.get('orderBy', None)
		limit = kw.get('limit', None)

		print(orderBy, limit)
		rs = []
		if where and not orderBy and not limit :
			rs = get_collection('blogs').find({where: args[0]})
		if not where and orderBy and limit:
			# print(isinstance(limit[1], int))
			rs = get_collection('blogs').find().sort('create_at', pymongo.DESCENDING).limit(limit[1]).skip(limit[0])
		print(rs[0])
		result =[]
		for r in rs:
			# r.pop('_id')
			r['_id'] = '_id'
			# print(r)
			b = cls(**r)
			result.append(b)
			# print('$$$', b.content)
			# print('$$$$$', type(b.create_at))
			# print(isinstance(cls(**r), Blog))


		# print(rs[0])
		# result = [cls(**r) for r in rs]
		# print(result[0].content)
		return result
			

	@classmethod
	def findNumber(cls, selectField, where=None, args=None):
		return get_collection('blogs').count()

	@classmethod
	def find(cls, pk):
		rs = get_collection('blogs').find_one({"id": pk})
		if rs == None:
			return None
		rs.pop('_id')
		return cls(**rs)

	def save(self):
		post = {
			'id' : next_id(),
			'user_id' : self.user_id,
			'user_name' : self.user_name,
			'user_image' : self.user_image,
			'name' : self.name,
			'summary' : self.summary,
			'content' : self.content,
			'create_at' : time.time()
		}
		self.collection.insert_one(post)

	def update(self):
		self.collection.update_one({'id': self.id},{'$set': {
			'name' : self.name,
			'summary' : self.summary,
			'content' : self.content,
			}})

	def remove(self):
		self.collection.delete_one({'id': self.id})


###################################################################

class Comment(dict):
	collection = get_collection('comments')
	def __init__(self, **kw):
		super(Comment, self).__init__(**kw)
		# self.collection = __db['comments']

	def __getattr__(self, key):
		try:
			# return self[key]
			return self.get(key)
		except KeyError as e:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value
		
	@classmethod
	def findAll(cls, where=None, args=None, **kw):
		orderBy = kw.get('orderBy', None)
		limit = kw.get('limit', None)
		rs = []
		if where and not orderBy and not limit :
			rs = get_collection('comments').find({where: args[0]})
		if not where and orderBy and limit:
			rs = get_collection('comments').find().sort('create_at', pymongo.DESCENDING).limit(limit[1]).skip(limit[0])
		if where and orderBy and not limit:
			rs = get_collection('comments').find({where: args[0]}).sort('create_at', pymongo.DESCENDING)
		result =[]
		for r in rs:
			r.pop('_id')
			result.append(cls(**r))
		return result
			

	@classmethod
	def findNumber(cls, selectField, where=None, args=None):
		return get_collection('comments').count()

		# return get_collection('comments').find().count()

	@classmethod
	def find(cls, pk):
		rs = get_collection('comments').find_one({"id": pk})
		if rs == None:
			return None
		rs.pop('_id')
		return cls(**rs)

	def save(self):
		post = {
			'id' : next_id(),
			'blog_id' : self.blog_id,
			'user_id' : self.user_id,
			'user_name' : self.user_name,
			'user_image' : self.user_image,
			'content' : self.content,
			'create_at' : time.time()
		}
		self.collection.insert_one(post)

	def update(self):
		self.collection.update_one({'id': self.id},{'$set': {
			'content' : self.content,
			}})

	def remove(self):
		self.collection.delete_one({'id': self.id})