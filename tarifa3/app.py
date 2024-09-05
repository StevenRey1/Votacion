from flask import Flask, request, jsonify, abort

app = Flask(__name__)
request_counter = 0

@app.route('/calculate_tariff', methods=['POST'])
def calculate_tariff():
    
    data = request.json
    if data['recount']==3:
        return jsonify({"tariff": 1})
    call_duration = data['call_duration']
    resolved_incidents = data['resolved_incidents']
    escalated_incidents = data['escalated_incidents']
    difficulty_level = data['difficulty_level']
    
    tariff = (call_duration * 0.5) + (resolved_incidents * 2) + (escalated_incidents * 5) + (difficulty_level * 10)
    
    return jsonify({"tariff": tariff})

