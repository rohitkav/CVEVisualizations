import json
from select import select
from flask import Flask,g,jsonify, render_template,request
import os,psycopg2

app = Flask(__name__)

# @app.before_request
# def before_request_func():
#     g.conn = psycopg2.connect(
#             host="localhost",
#             database="opencve",
#             user=os.environ['DB_USERNAME'],
#             password=os.environ['DB_PASSWORD'])
#     g.conn.autocommit = True
#     # Open a cursor to perform database operations
#     g.cur = g.conn.cursor()

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='opencve',
                            user='opencve',
                            password='opencve')
    return conn
@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/cves-over-time', methods = ['GET'])
def cvetime():
    product_value= request.args.get('product') #extract value for key 'product'
    conn=get_db_connection()
    cur= conn.cursor()
    query = "SELECT LEFT(created_at::text,4) AS year, count(*) FROM cves WHERE vendors::text like '%{}%' GROUP BY LEFT(created_at::text,4)".format(product_value)
    print(query)
    cur.execute(query)
    select_all_vendors = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(select_all_vendors)

# @app.route('/cvssbyvendor')

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/columnchart')
def columnchart():
    return render_template('columnchart.html')

@app.route('/linechart')
def linechart():
    return render_template('linechart.html')

@app.route('/graphselect')

def graphselect():
    return render_template('graphselect.html')

@app.route('/about')

def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
    