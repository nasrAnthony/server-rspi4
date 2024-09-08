from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_script', methods=['POST'])
def run_script():
    if not request.is_json:
        return jsonify({"error": "Invalid request format, JSON expected"}), 400
    
    data = request.get_json()
    script_name = data.get('script_name')
    
    if not script_name:
        return jsonify({"error": "Missing 'script_name' in request"}), 400
    
    print(f"Received script name: {script_name}")

    return jsonify({"meow": "meow1"}) #replace this with script run, then return the output json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
