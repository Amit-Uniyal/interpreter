from flask import Flask, jsonify, request
from flask import render_template
import json
from os import system
import subprocess




app = Flask(__name__)

def update_file(fname, data):
	try:
		data = data.decode('utf-8')
	except Exception as e:
		pass
	with open(fname, 'w') as fp:
		fp.write(data)
	
	p = subprocess.run(['python', fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out = p.stdout.decode('utf-8')
	err = p.stderr.decode('utf-8')

	return out, err



@app.route('/')
def index():
	return jsonify("Working")

@app.route('/run', methods=["POST"])
def execute_program():
	content = request.stream.read()
	out, err = update_file('filename.py', content)
	return out

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/interpreter')
def interpreter():
	return render_template('index.html')


@app.route('/interpreter', methods=["POST"])
def interpreter_post():
	content = request.form['code']
	out, err = update_file('filename.py', content)
	out = out.split('\n')
	err = err.split('\n')
	return render_template('index.html', content=content, out=out, err=err)



if __name__ == '__main__':
	app.run(host='0.0.0.0', port='8080')
