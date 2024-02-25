# Create class for packages
class Package:
    def __init__(self, ID, address_ID, address_label, address, city, state, zipcode, Deadline_time, weight, status):
        self.ID = ID
        self.address_ID = address_ID
        self.address_label = address_label
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.truck = None

    def __str__(self):
        return ("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
                % (self.ID, self.address_ID, self.address_label, self.address, self.city, self.state, self.zipcode,
                    self.Deadline_time, self.weight, self.truck, self.delivery_time, self.status))

    def current_status(self, checked_time):
        if self.delivery_time < checked_time:
            self.status = "Delivered"
        elif self.departure_time < checked_time:
            self.status = "En Route"
        else:
            self.status = "At Hub"


