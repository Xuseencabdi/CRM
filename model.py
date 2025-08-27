from datetime import datetime

class Service:
    def __init__(self, service_id, service_name, description=None, service_time=None):
        self.ServiceId = service_id
        self.ServiceName = service_name
        self.Description = description
        # Store as datetime or None
        if isinstance(service_time, str):
            self.ServiceTime = datetime.fromisoformat(service_time)
        else:
            self.ServiceTime = service_time

    def to_dict(self):
        return {
            'ServiceId': self.ServiceId,
            'ServiceName': self.ServiceName,
            'Description': self.Description,
            'ServiceTime': self.ServiceTime.isoformat() if self.ServiceTime else None
        }


class ServiceManager:
    def __init__(self):
        self.services = []
        self.next_id = 1

    def get_all(self):
        return self.services

    def get_by_id(self, service_id):
        return next((s for s in self.services if s.ServiceId == service_id), None)

    def create(self, service_name, description=None, service_time=None):
        service = Service(self.next_id, service_name, description, service_time)
        self.services.append(service)
        self.next_id += 1
        return service

    def update(self, service_id, service_name=None, description=None, service_time=None):
        service = self.get_by_id(service_id)
        if not service:
            return None
        if service_name is not None:
            service.ServiceName = service_name
        if description is not None:
            service.Description = description
        if service_time is not None:
            if isinstance(service_time, str):
                service.ServiceTime = datetime.fromisoformat(service_time)
            else:
                service.ServiceTime = service_time
        return service

    def delete(self, service_id):
        service = self.get_by_id(service_id)
        if service:
            self.services.remove(service)
            return True
        return False

    def delete_all(self):
        self.services.clear()
