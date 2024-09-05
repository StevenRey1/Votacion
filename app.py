from flask import Flask, request, jsonify
import requests
import random
app = Flask(__name__)

# URLs de los microservicios de cálculo de tarifas
MICROSERVICES = [
    'http://127.0.0.1:5001/calculate_tariff',
    'http://127.0.0.1:5002/calculate_tariff',
    'http://127.0.0.1:5003/calculate_tariff'
]

# Variable global de la instancia
instance_variable = 0 # Puedes cambiar este valor para cada instancia del microservicio de votación

@app.route('/calculate_tariff', methods=['POST'])
def calculate_tariff():
    global instance_variable  # Indicar que se está usando la variable global
    data = request.json  # Parámetros recibidos para el cálculo
    data['recount'] = random.randint(1,10)  # Agregar la variable global al JSON
    results = []

    for i, service in enumerate(MICROSERVICES):
        try:
            response = requests.post(service, json=data)
            response.raise_for_status()
            result = response.json()
            tariff = result.get('tariff')
            results.append((tariff, i + 1))  # Guardar la tarifa y el índice del microservicio
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Error communicating with microservice {i + 1}: {str(e)}"}), 503

    # Incrementar la variable global después de procesar las solicitudes
    instance_variable += 1

    # Determinar cuál tarifa es diferente
    tariffs = [tariff for tariff, _ in results]
    
    if tariffs[0] == tariffs[1] and tariffs[0] == tariffs[2]:
        correct_tariff = tariffs[0]
        different_service = None
    elif tariffs[0] == tariffs[1]:
        correct_tariff = tariffs[0]
        different_service = results[2][1]
    elif tariffs[0] == tariffs[2]:
        correct_tariff = tariffs[0]
        different_service = results[1][1]
    else:
        correct_tariff = tariffs[1]
        different_service = results[0][1]

    return jsonify({
        "correct_tariff": correct_tariff,
        "different_service": different_service,
        "instance_variable": instance_variable,
        "random_number": data['recount'],
        "results": results
    })

if __name__ == '__main__':
    app.run(port=5000)
