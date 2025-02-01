from Small_Zombie_Ship import Small_Zombie
from colorlog import ColoredFormatter
import logging
import multiprocessing
import time
from flask import Flask, request, jsonify
import mysql.connector



def Logger(name):
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s - %(white)s%(asctime)s: %(log_color)s%(message)-10s ",
        datefmt=None,
        reset=True,
        log_colors={
        'DEBUG':    'cyan',
        'INFO':     'white',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red',
        },
        style='%'
        )
    if name:
        name = name
    else:
        name = "Default"
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    return logger

logger = Logger("M-Server-Handler")
logger.setLevel(logging.DEBUG)
global_identifier = 0
app = Flask(__name__)
mysql_config = {
        'host': 'localhost',
        'user': 'jjbigdick',
        'password': '11111Qaz.',
        'autocommit': True
    }

worker_queue = multiprocessing.Queue()
result_queue = multiprocessing.Queue()


def worker(id):
    with Small_Zombie(port=1416 + id, headless=False, ws_timeout=3,
                      chrome="/usr/bin/google-chrome") as small_zombie:
        while True:
            if not worker_queue.empty():
                result  = worker_queue.get()
                result[0] = local_identifier
                result[1] = url
                traffic = small_zombie.navigate_to(url= url)
                if traffic:
                    html = small_zombie.retrieve_document()
                    result_queue.put([True, traffic, local_identifier, html])
                else:
                    result_queue.put([False, 0, local_identifier, html])
            else:
                time.sleep(0.1)


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


initiate_databases()

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


@app.route('/add_user', methods=['POST'])
def add_user():


@app.route('/small_zombie', methods=['POST'])
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
                with mysql.connector.connect(database='user_database', **mysql_config) as conn_user:
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
                            global global_identifier
                            if global_identifier == 500000:
                                global_identifier = 1
                                local_identifier = global_identifier
                            else:
                                global_identifier +=1
                                local_identifier = global_identifier
                            worker_queue.put([local_identifier,url])
                            while True:
                                if not result_queue.empty():
                                    result = result_queue.get()
                                    result[0] = identifier
                                    if identifier == local_identifier:
                                        return jsonify({"identifier": local_identifier,
                                                        "user": user,
                                                        "url": url,
                                            'HTML': result[1]}), 200
                                else:
                                    time.sleep(0.1)

if __name__ == "__main__":
    workers = []
    worker_number = 2
    # Two worker processes
    for i in range(1, worker_number+1):
        worker_process = multiprocessing.Process(target=worker, args=(i,))
        worker_process.start()
        workers.append(worker_process)
    logger.debug(f">>> {worker_number} workers started. ")
    app.run(debug=True)


