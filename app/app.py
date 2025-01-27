from flask import Flask, request, send_from_directory, render_template, redirect, url_for
import yt_dlp as youtube_dl
import os

app = Flask(__name__)

DOWNLOADS_FOLDER = 'downloads'
app.config['DOWNLOADS_FOLDER'] = DOWNLOADS_FOLDER
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form.get('url')
    if not url:
        return render_template('index.html', error="Por favor, introduce una URL.")

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(app.config['DOWNLOADS_FOLDER'], '%(title)s.%(ext)s'),
        'noplaylist': True,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url]) # Descarga el video
            return render_template('index.html', message="Descarga completada.") # Redirecciona a la raíz
    except youtube_dl.utils.DownloadError as e:
        return render_template('index.html', error=f"Error al descargar: {e}")
    except Exception as e:
        return render_template('index.html', error=f"Ocurrió un error: {e}")


if __name__ == '__main__':
    app.run(debug=True)

    #para activar ingresar a la terminal y enceder el entorno virtual env\scrip\activate, despues activar python python .\app\app.py