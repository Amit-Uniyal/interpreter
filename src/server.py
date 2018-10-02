from flask import Flask, jsonify, request
from flask import render_template
import json
from os import getcwd
import subprocess
from DB import DB



app = Flask(__name__)


def run_program(cmd):
	c0, c1 = cmd.split(' ')

	p = subprocess.run([c0, c1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out = p.stdout.decode('utf-8')
	err = p.stderr.decode('utf-8')
	
	if out:
		out = out.split('\n')
	if err:
		err = err.split('\n')
	
	return out, err	


def run_mysql(query):
	db = DB()
	out = db.run_query(query)

	return out, None



def update_file(fname, data):
	try:
		data = data.decode('utf-8')
	except Exception as e:
		pass
	with open(fname, 'w') as fp:
		fp.write(data)
	

@app.route('/')
def index():
	return jsonify("Working")


@app.route('/python')
def py():
	return render_template('index.html')


@app.route('/python', methods=["POST"])
def py_post():
	content = request.form['code']
	fname = 'programs/pyfile.py'
	
	update_file(fname, content)
	cmd = 'python '+fname
	out, err = run_program(cmd)

	return render_template('index.html', content=content, out=out, err=err)


@app.route('/mysql')
def mysql():
	return render_template('index.html')

@app.route('/mysql', methods=["POST"])
def mysql_post():
	content = request.form['code']
	fname = 'programs/query.sql'
	
	update_file(fname, content)

	out, err = run_mysql(content)

	return render_template('index.html', content=content, out=out, err=err)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port='8080')
