from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import psycopg2
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT')
    )

@app.route('/api/message', methods=['GET'])
def get_message():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT message FROM greetings ORDER BY id DESC LIMIT 1;")
        message = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/message', methods=['POST'])
def post_message():
    try:
        data = request.get_json()
        message = data.get('message')
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO greetings (message) VALUES (%s);", (message,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'Message added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
