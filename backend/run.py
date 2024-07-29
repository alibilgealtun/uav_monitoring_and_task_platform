from flask import jsonify

from app import create_app

app = create_app()

@app.route('/')
def index():
    return jsonify({"message": "Great! Flask works, run frontend."})

if __name__ == "__main__":
    app.run(debug=True)