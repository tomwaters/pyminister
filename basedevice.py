class BaseDevice(object):
	def __init__(self, id, type, name, connectionString):
		self.id = id
		self.type = type
		self.name = name
		self.conStr = connectionString
		self.views = []
	
	def getname(self):
		return self.name
	
	def getid(self):
		return self.id

	def getjson(self):
		return '{"id":"' + str(self.id) + '", "name":"' + self.name + '"}'

	def getviewsjson(self):
		json = '{"views":['
		for i in range(0, len(self.views)):
			if i > 0:
				json += ','
			json += '{"id":"' + self.views[i].id + '", "name":"' + self.views[i].name + '"}'
		json += ']}'
		return json

		
class View(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name
		