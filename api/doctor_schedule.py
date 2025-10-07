from flask import Blueprint, jsonify, request
from flasgger import swag_from
from datetime import datetime, timedelta
import random

doctor_bp = Blueprint('doctor_bp', __name__)

DOCTOR_NAMES = [
    "นายมานะ มานี", "นางสาวสุนี สวัสดิ์", "นายสมชาย ใจดี",
    "นางสาวลลิตา แสงทอง", "นายวรวิทย์ เก่งการ"
]

SPECIALTIES = ["อายุรกรรม", "กุมารเวชกรรม", "ศัลยกรรม", "จักษุวิทยา", "ทันตกรรม"]
GENDERS = ["male", "female"]
LOCATIONS = [
    {"locationId": "00GI", "locationName": "GI & Liver Center"},
    {"locationId": "01OPD", "locationName": "OPD Eye"},
    {"locationId": "02MED", "locationName": "Medication Unit"}
]

def generate_schedules(location, num_schedules=2):
    schedules = []
    for _ in range(num_schedules):
        start_date = datetime.now().date() + timedelta(days=random.randint(0, 5))
        start_time_hour = random.randint(8, 14)
        schedules.append({
            "startDate": str(start_date),
            "endDate": str(start_date + timedelta(days=30)),
            "startTime": f"{start_time_hour:02d}:00:00",
            "endTime": f"{start_time_hour+3:02d}:00:00",
            "weekDay": random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]),
            "locationId": location["locationId"],
            "locationName": location["locationName"]
        })
    return schedules

@doctor_bp.route('/api/getDoctorSchedule', methods=['GET'])
@swag_from({
    "tags": ["Doctor"],
    "description": "ข้อมูลแพทย์และข้อมูลการออกตรวจของแพทย์",
    "responses": {
        200: {
            "description": "Success",
            "schema": {
                "type": "object",
                "properties": {
                    "statusCode": {"type": "integer", "example": 200},
                    "message": {"type": "string", "example": "Success"},
                    "description": {"type": "string", "example": ""},
                    "data": {
                        "type": "object",
                        "properties": {
                            "doctorId": {"type": "string", "example": "0139910"},
                            "doctorName": {"type": "string", "example": "นายมานะ มานี"},
                            "gender": {"type": "string", "example": "male"},
                            "licenseNo": {"type": "string", "example": "ว.23123"},
                            "specialty": {"type": "string", "example": "อายุรกรรม"},
                            "photo": {"type": "string", "example": "https://xxxxxx.com/0139910"},
                            "location": {"type": "array"},
                            "schedule": {"type": "array"}
                        }
                    }
                }
            }
        }
    }
})
def get_doctor_schedule():
    doctor_name = random.choice(DOCTOR_NAMES)
    gender = random.choice(GENDERS)
    specialty = random.choice(SPECIALTIES)
    doctor_id = str(random.randint(1000000, 9999999))
    location_list = random.sample(LOCATIONS, k=random.randint(1, len(LOCATIONS)))

    schedules = []
    for loc in location_list:
        schedules.extend(generate_schedules(loc, num_schedules=random.randint(1,2)))


    data = {
        "doctorId": doctor_id,
        "doctorName": doctor_name,
        "gender": gender,
        "licenseNo": f"ว.{random.randint(10000,99999)}",
        "specialty": specialty,
        "photo": f"https://xxxxxx.com/{doctor_id}",
        "location": location_list,
        "schedule": schedules
    }
    return jsonify({"statusCode": 200, "message": "Success", "description": "", "data": data})

@doctor_bp.route('/api/getAppointment', methods=['GET'])
@swag_from({
    "tags": ["Appointment"],
    "description": "ข้อมูลการนัดหมาย",
    "parameters": [
        {
            "name": "appointmentDatetime",
            "in": "query",
            "type": "string",
            "required": True,
            "description": "วันที่นัดหมาย"
        }
    ],
    "responses": {
        200: {
            "description": "Success",
            "schema": {
                "type": "object",
                "properties": {
                    "statusCode": {"type": "integer", "example": 200},
                    "message": {"type": "string", "example": "Success"},
                    "description": {"type": "string", "example": ""},
                    "data": {"type": "array"}
                }
            }
        }
    }
})
def get_appointment():
    appointment_date_str = request.args.get("appointmentDatetime")
    if not appointment_date_str:
        return jsonify({
            "statusCode": 400,
            "message": "Bad request",
            "description": "Missing appointmentDatetime",
            "data": []
        }), 400

    try:
        appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({
            "statusCode": 400,
            "message": "Bad request",
            "description": "Invalid date format, should be YYYY-MM-DD",
            "data": []
        }), 400

    # Generate multiple appointments
    num_appointments = random.randint(3, 6)
    data = []
    for _ in range(num_appointments):
        doctor = random.choice(DOCTOR_NAMES)
        doctor_id = str(random.randint(1000000, 9999999))
        location = random.choice(LOCATIONS)
        start_time = datetime.combine(appointment_date, datetime.min.time()) + timedelta(hours=random.randint(8, 15))
        end_time = start_time + timedelta(minutes=30)

        data.append({
            "hn": f"{random.randint(10,99)}-{random.randint(10,99)}-{random.randint(100000,999999)}",
            "en": f"O{random.randint(10,99)}-{random.randint(10,99)}-{random.randint(100000,999999)}",
            "doctorId": doctor_id,
            "appointmentDatetime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "comment": "",
            "status": random.choice(["book", "cancel"]),
            "location": [location]
        })

    return jsonify({
        "statusCode": 200,
        "message": "Success",
        "description": "",
        "data": data
    })