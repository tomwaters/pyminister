import xml.etree.ElementTree as ET

class dm(object):
	devices = {}

	def __init__(self):
		self.readdevices()

	def readdevices(self):
		self.devices.clear()
		tree = ET.parse("devices.xml")
		root = tree.getroot()

		for device in root.getiterator("device"):
			index = root.getchildren().index(device)
			modtype = device.find("type").text
			n = device.find("name").text
			cs = device.find("connectionstring").text
			
			c = getattr(__import__(modtype), "Mod")
			self.devices[str(index)] = c(str(index), n, cs)
	
	def getdevicesjson(self):
		json = '{"devices":['
		for i in range(0, len(self.devices)):
			if i > 0:
				json += ','
			json += self.devices.values()[i].getjson()
		json = json + ']}'
		return json
		
	def getviewsjson(self, deviceid):
		json = ""
		d = self.devices[deviceid]
		if d:
			json = d.getviewsjson()
		return json
	
	def viewcommand(self, deviceid, command, data):
		d = self.devices[deviceid]
		if d:
			return d.viewcommand(command, data)
		else:
			return false

devicemanager = dm()