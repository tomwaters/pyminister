class BaseDevice(object):
	def __init__(self, id, type, name, connectionString):
		self.views = []
		self.id = id
		self.type = type
		self.name = name
		self.conStr = connectionString or ""
	
	def getname(self):
		return self.name
	
	def getid(self):
		return self.id

	def getjson(self):
		return '{"type": "' + self.type + '", "id":"' + str(self.id) + '", "name":"' + self.name + '", "connectionstring": "' + self.conStr + '"}'

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
		