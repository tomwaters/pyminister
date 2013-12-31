import web
import json
from devicemanager import devicemanager

urls = (
    '/', 'index',
		'/device', 'device',
		'/view', 'view',
		'/json/devices', 'devices',
		'/json/views', 'views',
		'/json/viewcommand', 'viewcommand'
)

t_globals = dict()
render = web.template.render('templates/', globals=t_globals)
render._keywords['globals']['render'] = render

class index:
	def GET(self):
		return render.base("")

class device:
	def GET(self):
		return render.base(render.device())

class view:
	def GET(self):
		i = web.input(deviceid=None, viewdid=None)
		if i.deviceid == None or views == "":
			return web.notfound()
		else:
			view = web.template.frender('templates/' + i.viewid + '.html')
			return view()

class viewcommand:
	def POST(self):
		i = web.input(deviceid=None, command=None, data=None)
		r = devicemanager.viewcommand(i.deviceid, i.command, i.data)
		if r == False:
			return web.notfound()
		else:
			return r

class devices:
	def GET(self):
		web.header('Content-Type', 'application/json')
		return devicemanager.getdevicesjson()

class views:
	def GET(self):
		i = web.input(deviceid=None)
		web.header('Content-Type', 'application/json')
		views = devicemanager.getviewsjson(str(i.deviceid))
		if i.deviceid == None or views == "":
			return web.notfound()
		else:
			return views

if __name__ == "__main__":
		app = web.application(urls, globals())
		app.internalerror = web.debugerror
		app.run()
