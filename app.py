from flask import Flask , render_template , request 

app = Flask(__name__)
@app.route("/")
def enter():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True , port=5000)