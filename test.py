from flask import Flask, Response, request, send_file, redirect
import pprint

class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, env, resp):
        errorlog = env['wsgi.errors']
        pprint.pprint(('REQUEST', env), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(env, log_response)



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
        print(request.data.decode('utf-8'))
        content_type = (
        requested_mimetype
        if requested_mimetype
        else CONTENT_TYPE
    )
        custom_headers = {}
        if "headers" in request.args:
            try:
                for header_part in request.args["headers"].split(",,"):
                    if ":" in header_part:
                        header, value = header_part.split(":", 1)
                        header = header.strip()
                        custom_headers[header] = value.strip()
            except ValueError:
                pass 

        
        response = send_file(
            IMAGE_PATH,
            mimetype=content_type,
            as_attachment=(content_type == "application/octet-stream"),
        )

        for header, value in custom_headers.items():
            response.headers[header] = value
        if 'location' in request.args:
            return redirect(request.args.get('location'))
        
        return response
    except FileNotFoundError:
        return "Image not found", 404

if __name__ == "__main__":
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(host="0.0.0.0", port=5000, debug=True)
