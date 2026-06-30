# Clinic Appointment Booking System

A comprehensive clinic appointment booking system that guides patients through the booking process step by step.

## Features

- **Patient Details Collection**: Collects comprehensive patient information
- **Doctor Selection**: Browse available doctors by specialty
- **Clinic Selection**: Choose from multiple clinic locations
- **Date & Time Selection**: Interactive calendar and time slot selection
- **Appointment Management**: View, modify, and cancel appointments
- **Database Storage**: SQLite database with sample clinic data

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

```
appointments/
├── main.py                 # Entry point
├── database.py             # Database initialization and operations
├── models.py               # Data models
├── booking_system.py       # Booking logic
├── utils.py                # Utility functions
├── sample_data.py          # Sample clinic data
└── requirements.txt        # Dependencies
```

## Database Schema

- **Patients**: Patient information
- **Doctors**: Doctor details and specialties
- **Clinics**: Clinic locations
- **Appointments**: Appointment records
- **AvailableSlots**: Doctor availability per clinic
