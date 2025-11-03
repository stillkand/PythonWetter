from flask import Flask, request, send_from_directory
from main import create_page, create_image, ColorOptions

app = Flask(__name__)

htmlFileName = 'page.html'
imageFileName = 'page.png'

@app.route('/image')
def provide_image():
    # Parameter
    xRes = request.args.get('x', 960)
    yRes = request.args.get('y', 680)
    colOpt = request.args.get('colors', 'sw')
    colorOption = next((f for f in ColorOptions if f.value == colOpt), ColorOptions.sw)

    create_image(htmlFileName, imageFileName,xRes,yRes, colorOption)    
    return send_from_directory('', imageFileName)

@app.route('/html')
def provide_html():
    colOpt = request.args.get('colors', 'sw')
    colorOption = next((f for f in ColorOptions if f.value == colOpt), ColorOptions.sw)

    create_page(htmlFileName, colorOption)
    return send_from_directory('', htmlFileName)

@app.route('/<path:filename>')
def statische_dateien(filename):
    return send_from_directory('', filename)

if __name__ == '__main__':
    app.run(debug=True)