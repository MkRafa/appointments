#!/usr/bin/env python3
"""Main entry point for Clinic Appointment Booking System"""

import os
from colorama import Fore, Style
from database import AppointmentDatabase
from booking_system import BookingSystem
from utils import print_header, print_success, print_error, print_info, clear_screen

def main_menu() -> None:
    """Display main menu and handle user choices"""
    db = AppointmentDatabase()
    
    # Initialize database if needed
    if not os.path.exists('appointments.db'):
        print_info("Initializing database...")
        db.connect()
        db.initialize_database()
        db.populate_sample_data()
        print_success("Database initialized with sample data")
    else:
        db.connect()
    
    while True:
        clear_screen()
        print_header("Clinic Appointment System")
        
        print(f"{Fore.CYAN}Main Menu:{Style.RESET_ALL}")
        print("  1. Book New Appointment")
        print("  2. View My Appointments")
        print("  3. Cancel Appointment")
        print("  4. About the System")
        print("  5. Exit")
        
        try:
            choice = input(f"\n{Fore.CYAN}Select an option (1-5):{Style.RESET_ALL} ").strip()
            
            if choice == '1':
                booking_system = BookingSystem(db)
                booking_system.start_booking()
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                email = input("\nEnter your email address: ").strip()
                patient = db.get_patient_by_email(email)
                
                if patient:
                    booking_system = BookingSystem(db)
                    booking_system.view_patient_appointments(patient.patient_id)
                    input("\nPress Enter to continue...")
                else:
                    print_error("Patient not found")
                    input("\nPress Enter to continue...")
            
            elif choice == '3':
                email = input("\nEnter your email address: ").strip()
                patient = db.get_patient_by_email(email)
                
                if patient:
                    appointments = db.get_patient_appointments(patient.patient_id)
                    
                    if appointments:
                        print("\nYour appointments:")
                        for idx, appt in enumerate(appointments, 1):
                            if appt.status != "cancelled":
                                print(f"  {idx}. ID: {appt.appointment_id} - {appt.appointment_date} {appt.appointment_time}")
                        
                        try:
                            appt_id = int(input("\nEnter appointment ID to cancel: ").strip())
                            booking_system = BookingSystem(db)
                            booking_system.cancel_appointment(appt_id)
                        except ValueError:
                            print_error("Invalid appointment ID")
                    else:
                        print_info("No appointments found")
                    
                    input("\nPress Enter to continue...")
                else:
                    print_error("Patient not found")
                    input("\nPress Enter to continue...")
            
            elif choice == '4':
                show_about()
                input("\nPress Enter to continue...")
            
            elif choice == '5':
                print_success("Thank you for using Clinic Appointment System!")
                db.disconnect()
                break
            
            else:
                print_error("Invalid choice. Please try again.")
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n")
            response = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if response == 'y':
                print_success("Goodbye!")
                db.disconnect()
                break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input("\nPress Enter to continue...")

def show_about() -> None:
    """Display about information"""
    print_header("About the System")
    print("""
    Clinic Appointment Booking System v1.0
    
    This system allows patients to:
    • Register or login to their profile
    • Browse available clinics
    • Select preferred doctors
    • Choose convenient appointment dates and times
    • Book appointments online
    • View and manage their appointments
    • Cancel appointments if needed
    
    Features:
    ✓ Comprehensive patient information collection
    ✓ Multiple clinic locations with extended hours
    ✓ Diverse range of medical specialties
    ✓ Real-time slot availability
    ✓ Email confirmation (simulated)
    ✓ Appointment history tracking
    
    Sample Data:
    • 3 clinic locations across New York
    • 8 doctors with different specialties
    • 30 days of available appointments
    • 30-minute appointment slots
    
    For support, contact: support@clinicappointments.com
    """)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program interrupted{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {str(e)}{Style.RESET_ALL}")
