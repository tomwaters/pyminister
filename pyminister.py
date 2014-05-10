from flask import Flask, request, render_template, make_response, abort
#import json
from devicemanager import devicemanager

app = Flask(__name__)

@app.route('/')
@app.route('/remote')
def remote():
	return render_template("remote.html")
	
@app.route('/events')
def events():
	return render_template("events.html")	
	
@app.route('/devices')
def devices():
	return render_template("devices.html")

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

@app.route('/json/devices/<string:deviceid>', methods=['GET', 'PUT', 'DELETE'])
def jsondevice(deviceid):
	if request.method == 'GET':
		res = devicemanager.getdevice(deviceid)
		if res == False:
			abort(404)
		else:
			response = make_response(res)
	elif request.method == 'PUT':
		name = request.form['name']
		constring = request.form['constring']
		res = devicemanager.editdevice(deviceid, name, constring)
		if res == False:
			abort(404)
		else:
			response = make_response(res)
	elif request.method == 'DELETE':
		res = devicemanager.deletedevice(deviceid)
		if res == False:
			abort(404)
		else:
			response = make_response(res)
	response.headers['Content-Type'] = 'application/json'
	return response
	
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
			abort(404)
		else:
			response = make_response(r)
			response.headers['Content-Type'] = 'application/json'		
			return response

if __name__ == "__main__":
		app.run(debug=True, host='0.0.0.0')
	
