import xml.etree.ElementTree as ET

class dm(object):
	devices = {}

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
		
	def deletedevice(self, deviceid):
		del self.devices[deviceid]
		self.writedevices()
	
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