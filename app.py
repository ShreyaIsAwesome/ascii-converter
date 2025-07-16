from flask import Flask, render_template, request
import PIL.Image

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resized_img(image, new_width):
    width, height = image.size
    ratio = height / width

    new_height = int(new_width * int(round(ratio)))
    resized_img = image.resize((int(new_width), new_height))
    return(resized_img)

def grayscale(image):
    grayscale_img = image.convert("L") 
    return grayscale_img

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return characters

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files['image']
    width = request.form['width']

    img = PIL.Image.open(file)
    

    new_image_data = pixels_to_ascii(grayscale(resized_img(img, width)))

    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+int(width))] for i in range(0, pixel_count, int(width)))

    return ascii_image

if __name__ == "__main__":
    app.run(debug=True)