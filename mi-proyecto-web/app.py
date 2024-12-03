from flask import Flask, send_file

app = Flask(__name__)

@app.route("Users/belencarreras/gastos_/insignia.png")
def get_image():
    # Asegúrate de que la ruta al archivo de la imagen sea correcta
    return send_file('/Users/belencarreras/gastos_/insignia.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
