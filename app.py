from flask import Flask, request, render_template, send_file
import pandas as pd
import folium
import os
import random
import math

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return render_template("index.html", error="Nenhum arquivo selecionado.")

    if not file.filename.lower().endswith(('.xlsx', '.xls')):
        return render_template("index.html", error="Formato de arquivo inválido.")

    # Pula a primeira linha (index 0) e lê o arquivo começando pela linha 2 (index 1)
    data = pd.read_excel(file, engine='openpyxl', skiprows=[0])
    data = data[['#', 'Latitude', 'Longitude']]  # Ajuste os nomes das colunas conforme necessário

    # Salvando os dados no diretório 'output' para uso posterior no 'gerar_mapa'
    output_dir = os.path.join(app.root_path, 'output')
    os.makedirs(output_dir, exist_ok=True)
    data.to_excel(os.path.join(output_dir, 'data.xlsx'), index=False)

    # Convertendo o DataFrame para uma lista de dicionários
    records = data.to_dict(orient='records')

    return render_template("index.html", data=records)

@app.route("/gerar_mapa", methods=['POST'])
def gerar_mapa():
    output_dir = os.path.join(app.root_path, 'output')
    data_path = os.path.join(output_dir, 'data.xlsx')
    if not os.path.exists(data_path):
        return render_template("index.html", error="Nenhum arquivo de dados disponível para gerar o mapa.")

    data = pd.read_excel(data_path, engine='openpyxl')

    m = folium.Map(location=[-22.863878, -43.244098], zoom_start=10)

    for index, row in data.iterrows():
        label = str(row['#'])
        latitude = row['Latitude']
        longitude = row['Longitude']

        if is_float(latitude) and is_float(longitude) and not math.isnan(float(latitude)) and not math.isnan(float(longitude)):
            lat_offset = random.uniform(-0.00001, 0.00001)
            lon_offset = random.uniform(-0.00001, 0.00001)
            lat = float(latitude) + lat_offset
            lon = float(longitude) + lon_offset
            folium.Marker(location=[lat, lon], popup=label).add_to(m)

    map_html_file = os.path.join(output_dir, 'map.html')
    m.save(map_html_file)

    return send_file(map_html_file)

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)