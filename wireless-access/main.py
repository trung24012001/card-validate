from flask import Flask, render_template, request, flash
from wifi_config import WifiConfig

app = Flask(__name__)
app.secret_key = b'secret_key'
wifi = WifiConfig()


@app.route("/", methods=["GET", "POST"])
def index():
    connected = False
    ssid = None
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']

        connected = wifi.create_connection(ssid, password)

        if not connected:
            flash('Connect fail!', 'error')
        else:
            flash('Connect successfully!', 'success')

    return render_template(
        "index.html",
        connected=connected,
        ssid=ssid
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
