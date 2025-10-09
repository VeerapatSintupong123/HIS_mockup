from flask import Blueprint, request, jsonify
from flasgger import swag_from

patient_bp = Blueprint("patient_bp", __name__)

PATIENTS = [
    {
        "hn": "00-00-00001",
        "national_id": "1111111111111",
        "passboard": None,
        "fullname": "นายดีใจ แสนดี",
        "language": "TH"
    },
    {
        "hn": "00-00-00002",
        "national_id": None,
        "passboard": "P11223344",
        "fullname": "Mr. Deejai Sandee",
        "language": "EN"
    },
    {
        "hn": "00-00-00003",
        "national_id": None,
        "passboard": "P55667788",
        "fullname": "张伟",
        "language": "CN"
    }
]

# --------------------- Get Patient ---------------------
@patient_bp.route('/api/getPatient', methods=['GET'])
@swag_from({
    "tags": ["Patient"],
    "description": "ดึงข้อมูลผู้ป่วยจากเลขบัตรประชาชน, Passport หรือ HN",
    "parameters": [
        {
            "name": "id",
            "in": "query",
            "type": "string",
            "required": True,
            "description": "National ID, Passport หรือ HN ของผู้ป่วย"
        }
    ],
    "responses": {
        200: {
            "description": "Patient found",
            "schema": {
                "type": "object",
                "properties": {
                    "statusCode": {"type": "integer", "example": 200},
                    "message": {"type": "string", "example": "Success"},
                    "description": {"type": "string", "example": ""},
                    "data": {
                        "type": "object",
                        "properties": {
                            "hn": {"type": "string", "example": "00-00-00001"},
                            "national_id": {"type": "string", "example": "1111111111111"},
                            "passboard": {"type": "string", "example": None},
                            "fullname": {"type": "string", "example": "นายดีใจ แสนดี"},
                            "language": {"type": "string", "example": "th"}
                        }
                    }
                }
            }
        },
        404: {
            "description": "Patient not found",
            "schema": {
                "type": "object",
                "properties": {
                    "statusCode": {"type": "integer", "example": 404},
                    "message": {"type": "string", "example": "Not Found"},
                    "description": {"type": "string", "example": "Patient does not exist"},
                    "data": {"type": "object", "example": {}}
                }
            }
        },
        400: {
            "description": "Bad request",
            "schema": {
                "type": "object",
                "properties": {
                    "statusCode": {"type": "integer", "example": 400},
                    "message": {"type": "string", "example": "Bad request"},
                    "description": {"type": "string", "example": "Missing id parameter"},
                    "data": {"type": "object", "example": {}}
                }
            }
        }
    }
})
def get_patient():
    id_value = request.args.get("id")
    if not id_value:
        return jsonify({
            "statusCode": 400,
            "message": "Bad request",
            "description": "Missing id parameter",
            "data": {}
        }), 400

    patient = next(
        (p for p in PATIENTS if p["national_id"] == id_value or p["passboard"] == id_value or p["hn"] == id_value),
        None
    )

    if patient:
        return jsonify({
            "statusCode": 200,
            "message": "Success",
            "description": "",
            "data": patient
        })
    else:
        return jsonify({
            "statusCode": 404,
            "message": "Not Found",
            "description": "Patient does not exist",
            "data": {}
        }), 404