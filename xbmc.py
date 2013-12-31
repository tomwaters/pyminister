from basedevice import BaseDevice as BD
from basedevice import View
import requests
import json

class Mod(BD):
	def __init__(self, index, name, connectionString):
		BD.__init__(self, index, name, connectionString)
		self.views.append(View('xbmc_remote', 'Remote'))
		self.views.append(View('xbmc_nowplaying', 'Now Playing'))
		
	def viewcommand(self, command, data):
		if 	command == 'remotecommand':
			return self.sendcommand(data)
		elif command == 'nowplaying':
			return self.getplaying()
		
	def sendcommand(self, data):
		csDict = dict(entry.split('=') for entry in self.conStr.split(';'))
		payload = {'request': '{"jsonrpc": "2.0", "id": 1, "method": "Input.' + data + '"}'}
		requests.get(csDict['url'], params=payload)
		return True

	def getplaying(self):
		csDict = dict(entry.split('=') for entry in self.conStr.split(';'))
		payload = {'request': '{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'}
		r = requests.get(csDict['url'], params=payload)
		type = json.loads(r.content)['result'][0]['type']
		
		if type == 'video':
			payload = {'request': '{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "album", "artist", "season", "episode", "duration", "showtitle", "tvshowid", "thumbnail", "file", "fanart", "streamdetails"], "playerid": 1 }, "id": "VideoGetItem"}'}
			r = requests.get(csDict['url'], params=payload)
			result = r.json()['result']#json.loads(r.content)['result']
			print result
			return result
		
		#result = json.loads(str(r.json()['result']))
		#return result['type']
		#
		
		