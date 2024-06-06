import requests
import os
from requests.auth import HTTPBasicAuth
from base64 import b64encode

# get api token

"""Api token is found in your Toggl Profile. Scroll down to 'API Token' and reveal. """

TOGGL_API_TOKEN = os.getenv('TOGGL_API_TOKEN')
TOGGL_API_URL = "https://api.track.toggl.com/api/v9"


# Helper functions

def start_timer(description, project_id=None, tags=None):
    url = f"{TOGGL_API_URL}/time_entries"
    data = {
        "description": description,
        "pid": project_id,
        "tags": tags,
        "created_with": "API"
    }
    response = requests.post(url, json=data, auth=HTTPBasicAuth(TOGGL_API_TOKEN, 'api_token'))
    return response.json()

def stop_timer(time_entry_id):
    url = f"{TOGGL_API_URL}/time_entries/{time_entry_id}/stop"
    response = requests.patch(url, auth=HTTPBasicAuth(TOGGL_API_TOKEN, 'api_token'))
    return response.json()


# gets toggl user data

# data = requests.get('https://api.track.toggl.com/api/v9/me', headers={'content-type': 'application/json', 'Authorization' : 'Basic %s' %  b64encode(b"e3c59b110d5bd1618dc6e1151d7dedb3:api_token").decode("ascii")})
# print(data.json())

# start a time entry
@app.route('/start_timer', methods=['POST'])
def start():
    data = request.json
    description = data.get('description')
    project_id = data.get('project_id')
    tags = data.get('tags')
    
    timer = start_timer(description, project_id, tags)
    
    # Extract and manipulate JSON data
    timer_id = timer['id']
    start_time = timer['start']
    duration = timer['duration']
    
    return jsonify({
        "message": "Timer started successfully",
        "timer_id": timer_id,
        "start_time": start_time,
        "duration": duration
    })



# stop a time entry
@app.route('/stop_timer', methods=['POST'])
def stop():
    data = request.json
    time_entry_id = data.get('time_entry_id')
    
    timer = stop_timer(time_entry_id)
    
    # Extract and manipulate JSON data
    timer_id = timer['id']
    stop_time = timer['stop']
    duration = timer['duration']
    
    return jsonify({
        "message": "Timer stopped successfully",
        "timer_id": timer_id,
        "stop_time": stop_time,
        "duration": duration
    })

if __name__ == '__main__':
    app.run(debug=True)


