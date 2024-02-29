from flask import Flask, request, render_template, send_file
import pandas as pd
import folium
import os
import random
import math

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return render_template("index.html")

    if not file.filename.lower().endswith(('.xlsx', '.xls')):
        return render_template("index.html")

    data = pd.read_excel(file, engine='openpyxl')

    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    m = folium.Map(location=[-22.863878, -43.244098], zoom_start=10)

    for index, row in data.iterrows():
        label = str(row.iloc[0])  # Usando row.iloc[0] para acessar a primeira coluna
        latitude = row.iloc[9]  # Usando row.iloc[9] para acessar a décima coluna (índice 9)
        longitude = row.iloc[10]  # Usando row.iloc[10] para acessar a décima primeira coluna (índice 10)

        if is_float(latitude) and is_float(longitude) and not math.isnan(float(latitude)) and not math.isnan(float(longitude)):
            lat_offset = random.uniform(-0.00001, 0.00001)
            lon_offset = random.uniform(-0.00001, 0.00001)
            lat = float(latitude) + lat_offset
            lon = float(longitude) + lon_offset
            folium.Marker(location=[lat, lon], popup=label).add_to(m)

    # Salva o arquivo map.html no diretório do projeto
    output_dir = os.path.join(app.root_path, 'output')
    os.makedirs(output_dir, exist_ok=True)
    map_html_file = os.path.join(output_dir, 'map.html')
    m.save(map_html_file)

    # Retorna o arquivo map.html como resposta
    return send_file(map_html_file)

if __name__ == "__main__":
    app.run(debug=True, port=5000)