from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import sqlite3
from datetime import datetime


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_db_connection():
    conn = sqlite3.connect('/home/ubuntu/flaskapp/database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    return conn

@app.route('/')
@cross_origin()
def index_render():
    return render_template('index.html')

@app.route('/toggle_state', methods= ['GET'])
@cross_origin()
def update_state():
    conn = get_db_connection()
    cur = conn.cursor()
    states = conn.execute('SELECT * FROM states ORDER BY created DESC LIMIT 1').fetchall()
    state = states[0][2]

    if (state == "locked" or state == "locked_error"):
        cur.execute("INSERT INTO states (state) VALUES (?)",('unlocked',))
    else:
        cur.execute("INSERT INTO states (state) VALUES (?)",('locked',))
    
    conn.commit()
    conn.close()        
   
    return jsonify(status="ok")

@app.route('/error_state', methods= ['GET'])
@cross_origin()
def error_state():
    conn = get_db_connection()
    cur = conn.cursor()
    states = conn.execute('SELECT * FROM states ORDER BY created DESC LIMIT 1').fetchall()
    state = states[0][2]

    if state == "locked":
        cur.execute("INSERT INTO states (state) VALUES (?)",('locked_error',))
    elif state == "unlocked":
        cur.execute("INSERT INTO states (state) VALUES (?)",('unlocked_error',))
    
    conn.commit()
    conn.close()        
   
    return jsonify(status="ok")




@app.route('/read_state', methods= ['GET'])
@cross_origin()
def read_state():
    conn = get_db_connection()
    states = conn.execute('SELECT * FROM states ORDER BY created DESC LIMIT 1').fetchall()
    state = states[0][2]
    msg_time = states[0][1]
    time_now = datetime.now()
    time_delta = time_now - msg_time
    if (state == "locked" and time_delta.total_seconds() < 240):
        state = "ontrip"
    return jsonify(state=state)

@app.route('/analytics')
@cross_origin()
def analytics():
    conn = get_db_connection()
    states = conn.execute('SELECT * FROM states ORDER BY created ASC').fetchall()
    prev_timestamp = 0
    results = []
    for state in states:
        if prev_timestamp == 0:
            prev_timestamp = state[1]
            continue
        if state[2] == "locked":
            time_to_load = state[1]-prev_timestamp
            result = [str(prev_timestamp), "Time to Load", str(time_to_load)]
            results.append(result)
        else:
            time_idling = state[1]-prev_timestamp
            result = [str(prev_timestamp), "Time Between Trips", str(time_idling)]
            results.append(result)
        prev_timestamp = state[1]
    return render_template('analytics.html',results=results)



if __name__ == '__main__':
    app.run()

