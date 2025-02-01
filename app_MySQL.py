from flask import Flask, request, jsonify
from Small_Zombie_Ship import Small_Zombie
import mysql.connector

app = Flask(__name__)
mysql_config = {
        'host': 'localhost',
        'user': 'jjbigdick',
        'password': '11111Qaz.',
        'autocommit': True
    }

def initiate_databases ():
    with mysql.connector.connect(**mysql_config) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS user_database")
        cursor.execute("USE user_database")
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(255) UNIQUE NOT NULL,
                            call_limit INT,
                            data_limit FLOAT
                        )''')
        cursor.execute("CREATE DATABASE IF NOT EXISTS blocked_ips_database")
        cursor.execute("USE blocked_ips_database")
        cursor.execute('''CREATE TABLE IF NOT EXISTS blocked_ips (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            ip_address VARCHAR(255) UNIQUE NOT NULL
                        )''')
        cursor.execute("CREATE DATABASE IF NOT EXISTS failed_attempts_database")
        cursor.execute("USE failed_attempts_database")
        cursor.execute('''CREATE TABLE IF NOT EXISTS failed_attempts (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            ip_address VARCHAR(255),
                            failed_time INT
                        )''')
        conn.close()



@app.route('/add_user', methods=['POST'])
def add_user():
    client_ip = request.remote_addr
    if check_ip(client_ip):
        return jsonify({'message': 'Blocked IP address.'}), 403
    else:
        api_key = request.headers.get('X-API-Key')
        if api_key is None or api_key != "ADADQFQQEQAADCXZCZCADADQWEQEQRQRADSAD":
            pending = increment_failed_attempts(client_ip)
            return jsonify({'message': 'Error'}), 400
        else:
            data = request.get_json()
            username = data.get('username')
            call_limit = data.get('call_limit')
            data_limit = data.get('data_limit')
            if username is None:
                return jsonify({'message': 'Username not provided in request.'}), 400
            if call_limit is None and data_limit is None:
                return jsonify({'message': 'Call_limit or Data_limit need to be provided in request.'}), 400
            with mysql.connector.connect(database='user_database', **mysql_config) as conn_user:
                cursor = conn_user.cursor()
                cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
                existing_user = cursor.fetchone()
                if existing_user:
                    current_call_limit, current_data_limit = existing_user[2], existing_user[3]
                    if call_limit is not None:
                        new_call_limit = current_call_limit + call_limit
                    else:
                        new_call_limit = current_call_limit
                    if data_limit is not None:
                        new_data_limit = current_data_limit + data_limit
                    else:
                        new_data_limit = current_data_limit
                    cursor.execute("UPDATE users SET call_limit=%s, data_limit=%s WHERE username=%s",
                                   (new_call_limit, new_data_limit, username))
                    conn_user.commit()
                    return jsonify({'message': f'User credits added successfully.',
                                    'user': username,
                                    'call limit added': call_limit,
                                    'data limit added ': data_limit,
                                    'existing_call_limit': new_call_limit,
                                    'existing_data_limit': new_data_limit
                                    }), 200
                else:
                    if not call_limit:
                        call_limit = 0
                    if not data_limit:
                        data_limit = 0.0
                    cursor.execute("INSERT INTO users (username, call_limit, data_limit) VALUES (%s, %s, %s)",
                                   (username, call_limit, data_limit))
                    return jsonify({'message': f'User operation successfully.',
                                    'user': username,
                                    'call_limit' : call_limit,
                                    'data_limit' : data_limit
                                    }), 200

def check_ip(ip_address):
    with mysql.connector.connect(database='blocked_ips_database', **mysql_config) as conn_blocked_ips:
        cursor_blocked_ips = conn_blocked_ips.cursor()
        cursor_blocked_ips.execute("SELECT * FROM blocked_ips WHERE ip_address=%s", (ip_address,))
        result = cursor_blocked_ips.fetchone()
        return result

def increment_failed_attempts(ip_address):
    with mysql.connector.connect(database='failed_attempts_database', **mysql_config) as conn_failed_attempts:
        cursor_failed_attempts = conn_failed_attempts.cursor()
        cursor_failed_attempts.execute("SELECT * FROM failed_attempts WHERE ip_address=%s", (ip_address,))
        existing_entry = cursor_failed_attempts.fetchone()
        if existing_entry:
            cursor_failed_attempts.execute("UPDATE failed_attempts SET failed_time = failed_time + 1 WHERE ip_address=%s",
                                           (ip_address,))
            if existing_entry[2] >= 100:
                return block_ip(ip_address)
        else:
            cursor_failed_attempts.execute("INSERT INTO failed_attempts (ip_address, failed_time) VALUES (%s, %s)",
                                           (ip_address, 1))
        conn_failed_attempts.commit()
        return True

def block_ip(ip_address):
    with mysql.connector.connect(database='blocked_ips_database', **mysql_config) as conn_blocked_ips:
        cursor = conn_blocked_ips.cursor()
        cursor.execute("INSERT INTO blocked_ips (ip_address) VALUES (%s)", (ip_address,))
        conn_blocked_ips.commit()
        return "Blocking"

@app.route('/flyingzombie', methods=['POST'])
def scrape():
    client_ip = request.remote_addr
    if check_ip(client_ip):
        return jsonify({'message': 'Blocked IP address.'}), 403
    else:
        data = request.get_json()
        identification = data.get('identification')
        username = data.get('username')
        url = data.get('url')
        if username is None:
            pending = increment_failed_attempts(client_ip)
            return
        else:
            if url is None:
                return jsonify({'message': 'Needed a validate url.'}), 400
            else:
                with sqlite3.connect('user_database.db') as conn_user:
                    cursor = conn_user.cursor()
                    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
                    user = cursor.fetchone()
                    if not user:
                        increment_failed_attempts(client_ip)
                        return jsonify({'message': ''}), 400
                    if user:
                        call_limit = user[2]
                        data_limit = user[3]
                        if call_limit <= 0:
                            return jsonify({'message': 'Not enough credits'}), 400
                        # if data_limit <=0:
                        #     return jsonify({'message': 'Not enough call_limit'}), 400
                        if call_limit > 0:
                            call_limit = call_limit - 1
                            with Small_Zombie(port=1416, headless=False, ws_timeout=3,
                                              chrome="/usr/bin/google-chrome") as small_zombie:
                                load = small_zombie.navigate_to(navigate_to=url)
                                if load == True:
                                    html  = small_zombie.retrieve_document()
                                    return jsonify({'HTML': html}), 200




