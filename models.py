from datetime import datetime
from typing import Optional, List

class Patient:
    """Patient data model"""
    def __init__(self, patient_id: int, first_name: str, last_name: str,
                 email: str, phone: str, date_of_birth: str, gender: str,
                 address: str, city: str, postal_code: str, insurance_id: Optional[str] = None):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address = address
        self.city = city
        self.postal_code = postal_code
        self.insurance_id = insurance_id
        self.created_at = datetime.now()

    def __repr__(self):
        return f"Patient({self.patient_id}, {self.first_name} {self.last_name})"


class Doctor:
    """Doctor data model"""
    def __init__(self, doctor_id: int, first_name: str, last_name: str,
                 specialty: str, license_number: str, phone: str,
                 email: str, years_of_experience: int):
        self.doctor_id = doctor_id
        self.first_name = first_name
        self.last_name = last_name
        self.specialty = specialty
        self.license_number = license_number
        self.phone = phone
        self.email = email
        self.years_of_experience = years_of_experience

    def __repr__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.specialty})"


class Clinic:
    """Clinic data model"""
    def __init__(self, clinic_id: int, name: str, address: str,
                 city: str, state: str, postal_code: str,
                 phone: str, email: str, opening_time: str, closing_time: str):
        self.clinic_id = clinic_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.phone = phone
        self.email = email
        self.opening_time = opening_time
        self.closing_time = closing_time

    def __repr__(self):
        return f"Clinic({self.clinic_id}, {self.name}, {self.city})"


class AvailableSlot:
    """Available appointment slot"""
    def __init__(self, slot_id: int, doctor_id: int, clinic_id: int,
                 date: str, start_time: str, end_time: str, is_available: bool = True):
        self.slot_id = slot_id
        self.doctor_id = doctor_id
        self.clinic_id = clinic_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.is_available = is_available

    def __repr__(self):
        return f"Slot({self.slot_id}, {self.date} {self.start_time}-{self.end_time})"


class Appointment:
    """Appointment data model"""
    def __init__(self, appointment_id: int, patient_id: int, doctor_id: int,
                 clinic_id: int, appointment_date: str, appointment_time: str,
                 reason: str, status: str = "scheduled", notes: Optional[str] = None):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.clinic_id = clinic_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.reason = reason
        self.status = status  # scheduled, completed, cancelled
        self.notes = notes
        self.created_at = datetime.now()
        self.modified_at = datetime.now()

    def __repr__(self):
        return f"Appointment({self.appointment_id}, Patient: {self.patient_id}, {self.appointment_date} {self.appointment_time})"
