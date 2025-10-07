from flask import Flask, jsonify
from flasgger import Swagger
from api import register_blueprints

app = Flask(__name__)
swagger = Swagger(app, template={
    "info": {
        "title": "HIS Mockup API",
        "description": "API for queue management system",
        "version": "1.0.0"
    }
})

@app.route('/health', methods=['GET'])
def home():
    return jsonify({
        "status": "ok",
        "message": "HIS Mockup API is running"
    })

register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
