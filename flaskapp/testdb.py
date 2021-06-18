import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES)
    return conn


def main():
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
    print results[0]

if __name__ == '__main__':
  main()

