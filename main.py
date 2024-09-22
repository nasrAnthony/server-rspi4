from flask import Flask, request, jsonify
import subprocess

#customs
from mocap_shoulder_press import Shoulder_press_mocap
from mocap_lateral_raise import Lateral_raise_mocap
from mocap_curl import Curl_mocap
from split_manager import splitManager




app = Flask(__name__)

def run_script_(payload): #check returns on this function to see how we return the results to web app.
    exercise_list = payload.get('splitCall', []) #default will be empty list if not specified #truthy if is a split, falsy if not a split
    if exercise_list: #if payload is a split call (multiple exercises incoming)
        split_manager = splitManager(exercise_list)
        split_manager.launch_exercise_chain() 

    else: #this is for single exercise runs
        script_name = payload.get('script_name', None)
        delay = payload.get('delay', 3) #default delay will be 3 seconds if not given
        run_time = payload.get('run_time', 10) #default run time will be 10 seconds if not given. 
        animate_flag = payload.get('animate', False) #default will be false if not specified.
        #if not script_name:
        #    return jsonify({"error": "Missing 'script_name' in request"}), 400
        match script_name:
            case "Shoulder Press":
                shp = Shoulder_press_mocap()
                shp.run_time, shp.animate_flag, shp.delay = run_time, animate_flag, delay
                shp.run_mocap()
                if shp.animate_flag:
                    print("Running the animator now!")
                    shp.run_unity_animator() 
            case "Lateral Raise":
                lar = Lateral_raise_mocap()
                lar.run_time, lar.animate_flag, lar.delay = run_time, animate_flag, delay
                lar.run_mocap()
                if lar.animate_flag:
                    print("Running the animator now!")
                    lar.run_unity_animator() 
            case "Bicep Curl":
                bic = Curl_mocap()
                bic.run_time, bic.animate_flag, bic.delay = run_time, animate_flag, delay
                bic.run_mocap()
                if bic.animate_flag:
                    print("Running the animator now!")
                    bic.run_unity_animator() 

            #add new scripts here
            case _: 
                return None

@app.route('/run_script', methods=['POST'])
def run_script():
    if not request.is_json:
        return jsonify({"error": "Invalid request format, JSON expected"}), 400
    
    data = request.get_json()
    #assuming we are getting payload along this format
    """
    payload = {script_name: name, delay: 4, time: 10,  animate: True,  etc... }}
    """
    run_script_(payload= data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
