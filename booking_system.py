from typing import Optional, List
from datetime import datetime, timedelta
from models import Patient, Appointment
from database import AppointmentDatabase
from utils import (
    print_header, print_success, print_error, print_info, print_section,
    validate_email, validate_phone, validate_date, validate_time, validate_age,
    get_valid_input, get_integer_input, display_list, format_date,
    calculate_age, is_business_hours
)
from sample_data import REASONS_FOR_VISIT

class BookingSystem:
    """Main appointment booking system"""
    
    def __init__(self, db: AppointmentDatabase):
        self.db = db
        self.current_patient: Optional[Patient] = None
        self.current_doctor_id: Optional[int] = None
        self.current_clinic_id: Optional[int] = None
        self.current_slot_id: Optional[int] = None
        self.appointment_reason: Optional[str] = None
    
    def start_booking(self) -> None:
        """Start the appointment booking process"""
        print_header("Welcome to Clinic Appointment Booking System")
        
        # Step 1: Collect patient details
        self.collect_patient_details()
        
        if not self.current_patient:
            print_error("Unable to proceed without patient information")
            return
        
        print_success(f"Patient verified: {self.current_patient.first_name} {self.current_patient.last_name}")
        
        # Step 2: Select clinic
        if not self.select_clinic():
            return
        
        # Step 3: Select doctor
        if not self.select_doctor():
            return
        
        # Step 4: Select date and time
        if not self.select_date_and_time():
            return
        
        # Step 5: Collect appointment reason
        if not self.collect_appointment_reason():
            return
        
        # Step 6: Confirm and book appointment
        self.confirm_and_book_appointment()
    
    def collect_patient_details(self) -> None:
        """Collect patient details step by step"""
        print_section("Step 1: Patient Information")
        print_info("Please provide your personal details")
        
        # Check if patient already exists
        email = get_valid_input("Email address", validate_email)
        existing_patient = self.db.get_patient_by_email(email)
        
        if existing_patient:
            response = input(f"\nPatient found: {existing_patient.first_name} {existing_patient.last_name}. Use this profile? (y/n): ").strip().lower()
            if response == 'y':
                self.current_patient = existing_patient
                return
        
        # Collect new patient details
        first_name = get_valid_input("First name")
        last_name = get_valid_input("Last name")
        phone = get_valid_input("Phone number", validate_phone)
        
        # Date of birth with validation
        while True:
            dob = get_valid_input("Date of birth (YYYY-MM-DD)", validate_date)
            if validate_age(dob):
                break
            print_error("Please enter a valid age (between 0 and 150 years)")
        
        gender = self.select_gender()
        address = get_valid_input("Street address")
        city = get_valid_input("City")
        postal_code = get_valid_input("Postal code")
        insurance_id = input("Insurance ID (optional, press Enter to skip): ").strip() or None
        
        # Create and save patient
        patient = Patient(
            patient_id=0,  # Will be assigned by database
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=dob,
            gender=gender,
            address=address,
            city=city,
            postal_code=postal_code,
            insurance_id=insurance_id
        )
        
        patient_id = self.db.add_patient(patient)
        patient.patient_id = patient_id
        self.current_patient = patient
        print_success(f"Patient profile created successfully (ID: {patient_id})")
    
    def select_gender(self) -> str:
        """Get gender selection"""
        genders = ["Male", "Female", "Other", "Prefer not to say"]
        print_section("Select gender")
        display_list(genders)
        choice = get_integer_input("Select option", 1, len(genders))
        return genders[choice - 1]
    
    def select_clinic(self) -> bool:
        """Select clinic for appointment"""
        print_section("Step 2: Select Clinic")
        clinics = self.db.get_all_clinics()
        
        if not clinics:
            print_error("No clinics available")
            return False
        
        print("Available clinics:")
        for idx, clinic in enumerate(clinics, 1):
            print(f"\n  {idx}. {clinic.name}")
            print(f"     Address: {clinic.address}, {clinic.city}, {clinic.state} {clinic.postal_code}")
            print(f"     Hours: {clinic.opening_time} - {clinic.closing_time}")
            print(f"     Phone: {clinic.phone}")
        
        choice = get_integer_input("\nSelect clinic", 1, len(clinics))
        selected_clinic = clinics[choice - 1]
        self.current_clinic_id = selected_clinic.clinic_id
        print_success(f"Clinic selected: {selected_clinic.name}")
        return True
    
    def select_doctor(self) -> bool:
        """Select doctor at clinic"""
        print_section("Step 3: Select Doctor")
        
        # Get doctors at selected clinic
        doctors = self.db.get_doctors_in_clinic(self.current_clinic_id)
        
        if not doctors:
            print_error("No doctors available at this clinic")
            return False
        
        # Ask if user wants to filter by specialty
        response = input("Would you like to filter doctors by specialty? (y/n): ").strip().lower()
        
        if response == 'y':
            specialties = sorted(set(doc.specialty for doc in doctors))
            print("\nAvailable specialties at this clinic:")
            display_list(specialties)
            choice = get_integer_input("Select specialty", 1, len(specialties))
            selected_specialty = specialties[choice - 1]
            doctors = [doc for doc in doctors if doc.specialty == selected_specialty]
        
        print("\nAvailable doctors:")
        for idx, doctor in enumerate(doctors, 1):
            print(f"\n  {idx}. Dr. {doctor.first_name} {doctor.last_name}")
            print(f"     Specialty: {doctor.specialty}")
            print(f"     Experience: {doctor.years_of_experience} years")
            print(f"     License: {doctor.license_number}")
        
        choice = get_integer_input("\nSelect doctor", 1, len(doctors))
        selected_doctor = doctors[choice - 1]
        self.current_doctor_id = selected_doctor.doctor_id
        print_success(f"Doctor selected: Dr. {selected_doctor.first_name} {selected_doctor.last_name}")
        return True
    
    def select_date_and_time(self) -> bool:
        """Select appointment date and time"""
        print_section("Step 4: Select Date and Time")
        
        # Get available dates
        available_dates = self.db.get_available_dates(self.current_doctor_id, self.current_clinic_id)
        
        if not available_dates:
            print_error("No available dates for this doctor at this clinic")
            return False
        
        print("\nAvailable dates:")
        display_list([format_date(date) for date in available_dates])
        
        choice = get_integer_input("\nSelect date", 1, len(available_dates))
        selected_date = available_dates[choice - 1]
        print_success(f"Date selected: {format_date(selected_date)}")
        
        # Get available times
        available_slots = self.db.get_available_slots(self.current_doctor_id, self.current_clinic_id, selected_date)
        
        if not available_slots:
            print_error("No available time slots for the selected date")
            return False
        
        print("\nAvailable time slots:")
        for idx, slot in enumerate(available_slots, 1):
            print(f"  {idx}. {slot.start_time} - {slot.end_time}")
        
        choice = get_integer_input("\nSelect time slot", 1, len(available_slots))
        selected_slot = available_slots[choice - 1]
        self.current_slot_id = selected_slot.slot_id
        print_success(f"Time slot selected: {selected_slot.start_time} - {selected_slot.end_time}")
        return True
    
    def collect_appointment_reason(self) -> bool:
        """Collect reason for appointment"""
        print_section("Step 5: Appointment Details")
        print("Reason for visit:")
        display_list(REASONS_FOR_VISIT)
        
        choice = get_integer_input("Select reason", 1, len(REASONS_FOR_VISIT))
        selected_reason = REASONS_FOR_VISIT[choice - 1]
        
        if selected_reason == "Other":
            self.appointment_reason = get_valid_input("Please specify the reason")
        else:
            self.appointment_reason = selected_reason
        
        print_success(f"Reason recorded: {self.appointment_reason}")
        return True
    
    def confirm_and_book_appointment(self) -> None:
        """Confirm and book the appointment"""
        print_section("Step 6: Confirmation and Booking")
        
        # Get all details
        doctor = self.db.get_doctor_by_id(self.current_doctor_id)
        clinic = self.db.get_clinic_by_id(self.current_clinic_id)
        slot = self.db.cursor.execute('SELECT * FROM available_slots WHERE slot_id = ?', (self.current_slot_id,)).fetchone()
        
        # Display appointment summary
        print("\n" + "="*60)
        print("APPOINTMENT SUMMARY".center(60))
        print("="*60)
        print(f"Patient: {self.current_patient.first_name} {self.current_patient.last_name}")
        print(f"Email: {self.current_patient.email}")
        print(f"Phone: {self.current_patient.phone}")
        print(f"\nDoctor: Dr. {doctor.first_name} {doctor.last_name}")
        print(f"Specialty: {doctor.specialty}")
        print(f"\nClinic: {clinic.name}")
        print(f"Address: {clinic.address}, {clinic.city}, {clinic.state} {clinic.postal_code}")
        print(f"\nDate: {format_date(slot[3])}")
        print(f"Time: {slot[4]} - {slot[5]}")
        print(f"Reason: {self.appointment_reason}")
        print("="*60 + "\n")
        
        # Confirm booking
        response = input("Confirm and book this appointment? (y/n): ").strip().lower()
        
        if response == 'y':
            # Book the slot
            if self.db.book_slot(self.current_slot_id):
                # Create appointment
                appointment = Appointment(
                    appointment_id=0,
                    patient_id=self.current_patient.patient_id,
                    doctor_id=self.current_doctor_id,
                    clinic_id=self.current_clinic_id,
                    appointment_date=slot[3],
                    appointment_time=slot[4],
                    reason=self.appointment_reason,
                    status="scheduled"
                )
                
                appointment_id = self.db.add_appointment(appointment)
                print_success(f"Appointment booked successfully! (Booking ID: {appointment_id})")
                print_info(f"A confirmation has been sent to {self.current_patient.email}")
            else:
                print_error("Failed to book appointment. Please try again.")
        else:
            print_info("Booking cancelled")
    
    def view_patient_appointments(self, patient_id: int) -> None:
        """View all appointments for a patient"""
        print_header("Your Appointments")
        
        appointments = self.db.get_patient_appointments(patient_id)
        
        if not appointments:
            print_info("You have no appointments")
            return
        
        for idx, appt in enumerate(appointments, 1):
            doctor = self.db.get_doctor_by_id(appt.doctor_id)
            clinic = self.db.get_clinic_by_id(appt.clinic_id)
            
            print(f"\n{idx}. Appointment ID: {appt.appointment_id}")
            print(f"   Doctor: Dr. {doctor.first_name} {doctor.last_name} ({doctor.specialty})")
            print(f"   Clinic: {clinic.name}")
            print(f"   Date: {format_date(appt.appointment_date)}")
            print(f"   Time: {appt.appointment_time}")
            print(f"   Reason: {appt.reason}")
            print(f"   Status: {appt.status.upper()}")
    
    def cancel_appointment(self, appointment_id: int) -> bool:
        """Cancel an appointment"""
        appt = self.db.get_appointment_by_id(appointment_id)
        
        if not appt:
            print_error("Appointment not found")
            return False
        
        if appt.status == "cancelled":
            print_info("This appointment is already cancelled")
            return False
        
        response = input(f"Are you sure you want to cancel appointment {appointment_id}? (y/n): ").strip().lower()
        
        if response == 'y':
            if self.db.cancel_appointment(appointment_id):
                print_success("Appointment cancelled successfully")
                return True
            else:
                print_error("Failed to cancel appointment")
                return False
        
        return False
