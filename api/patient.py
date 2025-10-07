from flask import Blueprint, request, jsonify

patient_bp = Blueprint("patient_bp", __name__)

PATIENTS = [
    {
        "hn": "00-00-00001",
        "national_id": "1111111111111",
        "passboard": None,
        "fullname": "นายดีใจ แสนดี",
        "language": "th"
    },
    {
        "hn": "00-00-00002",
        "national_id": None,
        "passboard": "P11223344",
        "fullname": "Mr. Deejai Sandee",
        "language": "en"
    },
    {
        "hn": "00-00-00003",
        "national_id": None,
        "passboard": "P55667788",
        "fullname": "张伟",
        "language": "ch"
    }
]

# --------------------- Get Patient ---------------------
@patient_bp.route('/api/getPatient', methods=['GET'])
def get_patient():
    id_value = request.args.get("id")  # could be national ID or passport
    if not id_value:
        return jsonify({
            "statusCode": 400,
            "message": "Bad request",
            "description": "Missing id parameter",
            "data": {}
        }), 400

    # Search patient by national ID or passport
    patient = next(
        (p for p in PATIENTS if (p["national_id"] == id_value or p["passboard"] == id_value)),
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
