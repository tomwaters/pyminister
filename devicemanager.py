import sys, os
import xml.etree.ElementTree as ET

class dm(object):
	devices = {}
	sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

	def __init__(self):
		self.readdevices()

	def readdevices(self):
		self.devices.clear()
		tree = ET.parse('devices.xml')
		root = tree.getroot()

		for device in root.getiterator('device'):
			index = root.getchildren().index(device)
			modtype = device.find('type').text
			n = device.find('name').text
			cs = device.find('connectionstring').text
			
			c = getattr(__import__(modtype), "Mod")
			self.devices[str(index)] = c(str(index), modtype, n, cs)

	def writedevices(self):
		ds = ET.Element('devices')
		for devid in self.devices:
			d = ET.SubElement(ds, 'device')
			n = ET.SubElement(d, 'name')
			t = ET.SubElement(d, 'type')
			c = ET.SubElement(d, 'connectionstring')
			n.text = self.devices[devid].name
			t.text = self.devices[devid].type
			c.text = self.devices[devid].conStr
		tree = ET.ElementTree(ds)
		tree.write('devices.xml')
		
	def adddevice(self, type, name, cstring):
		c = getattr(__import__(type), "Mod")
		index = len(self.devices) + 1
		self.devices[str(index)] = c(str(index), type, name, cstring)
		self.writedevices()
		return self.devices[str(index)].getjson()
	
	def editdevice(self, deviceid, name, cstring):
		d = self.devices[devicesid]
		if d:
			self.devices[str(index)].edit(name, cstring)
			self.writedevices()
			return self.devices[str(index)].getjson()
		else:
			return False
		
	def deletedevice(self, deviceid):
		d = self.devices[deviceid]
		if d:
			self.devices.pop(deviceid)
			self.writedevices()
			return "{}"
		else:
			return False

	def getmodules(self):
		json = ''
		for module in os.listdir('modules'):
			if module.endswith('.py'):
				if len(json) > 0:
					json += ','
				json += '{"name":"' + module[:-3] + '"}'
		json = '{"modules":[' + json + ']}'
		return json
		
	def getdevices(self):
		json = '{"devices":['
		for i in range(0, len(self.devices)):
			if i > 0:
				json += ','
			json += self.devices.values()[i].getjson()
		json = json + ']}'
		return json
	
	def getdevice(self, deviceid):
		d = self.devices[deviceid]
		if d:
			return d.getjsonfull()
		else:
			return False

	def getviews(self, deviceid):
		json = ""
		d = self.devices[deviceid]
		if d:
			json = d.getviewsjson()
		return json
	
	def viewcommand(self, deviceid, command, data):
		d = self.devices[deviceid]
		if d:
			return d.viewcommand(command, data) or "{}"
		else:
			return False

devicemanager = dm()