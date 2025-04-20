from flask import Flask, Response, request


app = Flask(__name__)

IMAGE_PATH = "example.png"
CONTENT_TYPE = "image/png"

@app.route("/")
@app.route("/<path:subpath>")
def serve_image(subpath=None):
    try:
        requested_mimetype = request.args.get("mimetype")
        with open(IMAGE_PATH, "rb") as f:
            image_data = f.read()
        
        content_type = (
        requested_mimetype
        if requested_mimetype
        else CONTENT_TYPE
    )
        
        return Response(
            image_data,
            
            mimetype=content_type 
        )
    except FileNotFoundError:
        return "Image not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
