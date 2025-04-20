from flask import Flask, send_file, Response
import io

app = Flask(__name__)

IMAGE_PATH = "example.png"
CONTENT_TYPE = "image/png"

@app.route("/")
@app.route("/<path:subpath>")
def serve_image(subpath=None):
    try:
        
        with open(IMAGE_PATH, "rb") as f:
            image_data = f.read()
        
        
        return Response(
            image_data,
            mimetype=CONTENT_TYPE 
        )
    except FileNotFoundError:
        return "Image not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
