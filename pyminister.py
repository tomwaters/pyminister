from flask import Flask, request, render_template, make_response, abort
#import json
from devicemanager import devicemanager

app = Flask(__name__)

@app.route('/')
def root():
	return render_template("base.html")

@app.route('/device')
def device():
	return render_template("device.html")
	
@app.route('/settings')
def settings():
	return render_template("settings.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/view')
def view():
	viewid = request.args.get('viewid')
	if viewid == None:
		abort(404)
	else:
		return render_template(viewid + '.html')

@app.route('/json/modules')
def jsonmodules():
	response = make_response(devicemanager.getmodules())
	response.headers['Content-Type'] = 'application/json'
	return response
	
@app.route('/json/devices', methods=['GET', 'POST'])
def jsondevices():
	if request.method == 'GET':
		response = make_response(devicemanager.getdevices())
	elif request.method == 'POST':
		type = request.form['type']
		name = request.form['name']
		constring = request.form['constring']
		response = make_response(devicemanager.adddevice(type, name, constring))

	response.headers['Content-Type'] = 'application/json'
	return response

@app.route('/json/device', methods=['GET', 'DELETE'])
def jsondevice():
	if request.method == 'GET':
		deviceid = request.args.get('deviceid')
		res = devicemanager.getdevice(deviceid)
		if res == False:
			abort(404)
		else:
			response = make_response(res)
			response.headers['Content-Type'] = 'application/json'
			return response
	elif request.method == 'DELETE':
		deviceid = str(request.form['deviceid'])
		devicemanager.deletedevice(deviceid)
		
		
# class jsondevice:
	# def DELETE(self):
		# inDict = dict(entry.split('=') for entry in web.data().split('&'))
		# deviceid = inDict['deviceid']
		# devicemanager.deletedevice(deviceid)
		

			
@app.route('/json/views')
def jsonviews():
	deviceid = request.args.get('deviceid')
	views = devicemanager.getviews(deviceid)
	if deviceid == None or views == "":
		abort(404)
	else:
		response = make_response(views)
	response.headers['Content-Type'] = 'application/json'
	return response

@app.route('/json/viewcommand', methods=['POST'])
def jsonviewcommand():
	if request.method == 'POST':
		deviceid = str(request.form['deviceid'])
		command = request.form['command']
		data = request.form['data']
		r = devicemanager.viewcommand(deviceid, command, data)
		if r == False:
			abort(400)
		else:
			response = make_response(r)
			response.headers['Content-Type'] = 'application/json'		
			return response

if __name__ == "__main__":
		app.run(debug=True, host='0.0.0.0')
	
