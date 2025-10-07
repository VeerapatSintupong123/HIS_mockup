from .login import login_bp
from .doctor_schedule import doctor_bp
from .patient import patient_bp

def register_blueprints(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)