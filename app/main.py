import pymysql
from flask import Flask, request, jsonify, render_template
from flaskext.mysql import MySQL 
#from flask_restful import Resource, Api

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'alexa'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

#-----------------------------------Add UserName and Command----------------------------------------#
@app.route('/add/<username>/<command>', methods=['POST'])
def add_user(username, command):
	try:
		if request.method == 'POST':
			sql = "INSERT INTO records(UserName, Command) VALUES(%s, %s)"
			data = (username, command)
			mydb = mysql.connect()
			mycursor = mydb.cursor()
			mycursor.execute(sql, data)
			mydb.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		mycursor.close() 
		mydb.close()

#------------------------------------------Echo Latest Entry----------------------------------------# 
@app.route('/list', methods=['GET'])
def users():
	try: 
		mydb = mysql.connect()
		mycursor = mydb.cursor(pymysql.cursors.DictCursor)
		mycursor.execute("SELECT * FROM records ORDER BY RecordID DESC LIMIT 1;")
		rows = mycursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		mycursor.close() 
		mydb.close()

if __name__ == "__main__":
    app.run(debug=True, port=8050)