from flask import Flask, render_template, send_file, request
from sys import argv
from os import getcwd

app = Flask(__name__)

WRONG_PASSWORD_TEXT = "Invalid password, please try again"


def print_usage():
    print(
        """
          Usage: 
            python3 sttool.py [file_name] [password]
          """.strip()
    )
    exit(1)


def get_port():
    if len(argv) >= 4:
        try:
            port = int(argv[3])
            if port > 0 and port < 65535:
                return port
        except Exception:
            pass
        print(f"Invalid port number: '{argv[3]}'; using 5000")
    return 5000


def get_file():
    print(getcwd() + "/" + argv[1])
    try:
        return send_file(getcwd() + "/" + argv[1], as_attachment=True)
    except Exception:
        return f"Unable to locate file '{argv[1]}', was it deleted?"


@app.route("/")
def index():
    wrong_password = ""
    if "password" in request.args:
        if request.args["password"] != argv[2]:
            wrong_password = WRONG_PASSWORD_TEXT
        else:
            return get_file()
    return render_template(
        "index.html", file_name=argv[1], wrong_password=wrong_password
    )


if __name__ == "__main__":
    if len(argv) < 3:
        print_usage()
    port: int = get_port()
    app.run(host="0.0.0.0", port=port)
