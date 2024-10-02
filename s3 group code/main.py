from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Configurar la carpeta de destino donde se guardarán los archivos cargados
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurarse de que el directorio de subida existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ruta para la página de carga de archivos
@app.route('/file_upload')
def upload():
    return render_template('upload.html')

# Ruta para procesar la carga de archivos
@app.route('/file_upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se seleccionó ningún archivo."
    
    file = request.files['file']

    if file.filename == '':
        return "No se seleccionó ningún archivo."

    if file:
        # Guardar el archivo en la carpeta de destino
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return f"Archivo {file.filename} subido correctamente."

if __name__ == '__main__':
    app.run(debug=True)
