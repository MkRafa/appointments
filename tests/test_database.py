"""Unit tests for database operations"""

import unittest
import os
from datetime import datetime, timedelta
from models import Patient, Doctor, Clinic, Appointment
from database import AppointmentDatabase

class TestAppointmentDatabase(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Set up test database"""
        self.db = AppointmentDatabase('test_appointments.db')
        self.db.connect()
        self.db.initialize_database()
        self.db.populate_sample_data()
    
    def tearDown(self):
        """Clean up test database"""
        self.db.disconnect()
        if os.path.exists('test_appointments.db'):
            os.remove('test_appointments.db')
    
    def test_add_patient(self):
        """Test adding a patient"""
        patient = Patient(
            patient_id=0,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            date_of_birth="1990-01-01",
            gender="Male",
            address="123 Main St",
            city="New York",
            postal_code="10001"
        )
        
        patient_id = self.db.add_patient(patient)
        self.assertIsNotNone(patient_id)
        self.assertGreater(patient_id, 0)
    
    def test_get_patient_by_email(self):
        """Test retrieving patient by email"""
        patient = Patient(
            patient_id=0,
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            phone="9876543210",
            date_of_birth="1992-05-15",
            gender="Female",
            address="456 Elm St",
            city="Boston",
            postal_code="02101"
        )
        
        self.db.add_patient(patient)
        retrieved = self.db.get_patient_by_email("jane@example.com")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.first_name, "Jane")
        self.assertEqual(retrieved.last_name, "Smith")
    
    def test_get_all_doctors(self):
        """Test retrieving all doctors"""
        doctors = self.db.get_all_doctors()
        self.assertGreater(len(doctors), 0)
    
    def test_get_doctors_by_specialty(self):
        """Test retrieving doctors by specialty"""
        doctors = self.db.get_doctors_by_specialty("General Practice")
        self.assertGreater(len(doctors), 0)
        for doctor in doctors:
            self.assertEqual(doctor.specialty, "General Practice")
    
    def test_get_all_clinics(self):
        """Test retrieving all clinics"""
        clinics = self.db.get_all_clinics()
        self.assertEqual(len(clinics), 3)
    
    def test_get_available_slots(self):
        """Test retrieving available slots"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        slots = self.db.get_available_slots(1, 1, tomorrow)
        self.assertGreater(len(slots), 0)
    
    def test_add_appointment(self):
        """Test adding an appointment"""
        patient = Patient(
            patient_id=0,
            first_name="Bob",
            last_name="Johnson",
            email="bob@example.com",
            phone="5555555555",
            date_of_birth="1985-03-20",
            gender="Male",
            address="789 Oak St",
            city="Chicago",
            postal_code="60601"
        )
        
        patient_id = self.db.add_patient(patient)
        appointment_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        appointment = Appointment(
            appointment_id=0,
            patient_id=patient_id,
            doctor_id=1,
            clinic_id=1,
            appointment_date=appointment_date,
            appointment_time="09:00",
            reason="Checkup"
        )
        
        appt_id = self.db.add_appointment(appointment)
        self.assertIsNotNone(appt_id)
        self.assertGreater(appt_id, 0)
    
    def test_cancel_appointment(self):
        """Test canceling an appointment"""
        patient = Patient(
            patient_id=0,
            first_name="Alice",
            last_name="Brown",
            email="alice@example.com",
            phone="4444444444",
            date_of_birth="1988-07-10",
            gender="Female",
            address="321 Pine St",
            city="Seattle",
            postal_code="98101"
        )
        
        patient_id = self.db.add_patient(patient)
        appointment_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        appointment = Appointment(
            appointment_id=0,
            patient_id=patient_id,
            doctor_id=1,
            clinic_id=1,
            appointment_date=appointment_date,
            appointment_time="10:00",
            reason="Consultation"
        )
        
        appt_id = self.db.add_appointment(appointment)
        result = self.db.cancel_appointment(appt_id)
        self.assertTrue(result)
        
        # Verify status changed
        cancelled_appt = self.db.get_appointment_by_id(appt_id)
        self.assertEqual(cancelled_appt.status, "cancelled")

if __name__ == '__main__':
    unittest.main()
