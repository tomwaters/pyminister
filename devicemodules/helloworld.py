from basedevice import BaseDevice as BD
from basedevice import View

class Mod(BD):
	def __init__(self, index, type, name, connectionString):
		BD.__init__(self, index, type, name, connectionString)
		self.views.append(View('helloworld_sayhello', 'Say Hello'))
		self.actions.append("Say Hello");
		
	def action(self, command, data):
		if command == 'Say Hello':
			csDict = dict(entry.split('=') for entry in self.conStr.split(';'))
			return "Hello " + csDict['username']
