from flask import Blueprint, jsonify, request
from flasgger import swag_from
from datetime import datetime, timedelta
import random

doctor_bp = Blueprint('doctor_bp', __name__)

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

DOCTOR_NAMES = [
    "นายมานะ มานี", "นางสาวสุนี สวัสดิ์", "นายสมชาย ใจดี",
    "นางสาวลลิตา แสงทอง", "นายวรวิทย์ เก่งการ"
]

SPECIALTIES = ["อายุรกรรม", "กุมารเวชกรรม", "ศัลยกรรม", "จักษุวิทยา", "ทันตกรรม"]
GENDERS = ["male", "female"]

departments = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Pediatrics",
    "Radiology",
    "Oncology",
    "Dermatology",
]

LOCATIONS = [
    {
        "locationId": f"{i:02d}{dept[:3].upper()}",
        "locationName": dept,
        "parentDeptName": f"{dept} Center"
    }
    for i, dept in enumerate(departments)
]

APPOINTMENT_MAP = {
    "00-00-00001": None,
    "00-00-00002": {},
    "00-00-00003": {}
}

def generate_realistic_schedules(location):
    SLOT_TEMPLATES = [
        ("08:00:00", "12:00:00"),  # morning
        ("13:00:00", "16:00:00"),  # afternoon
        ("16:00:00", "20:00:00"),  # evening
    ]

    WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    # choose 3–5 working days
    working_days = random.sample(WEEKDAYS, k=random.randint(3, 5))

    schedules = []
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=30)

    for day in working_days:
        # doctor works 1–3 slots in a day
        num_slots = random.randint(1, 3)
        slots = random.sample(SLOT_TEMPLATES, num_slots)

        for start_time, end_time in slots:
            schedules.append({
                "startDate": str(start_date),
                "endDate": str(end_date),
                "weekDay": day,
                "startTime": start_time,
                "endTime": end_time,
                "locationId": location["locationId"],
                "locationName": location["locationName"],
                "parentDeptName": location["parentDeptName"]
            })

    return schedules

def generate_appointment_for_patient(hn, appointment_date):
    """Generate a single appointment for a patient."""
    en = f"O{random.randint(10,99)}-{random.randint(10,99)}-{random.randint(100000,999999)}"

    # Random time between 8:00 - 15:00
    start_time = datetime.combine(appointment_date, datetime.min.time()) + timedelta(
        hours=random.randint(8, 15)
    )

    # Pick location from LOCATIONS
    location = random.choice(LOCATIONS)

    appt = {
        "hn": hn,
        "en": en,
        "appointmentDatetime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "comment": "",
        "status": "book",
        "location": [
            {
                "locationId": location["locationId"],
                "locationName": location["locationName"],
                "parentDeptName": location["parentDeptName"]
            }
        ]
    }

    # 50% chance include doctor
    if random.choice([True, False]):
        appt["doctorId"] = str(random.randint(1000000, 9999999))
        appt["doctorName"] = random.choice(DOCTOR_NAMES)

    return appt


def generate_schedules(location, num_schedules=2):
    schedules = []
    for _ in range(num_schedules):
        start_date = datetime.now().date() + timedelta(days=random.randint(0, 5))
        start_hour = random.randint(8, 14)

        schedules.append({
            "startDate": str(start_date),
            "endDate": str(start_date + timedelta(days=30)),
            "startTime": f"{start_hour:02d}:00:00",
            "endTime": f"{start_hour+3:02d}:00:00",
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
                    "statusCode": {"type": "integer"},
                    "message": {"type": "string"},
                    "description": {"type": "string"},
                    "data": {"type": "object"}
                }
            }
        }
    }
})
def get_doctor_schedule():
    doctor_id = str(random.randint(1000000, 9999999))
    doctor_name = random.choice(DOCTOR_NAMES)
    gender = random.choice(GENDERS)
    specialty = random.choice(SPECIALTIES)

    # doctor works in 1–2 locations max
    location_list = random.sample(LOCATIONS, k=random.randint(1, 2))

    schedules = []
    for loc in location_list:
        schedules.extend(generate_realistic_schedules(loc))

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
    "description": "ข้อมูลการนัดหมายของผู้ป่วยทั้งหมด",
    "parameters": [
        {
            "name": "appointmentDatetime",
            "in": "query",
            "type": "string",
            "required": True,
            "description": "วันที่นัดหมาย (YYYY-MM-DD)"
        }
    ],
    "responses": {
        200: {
            "description": "Success",
            "schema": {"type": "object"}
        }
    }
})
def get_appointment():
    date_str = request.args.get("appointmentDatetime")

    if not date_str:
        return jsonify({
            "statusCode": 400,
            "message": "Bad request",
            "description": "Missing appointmentDatetime",
            "data": []
        }), 400

    try:
        appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({
            "statusCode": 400,
            "message": "Bad request",
            "description": "Invalid date format, should be YYYY-MM-DD",
            "data": []
        }), 400

    appointments = []

    for patient in PATIENTS:
        hn = patient["hn"]

        # No appointment for this patient
        if APPOINTMENT_MAP[hn] is None:
            continue

        # Generate once
        if APPOINTMENT_MAP[hn] == {}:
            APPOINTMENT_MAP[hn] = generate_appointment_for_patient(hn, appointment_date)

        appointments.append(APPOINTMENT_MAP[hn])

    return jsonify({
        "statusCode": 200,
        "message": "Success",
        "description": "",
        "data": appointments
    })