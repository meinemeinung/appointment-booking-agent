import datetime as dt
import csv
import pandas as pd
from .appointment_manager import AppointmentManager

class CSVAppointmentManager(AppointmentManager):
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def __read_csv_file(self):
        appointment = pd.read_csv(self.csv_path)
        appointment['Date'] = pd.to_datetime(appointment['Date'], format='%Y-%m-%d')
        appointment['Start'] = appointment['Date'].dt.strftime('%Y-%m-%d') + ' ' + appointment['Start']
        appointment['End'] = appointment['Date'].dt.strftime('%Y-%m-%d') + ' ' + appointment['End']

        for col in ['Date', 'Start', 'End']:
            appointment[col] = pd.to_datetime(appointment[col])
        
        return appointment

    def is_appointment_slot_available(self, start: dt.datetime, end: dt.datetime) -> bool:
        appointment = self.__read_csv_file()

        return ((appointment['Start'] >= end) | (appointment['End'] <= start)).all()

    def create_appointment(self, entity: str, start: dt.datetime, end: dt.datetime):
        if self.is_appointment_slot_available(start, end):
            if entity:
                date_str = start.strftime('%Y-%m-%d')
                with open(self.csv_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    start_time, end_time = start.strftime('%H:%M:%S'), end.strftime('%H:%M:%S')
                    writer.writerow([entity, date_str, start_time, end_time])
                return (0, f"Appointment booked for {entity} on {date_str} from {start_time} to {end_time}.")
            else:
                return (1, "Please specify who you would like to book an appointment for.")
        else:
            return (2, "The time slot is not available. Please choose a different time.")

    def read_appointment(self, date: dt.datetime):
        appointment = self.__read_csv_file()
        appointment_date = appointment[appointment['Date']==date].drop(columns=['Name'], axis=1)
        return appointment_date
    