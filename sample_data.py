"""Sample clinic data for the appointment system"""

CLINICS = [
    {
        "clinic_id": 1,
        "name": "Central Medical Clinic",
        "address": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "phone": "+1-212-555-0101",
        "email": "info@centralmedical.com",
        "opening_time": "08:00",
        "closing_time": "18:00"
    },
    {
        "clinic_id": 2,
        "name": "Westside Health Center",
        "address": "456 Park Avenue",
        "city": "New York",
        "state": "NY",
        "postal_code": "10022",
        "phone": "+1-212-555-0202",
        "email": "info@westsidehealth.com",
        "opening_time": "07:30",
        "closing_time": "19:00"
    },
    {
        "clinic_id": 3,
        "name": "East River Family Medicine",
        "address": "789 First Avenue",
        "city": "New York",
        "state": "NY",
        "postal_code": "10065",
        "phone": "+1-212-555-0303",
        "email": "info@eastriverfamily.com",
        "opening_time": "08:30",
        "closing_time": "17:30"
    }
]

DOCTORS = [
    {
        "doctor_id": 1,
        "first_name": "James",
        "last_name": "Smith",
        "specialty": "General Practice",
        "license_number": "LIC001234",
        "phone": "+1-212-555-1001",
        "email": "james.smith@medicalclinic.com",
        "years_of_experience": 15
    },
    {
        "doctor_id": 2,
        "first_name": "Sarah",
        "last_name": "Johnson",
        "specialty": "Cardiology",
        "license_number": "LIC001235",
        "phone": "+1-212-555-1002",
        "email": "sarah.johnson@medicalclinic.com",
        "years_of_experience": 12
    },
    {
        "doctor_id": 3,
        "first_name": "Michael",
        "last_name": "Chen",
        "specialty": "Orthopedics",
        "license_number": "LIC001236",
        "phone": "+1-212-555-1003",
        "email": "michael.chen@medicalclinic.com",
        "years_of_experience": 18
    },
    {
        "doctor_id": 4,
        "first_name": "Emily",
        "last_name": "Williams",
        "specialty": "Dermatology",
        "license_number": "LIC001237",
        "phone": "+1-212-555-1004",
        "email": "emily.williams@medicalclinic.com",
        "years_of_experience": 10
    },
    {
        "doctor_id": 5,
        "first_name": "Robert",
        "last_name": "Martinez",
        "specialty": "Neurology",
        "license_number": "LIC001238",
        "phone": "+1-212-555-1005",
        "email": "robert.martinez@medicalclinic.com",
        "years_of_experience": 14
    },
    {
        "doctor_id": 6,
        "first_name": "Lisa",
        "last_name": "Anderson",
        "specialty": "Pediatrics",
        "license_number": "LIC001239",
        "phone": "+1-212-555-1006",
        "email": "lisa.anderson@medicalclinic.com",
        "years_of_experience": 11
    },
    {
        "doctor_id": 7,
        "first_name": "David",
        "last_name": "Thompson",
        "specialty": "General Practice",
        "license_number": "LIC001240",
        "phone": "+1-212-555-1007",
        "email": "david.thompson@medicalclinic.com",
        "years_of_experience": 20
    },
    {
        "doctor_id": 8,
        "first_name": "Jennifer",
        "last_name": "Lee",
        "specialty": "Ophthalmology",
        "license_number": "LIC001241",
        "phone": "+1-212-555-1008",
        "email": "jennifer.lee@medicalclinic.com",
        "years_of_experience": 13
    }
]

# Doctor-Clinic associations
DOCTOR_CLINIC_ASSIGNMENTS = [
    {"doctor_id": 1, "clinic_id": 1},
    {"doctor_id": 2, "clinic_id": 1},
    {"doctor_id": 3, "clinic_id": 2},
    {"doctor_id": 4, "clinic_id": 2},
    {"doctor_id": 5, "clinic_id": 3},
    {"doctor_id": 6, "clinic_id": 3},
    {"doctor_id": 1, "clinic_id": 2},
    {"doctor_id": 7, "clinic_id": 1},
    {"doctor_id": 8, "clinic_id": 2},
]

# Sample time slots (in 30-minute intervals)
DEFAULT_TIME_SLOTS = [
    "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
    "13:00", "13:30", "14:00", "14:30", "15:00", "15:30",
    "16:00", "16:30", "17:00"
]

REASONS_FOR_VISIT = [
    "Routine Checkup",
    "Follow-up Appointment",
    "Acute Illness",
    "Chronic Disease Management",
    "Preventive Care",
    "Consultation",
    "Post-operative Follow-up",
    "Vaccination",
    "Physical Examination",
    "Other"
]
