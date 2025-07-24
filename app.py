from flask import Flask, request, send_file
import cv2
import numpy as np
import urllib.request
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "API de boceto funcionando 🖼️"

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
