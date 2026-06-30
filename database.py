import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from models import Patient, Doctor, Clinic, AvailableSlot, Appointment
from sample_data import CLINICS, DOCTORS, DOCTOR_CLINIC_ASSIGNMENTS, DEFAULT_TIME_SLOTS

class AppointmentDatabase:
    """Database handler for appointment system"""
    
    def __init__(self, db_path: str = 'appointments.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self) -> None:
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def disconnect(self) -> None:
        """Disconnect from database"""
        if self.conn:
            self.conn.close()
    
    def initialize_database(self) -> None:
        """Create all necessary tables"""
        self.connect()
        
        # Patients table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                gender TEXT NOT NULL,
                address TEXT,
                city TEXT,
                postal_code TEXT,
                insurance_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Doctors table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                license_number TEXT UNIQUE NOT NULL,
                phone TEXT,
                email TEXT,
                years_of_experience INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Clinics table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clinics (
                clinic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                city TEXT,
                state TEXT,
                postal_code TEXT,
                phone TEXT,
                email TEXT,
                opening_time TEXT,
                closing_time TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Doctor-Clinic assignments
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctor_clinic_assignments (
                assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                clinic_id INTEGER NOT NULL,
                FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id),
                FOREIGN KEY(clinic_id) REFERENCES clinics(clinic_id),
                UNIQUE(doctor_id, clinic_id)
            )
        ''')
        
        # Available slots
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS available_slots (
                slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                clinic_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                is_available BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id),
                FOREIGN KEY(clinic_id) REFERENCES clinics(clinic_id)
            )
        ''')
        
        # Appointments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                clinic_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id),
                FOREIGN KEY(clinic_id) REFERENCES clinics(clinic_id)
            )
        ''')
        
        self.conn.commit()
    
    def populate_sample_data(self) -> None:
        """Populate database with sample data"""
        # Add clinics
        for clinic in CLINICS:
            try:
                self.cursor.execute('''
                    INSERT INTO clinics (clinic_id, name, address, city, state, postal_code, phone, email, opening_time, closing_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    clinic['clinic_id'], clinic['name'], clinic['address'],
                    clinic['city'], clinic['state'], clinic['postal_code'],
                    clinic['phone'], clinic['email'], clinic['opening_time'],
                    clinic['closing_time']
                ))
            except sqlite3.IntegrityError:
                pass
        
        # Add doctors
        for doctor in DOCTORS:
            try:
                self.cursor.execute('''
                    INSERT INTO doctors (doctor_id, first_name, last_name, specialty, license_number, phone, email, years_of_experience)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    doctor['doctor_id'], doctor['first_name'], doctor['last_name'],
                    doctor['specialty'], doctor['license_number'], doctor['phone'],
                    doctor['email'], doctor['years_of_experience']
                ))
            except sqlite3.IntegrityError:
                pass
        
        # Add doctor-clinic assignments
        for assignment in DOCTOR_CLINIC_ASSIGNMENTS:
            try:
                self.cursor.execute('''
                    INSERT INTO doctor_clinic_assignments (doctor_id, clinic_id)
                    VALUES (?, ?)
                ''', (assignment['doctor_id'], assignment['clinic_id']))
            except sqlite3.IntegrityError:
                pass
        
        # Generate available slots for next 30 days
        self._generate_available_slots()
        
        self.conn.commit()
    
    def _generate_available_slots(self) -> None:
        """Generate available slots for all doctor-clinic combinations"""
        from sample_data import DEFAULT_TIME_SLOTS
        
        today = datetime.now()
        start_date = today + timedelta(days=1)
        end_date = today + timedelta(days=30)
        
        current_date = start_date
        slot_id = 1
        
        while current_date <= end_date:
            # Skip weekends
            if current_date.weekday() < 5:  # Monday=0 to Friday=4
                date_str = current_date.strftime('%Y-%m-%d')
                
                # Add slots for each doctor-clinic assignment
                for assignment in DOCTOR_CLINIC_ASSIGNMENTS:
                    for time_slot in DEFAULT_TIME_SLOTS:
                        # Calculate end time (30 minutes after start)
                        start_dt = datetime.strptime(time_slot, '%H:%M')
                        end_dt = start_dt + timedelta(minutes=30)
                        end_time = end_dt.strftime('%H:%M')
                        
                        try:
                            self.cursor.execute('''
                                INSERT INTO available_slots (slot_id, doctor_id, clinic_id, date, start_time, end_time, is_available)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                slot_id, assignment['doctor_id'], assignment['clinic_id'],
                                date_str, time_slot, end_time, True
                            ))
                            slot_id += 1
                        except sqlite3.IntegrityError:
                            pass
            
            current_date += timedelta(days=1)
    
    # Patient operations
    def add_patient(self, patient: Patient) -> int:
        """Add new patient to database"""
        self.cursor.execute('''
            INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, address, city, postal_code, insurance_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient.first_name, patient.last_name, patient.email, patient.phone,
            patient.date_of_birth, patient.gender, patient.address, patient.city,
            patient.postal_code, patient.insurance_id
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_patient_by_email(self, email: str) -> Optional[Patient]:
        """Retrieve patient by email"""
        self.cursor.execute('SELECT * FROM patients WHERE email = ?', (email,))
        row = self.cursor.fetchone()
        if row:
            return Patient(*row[1:])
        return None
    
    def get_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        """Retrieve patient by ID"""
        self.cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
        row = self.cursor.fetchone()
        if row:
            patient = Patient(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            return patient
        return None
    
    # Doctor operations
    def get_all_doctors(self) -> List[Doctor]:
        """Get all doctors"""
        self.cursor.execute('SELECT * FROM doctors ORDER BY last_name')
        doctors = []
        for row in self.cursor.fetchall():
            doctor = Doctor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            doctors.append(doctor)
        return doctors
    
    def get_doctors_by_specialty(self, specialty: str) -> List[Doctor]:
        """Get doctors by specialty"""
        self.cursor.execute('SELECT * FROM doctors WHERE specialty = ? ORDER BY last_name', (specialty,))
        doctors = []
        for row in self.cursor.fetchall():
            doctor = Doctor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            doctors.append(doctor)
        return doctors
    
    def get_doctors_in_clinic(self, clinic_id: int) -> List[Doctor]:
        """Get doctors available in a specific clinic"""
        self.cursor.execute('''
            SELECT d.* FROM doctors d
            JOIN doctor_clinic_assignments dca ON d.doctor_id = dca.doctor_id
            WHERE dca.clinic_id = ?
            ORDER BY d.last_name
        ''', (clinic_id,))
        doctors = []
        for row in self.cursor.fetchall():
            doctor = Doctor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            doctors.append(doctor)
        return doctors
    
    def get_doctor_by_id(self, doctor_id: int) -> Optional[Doctor]:
        """Get doctor by ID"""
        self.cursor.execute('SELECT * FROM doctors WHERE doctor_id = ?', (doctor_id,))
        row = self.cursor.fetchone()
        if row:
            return Doctor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        return None
    
    def get_specialties(self) -> List[str]:
        """Get all unique specialties"""
        self.cursor.execute('SELECT DISTINCT specialty FROM doctors ORDER BY specialty')
        return [row[0] for row in self.cursor.fetchall()]
    
    # Clinic operations
    def get_all_clinics(self) -> List[Clinic]:
        """Get all clinics"""
        self.cursor.execute('SELECT * FROM clinics ORDER BY name')
        clinics = []
        for row in self.cursor.fetchall():
            clinic = Clinic(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            clinics.append(clinic)
        return clinics
    
    def get_clinic_by_id(self, clinic_id: int) -> Optional[Clinic]:
        """Get clinic by ID"""
        self.cursor.execute('SELECT * FROM clinics WHERE clinic_id = ?', (clinic_id,))
        row = self.cursor.fetchone()
        if row:
            return Clinic(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        return None
    
    # Available slots operations
    def get_available_slots(self, doctor_id: int, clinic_id: int, date: str) -> List[AvailableSlot]:
        """Get available slots for a doctor at a clinic on a specific date"""
        self.cursor.execute('''
            SELECT * FROM available_slots
            WHERE doctor_id = ? AND clinic_id = ? AND date = ? AND is_available = TRUE
            ORDER BY start_time
        ''', (doctor_id, clinic_id, date))
        slots = []
        for row in self.cursor.fetchall():
            slot = AvailableSlot(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            slots.append(slot)
        return slots
    
    def get_available_dates(self, doctor_id: int, clinic_id: int) -> List[str]:
        """Get available dates for a doctor at a clinic"""
        self.cursor.execute('''
            SELECT DISTINCT date FROM available_slots
            WHERE doctor_id = ? AND clinic_id = ? AND is_available = TRUE
            ORDER BY date
        ''', (doctor_id, clinic_id))
        return [row[0] for row in self.cursor.fetchall()]
    
    def book_slot(self, slot_id: int) -> bool:
        """Mark slot as booked"""
        self.cursor.execute('UPDATE available_slots SET is_available = FALSE WHERE slot_id = ?', (slot_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    # Appointment operations
    def add_appointment(self, appointment: Appointment) -> int:
        """Add new appointment"""
        self.cursor.execute('''
            INSERT INTO appointments (patient_id, doctor_id, clinic_id, appointment_date, appointment_time, reason, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            appointment.patient_id, appointment.doctor_id, appointment.clinic_id,
            appointment.appointment_date, appointment.appointment_time,
            appointment.reason, appointment.status, appointment.notes
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_patient_appointments(self, patient_id: int) -> List[Appointment]:
        """Get all appointments for a patient"""
        self.cursor.execute('''
            SELECT * FROM appointments
            WHERE patient_id = ?
            ORDER BY appointment_date DESC, appointment_time DESC
        ''', (patient_id,))
        appointments = []
        for row in self.cursor.fetchall():
            appt = Appointment(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            appointments.append(appt)
        return appointments
    
    def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Get appointment by ID"""
        self.cursor.execute('SELECT * FROM appointments WHERE appointment_id = ?', (appointment_id,))
        row = self.cursor.fetchone()
        if row:
            return Appointment(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        return None
    
    def cancel_appointment(self, appointment_id: int) -> bool:
        """Cancel an appointment"""
        self.cursor.execute('''
            UPDATE appointments
            SET status = 'cancelled', modified_at = CURRENT_TIMESTAMP
            WHERE appointment_id = ?
        ''', (appointment_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def update_appointment(self, appointment_id: int, **kwargs) -> bool:
        """Update appointment details"""
        allowed_fields = ['reason', 'notes', 'status']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        updates['modified_at'] = datetime.now().isoformat()
        
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [appointment_id]
        
        self.cursor.execute(f'UPDATE appointments SET {set_clause} WHERE appointment_id = ?', values)
        self.conn.commit()
        return self.cursor.rowcount > 0
