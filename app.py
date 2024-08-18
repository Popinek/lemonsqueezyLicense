from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('licenses.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS licenses (
        license_key TEXT PRIMARY KEY,
        hwid TEXT
    )
    ''')
    conn.commit()
    conn.close()


@app.route('/validate', methods=['POST'])
def validate_license():
    data = request.json
    license_key = data.get('license_key')
    hwid = data.get('hwid')

    if not license_key or not hwid:
        return jsonify({'status': 'error', 'message': 'License key and HWID are required'}), 400

    conn = sqlite3.connect('licenses.db')
    cursor = conn.cursor()

    # Check if the license key exists in the database
    cursor.execute('SELECT hwid FROM licenses WHERE license_key = ?', (license_key,))
    result = cursor.fetchone()

    if result is None:
        # If the license key doesn't exist, add it with the provided HWID
        cursor.execute('INSERT INTO licenses (license_key, hwid) VALUES (?, ?)', (license_key, hwid))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'License key and HWID added successfully'})

    stored_hwid = result[0]

    # If the HWID matches, allow access
    if stored_hwid == hwid:
        conn.close()
        return jsonify({'status': 'success', 'message': 'License validated successfully'})

    # If the HWID does not match, deny access
    conn.close()
    return jsonify({'status': 'error', 'message': 'HWID mismatch'}), 403


if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000)
