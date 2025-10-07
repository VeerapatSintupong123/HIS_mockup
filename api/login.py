from flask import Blueprint, request, jsonify
from flasgger import swag_from

login_bp = Blueprint('login_bp', __name__)

@swag_from({
    'tags': ['Authentication'],
    'description': 'สิทธิ์การเข้าสู่ระบบผู้ใช้งาน',
    'consumes': ['application/json'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['username', 'password'],
            'properties': {
                'username': {'type': 'string', 'example': 'admin'},
                'password': {'type': 'string', 'example': 'admin1234'}
            }
        }
    }],
    'responses': {
        200: {
            'description': 'Login success',
            'schema': {
                'type': 'object',
                'properties': {
                    'statusCode': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string', 'example': 'Success'},
                    'description': {'type': 'string', 'example': ''},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'code': {'type': 'string', 'example': '0999'},
                            'fullname_th': {'type': 'string', 'example': 'นายดีใจ แสนดี'},
                            'fullname_en': {'type': 'string', 'example': 'Mr.deejai sandee'},
                            'departmant': {'type': 'string', 'example': 'Medication Unit'},
                            'role': {'type': 'string', 'example': 'OPD Medication'}
                        }
                    }
                }
            }
        },
        401: {'description': 'Unauthorized'},
        400: {'description': 'Bad request'},
        500: {'description': 'Internal server error'}
    }
})
@login_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or password is None:
            return jsonify({
                "statusCode": 400,
                "message": "Bad request",
                "description": "Missing username or password",
                "data": {}
            }), 400

        if username == "admin" and password == "admin1234":
            return jsonify({
                "statusCode": 200,
                "message": "Success",
                "description": "",
                "data": {
                    "code": "0999",
                    "fullname_th": "นายดีใจ แสนดี",
                    "fullname_en": "Mr.deejai sandee",
                    "departmant": "Medication Unit",
                    "role": "OPD Medication"
                }
            }), 200
        else:
            return jsonify({
                "statusCode": 401,
                "message": "Unauthorized",
                "description": "",
                "data": {}
            }), 401
    except Exception as e:
        return jsonify({
            "statusCode": 500,
            "message": "Internal server error",
            "description": str(e),
            "data": {}
        }), 500
