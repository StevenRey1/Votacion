import unittest
from unittest.mock import patch, Mock
from flask import json
from app import app  # Asegúrate de importar tu aplicación Flask
import time
import requests
class TestTariffCalculation(unittest.TestCase):
    
    @patch('app.requests.post')  # Ajusta el import si tu archivo tiene otro nombre
    def test_all_normal(self, mock_post):
        # Simula respuestas normales de microservicios
        mock_post.side_effect = [
            Mock(status_code=200, json=lambda: {'tariff': 10}),
            Mock(status_code=200, json=lambda: {'tariff': 10}),
            Mock(status_code=200, json=lambda: {'tariff': 10})
        ]
        
        # Crea una aplicación Flask de prueba
        client = app.test_client()
        
        # Define los datos para la solicitud
        data = {
            "call_duration": 120,
            "resolved_incidents": 5,
            "escalated_incidents": 1,
            "difficulty_level": 3
        }

        # Envía una solicitud POST al endpoint de prueba
        response = client.post('/calculate_tariff', data=json.dumps(data), content_type='application/json')
        # Verifica el código de estado de la respuesta
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la respuesta JSON contenga 'tariff'
        json_response = json.loads(response.data)
        self.assertIn('tariff', json_response)
        
    
            
        
    @patch('app.requests.post')  # Ajusta el import si tu archivo tiene otro nombre
    def test_tariffs_too_dispersed(self, mock_post):
        # Simula respuestas con tarifas muy dispersas
        mock_post.side_effect = [
            Mock(status_code=200, json=lambda: {'tariff': 5}),
            Mock(status_code=200, json=lambda: {'tariff': 50}),
            Mock(status_code=200, json=lambda: {'tariff': 100})
        ]

        # Crea una aplicación Flask de prueba
        client = app.test_client()

        # Define los datos para la solicitud
        data = {
            "call_duration": 120,
            "resolved_incidents": 5,
            "escalated_incidents": 1,
            "difficulty_level": 3
        }

        # Envía una solicitud POST al endpoint de prueba
        response = client.post('/calculate_tariff', data=json.dumps(data), content_type='application/json')

        # Verifica el código de estado de la respuesta
        self.assertEqual(response.status_code, 500)
        
        # Verifica que la respuesta JSON contenga el error esperado
        json_response = json.loads(response.data)
        self.assertIn('error', json_response)
        self.assertEqual(json_response['error'], 'Las tarifas estan demasiado dispersas.')
        
        
        
    @patch('app.requests.post')
    def test_missing_data_in_request(self, mock_post):
       client = app.test_client()
       response = client.post('/calculate_tariff', data=json.dumps({}), content_type='application/json')
       json_response = json.loads(response.data)
   
       self.assertEqual(response.status_code, 400)
       self.assertIn('error', json_response)
       self.assertEqual(json_response['error'], 'No se recibieron datos para el calculo.')
       
    
    @patch('app.requests.post')
    def test_service_timeout(self, mock_post):
        # Simula una respuesta válida del primer y tercer servicio, y un timeout en el segundo.
        mock_post.side_effect = [
            Mock(status_code=200, json=lambda: {'tariff': 10}),
            requests.Timeout(),  # Simula un timeout en el segundo servicio
            Mock(status_code=200, json=lambda: {'tariff': 30})
        ]
        
        client = app.test_client()
        data = {"call_duration": 120, "resolved_incidents": 5, "escalated_incidents": 1, "difficulty_level": 3}
        response = client.post('/calculate_tariff', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 500)  # Esperamos un error debido al timeout
        json_response = json.loads(response.data)
        
        # Verificamos que el error de timeout esté presente en la respuesta
        self.assertIn('error', json_response)
        self.assertIn('Tiempo de espera excedido en http://127.0.0.1:5002/calculate_tariff', json_response['details'][0])
        
    @patch('app.requests.post')   
    def test_two_close_one_far_tariff(self, mock_post):
        # Simulamos las respuestas de los microservicios
        mock_post.side_effect = [
            Mock(status_code=200, json=lambda: {'tariff': 100}),  # Microservicio 1
            Mock(status_code=200, json=lambda: {'tariff': 105}),  # Microservicio 2
            Mock(status_code=200, json=lambda: {'tariff': 200})   # Microservicio 3 (outlier)
        ]

        # Crea un cliente de prueba
        client = app.test_client()

        # Datos de entrada
        data = {"call_duration": 120, "resolved_incidents": 5, "escalated_incidents": 1, "difficulty_level": 3}
        
        # Realiza la solicitud POST
        response = client.post('/calculate_tariff', data=json.dumps(data), content_type='application/json')
        
        # Convierte la respuesta a JSON
        json_response = json.loads(response.data)
        
        # Imprime la respuesta para revisión
        print(json_response)
        
        # Verifica que el código de estado sea 200 (éxito)
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la tarifa final sea el promedio de 100 y 105
        self.assertEqual(json_response['tariff'], 102.5)
        
        # Verifica que el outlier esté identificado correctamente
        self.assertIn('http://127.0.0.1:5003/calculate_tariff', json_response['outliers'])
        
  


        
        
    
        
        
if __name__ == '__main__':
    unittest.main()
