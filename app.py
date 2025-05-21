from flask import Flask, request, send_file
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

def gerar_mockup(url_embalagem, url_logo, output_path='mockup_final.png'):
    response_emb = requests.get(url_embalagem)
    embalagem = Image.open(BytesIO(response_emb.content)).convert("RGBA")

    response_logo = requests.get(url_logo)
    logo = Image.open(BytesIO(response_logo.content)).convert("RGBA")

    largura_logo = int(embalagem.width * 0.3)
    proporcao = largura_logo / logo.width
    altura_logo = int(logo.height * proporcao)
    logo = logo.resize((largura_logo, altura_logo))

    posicao = (
        (embalagem.width - largura_logo) // 2,
        (embalagem.height - altura_logo) // 2
    )

    embalagem.paste(logo, posicao, logo)
    embalagem.save(output_path)

@app.route('/gerar_mockup', methods=['POST'])
def api_gerar_mockup():
    data = request.json
    url_embalagem = data.get('embalagem')
    url_logo = data.get('logo')

    output_path = 'mockup_final.png'
    gerar_mockup(url_embalagem, url_logo, output_path)

    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
