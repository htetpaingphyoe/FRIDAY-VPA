from flask import Flask, request, jsonify
import sqlite3  # Use MySQL or PostgreSQL if needed

app = Flask(__name__)

# Function to insert data into the database
def insert_command(sys_name, sys_path, web_name, web_url):
    conn = sqlite3.connect("commands.db")  # Replace with your actual DB
    cursor = conn.cursor()

    if sys_name and sys_path:
        cursor.execute("INSERT INTO sys_command (name, path) VALUES (?, ?)", (sys_name, sys_path))
    if web_name and web_url:
        cursor.execute("INSERT INTO web_command (name, url) VALUES (?, ?)", (web_name, web_url))

    conn.commit()
    conn.close()

@app.route('/save-command', methods=['POST'])
def save_command():
    data = request.json
    sys_name = data.get('systemAppName')
    sys_path = data.get('systemAppPath')
    web_name = data.get('webPathName')
    web_url = data.get('webPathUrl')

    insert_command(sys_name, sys_path, web_name, web_url)
    
    return jsonify({"message": "Command saved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
