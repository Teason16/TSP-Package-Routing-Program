# Create class for delivery trucks
class DeliveryTruck:
    def __init__(self, ID, capacity, speed, load, packages, mileage, address, depart_time):
        self.ID = int(ID)
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.capacity, self.speed, self.load, self.packages,
                                                   self.mileage, self.address, self.depart_time)

