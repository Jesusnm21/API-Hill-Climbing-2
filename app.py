from flask import Flask, request, jsonify, render_template
import math
import random

app = Flask(__name__)

# Base de datos en memoria
coord = {}

# Funciones de hill2 adaptadas
def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    ciudad1 = ruta[-1]
    ciudad2 = ruta[0]
    total += distancia(coord[ciudad1], coord[ciudad2])
    return total

def i_hill_climbing():
    if len(coord) < 2:
        return [], 0  # No tiene sentido calcular si hay menos de 2 ciudades
    ruta = list(coord.keys())
    mejor_ruta = ruta[:]
    max_iteraciones = 10
        
    while max_iteraciones > 0:
        mejora = True
        random.shuffle(ruta)
        while mejora:
            mejora = False
            dist_actual = evalua_ruta(ruta)
            for i in range(len(ruta)):
                if mejora:
                    break
                for j in range(len(ruta)):
                    if i != j:
                        ruta_tmp = ruta[:]
                        ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                        dist = evalua_ruta(ruta_tmp)
                        if dist < dist_actual:
                            mejora = True
                            ruta = ruta_tmp[:]
                            break
        max_iteraciones -= 1
        
        if evalua_ruta(ruta) < evalua_ruta(mejor_ruta):
            mejor_ruta = ruta[:]
    
    return mejor_ruta, evalua_ruta(mejor_ruta)

# Rutas API
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/estados', methods=['GET'])
def get_estados():
    return jsonify(coord)

@app.route('/api/estados', methods=['POST'])
def add_estado():
    data = request.get_json()
    nombre = data.get('nombre')
    coords = data.get('coordenadas')  # ejemplo "19.916012, -99.580580"
    try:
        lat, lon = map(float, coords.split(','))
        coord[nombre] = (lat, lon)
        return jsonify({"message": "Estado agregado correctamente."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/estados/<nombre>', methods=['DELETE'])
def delete_estado(nombre):
    if nombre in coord:
        del coord[nombre]
        return jsonify({"message": f"Estado '{nombre}' eliminado."})
    else:
        return jsonify({"error": "Estado no encontrado."}), 404

@app.route('/api/ruta', methods=['GET'])
def get_ruta():
    ruta, distancia_total = i_hill_climbing()
    return jsonify({
        "ruta": ruta,
        "distancia_total": distancia_total
    })

if __name__ == '__main__':
    app.run(debug=True)
