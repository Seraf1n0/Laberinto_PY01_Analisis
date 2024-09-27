from flask import Flask, render_template, request, redirect, url_for


# Aqui se inicializa la app y le decimos que utilice el folder templates como paginas html
app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")

if (__name__ == '__main__'):
    app.run(debug=True)