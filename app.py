from flask import Flask
import pycas
app = Flask(__name__)

@app.route("/")
def index():
	status, id, cookie = login("https://login.dartmouth.edu", "localhost")
	print "no"
	return "Hello World! %", id

if __name__ == "__main__":
	app.run()