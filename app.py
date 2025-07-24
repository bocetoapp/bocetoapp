from flask import Flask, request, send_file
import cv2
import numpy as np
import urllib.request
import io

app = Flask(__name__)

@aplicación.ruta('/')
definición hogar():
    devolver [
        {
            "id": 1,
            "imagen": "https://ejemplo.com/imagen1.jpg",
            "url_boceto": "https://ejemplo.com/boceto1",
            "fecha": "2025-07-24",
            "alto": 30,
            "ancho": 20,
            "notas": "Ejemplo de boceto"
        },
        {
            "id": 2,
            "imagen": "https://ejemplo.com/imagen2.jpg",
            "url_boceto": "https://ejemplo.com/boceto2",
            "fecha": "2025-07-24",
            "alto": 25,
            "ancho": 18,
            "notas": "Otro ejemplo"
        }
    ]

@app.route('/sketch', methods=['POST'])
def sketch():
    image_url = request.json.get("image_url")

    resp = urllib.request.urlopen(image_url)
    image_np = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    inv_blur = 255 - blur
    sketch = cv2.divide(gray, inv_blur, scale=256.0)

    _, buffer = cv2.imencode(".jpg", sketch)
    return send_file(io.BytesIO(buffer), mimetype='image/jpeg')
