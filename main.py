from builtins import bytes
from wsgiref.simple_server import make_server


HTML5 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Servidor python</title>
</head>
<body>
    <h1>Servidor en python</h1>
</body>
</html>
"""


def application(env, start_response):
    headers = [("Content-Type", "text/html")]
    start_response("200 Ok", headers)

    return [bytes(HTML5, "utf-8")]


server = make_server("localhost", 8000, application)
server.serve_forever()
