from abc import ABC, abstractmethod

class AppointmentManager(ABC):
    @abstractmethod
    def is_appointment_slot_available(self, date, start, end):
        pass

    @abstractmethod
    def create_appointment(self, entity, start, end):
        pass

    @abstractmethod
    def read_appointment(self, date):
        pass