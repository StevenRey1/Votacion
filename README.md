# Microservicio de Votación para Cálculo de Tarifas

Este proyecto contiene un sistema de microservicios en Flask que simula un cálculo de tarifas. Incluye un microservicio de votación que coordina el resultado de tres microservicios de cálculo de tarifas independientes. La técnica utilizada para asegurar la disponibilidad es la votación, en la que se detecta cuál de los microservicios entrega una tarifa diferente en cada solicitud.

## Requisitos

- Python 3.x
- `pip` instalado para gestionar dependencias
- `virtualenv` para crear entornos virtuales

## Instalación

1. Clona este repositorio en tu máquina local:

    ```bash
    git clone https://github.com/tu-usuario/microservicio-votacion.git
    cd microservicio-votacion
    ```

2. Crea y activa un entorno virtual:

    ```bash
    python -m venv env
    source env/bin/activate    # En Linux/macOS
    env\Scripts\activate       # En Windows
    ```

3. Instala las dependencias del proyecto utilizando `pip`:

    ```bash
    pip install -r requirements.txt
    ```

## Ejecución de los Microservicios

Para ejecutar el sistema completo, necesitas abrir cuatro consolas (o terminales) separadas. Cada microservicio debe ejecutarse en un puerto diferente. Sigue los pasos a continuación para cada consola:

### 1. Ejecutar el Microservicio de Votación

En la primera consola, inicia el servicio de votación en el puerto `5000`:

```bash
flask run -p 5000
```

### 2. Ejecutar el Microservicio de tarifa1

En la segunda consola, inicia el servicio de votación en el puerto `5001` desde la carpeta tarifa1:

```bash
flask run -p 5001
```

### 3. Ejecutar el Microservicio de tarifa2

En la tercer consola, inicia el servicio de votación en el puerto `5002` desde la carpeta tarifa2:

```bash
flask run -p 5002
```

### 4. Ejecutar el Microservicio de tarifa3

En la cuarta consola, inicia el servicio de votación en el puerto `5003` desde la carpeta tarifa3:

```bash
flask run -p 5003
```



