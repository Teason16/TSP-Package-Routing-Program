import csv
import datetime

from DeliveryTruck import DeliveryTruck
from Package import Package
from HashTableWithChaining import ChainingHashTable


# Read the file of package information
with open("C:/Users/taelr/PycharmProjects/TravelingSalesmanTest1/.venv/CSV/Packages.csv") as pack_csv_file:
    CSV_Package = csv.reader(pack_csv_file)
    CSV_Package = list(CSV_Package)

# Read the file of address information
with open("C:/Users/taelr/PycharmProjects/TravelingSalesmanTest1/.venv/CSV/Addresses.csv") as address_csv_file:
    CSV_Address = csv.reader(address_csv_file)
    CSV_Address = list(CSV_Address)

# Read the file of distance information
with open("C:/Users/taelr/PycharmProjects/TravelingSalesmanTest1/.venv/CSV/Distances.csv") as dist_csv_file:
    CSV_Distance = csv.reader(dist_csv_file)
    CSV_Distance = list(CSV_Distance)


# read package and address data from address and package csv files
# create new package objects and insert them into hash table
def Load_newPackage_Obj_Data(hashtable):
    for addressItem in CSV_Address:
        for packageItem in CSV_Package:
            if addressItem[2] in packageItem[1]:
                pID = int(packageItem[0])
                pAddress_ID = int(addressItem[0])
                pAddress_label = addressItem[1]
                pAddress = packageItem[1]
                pCity = packageItem[2]
                pState = packageItem[3]
                pZipcode = packageItem[4]
                pDeadline_time = packageItem[5]
                pWeight = packageItem[6]
                pStatus = "At Hub"

                # new package object
                package = Package(pID, pAddress_ID, pAddress_label, pAddress, pCity, pState, pZipcode, pDeadline_time,
                                  pWeight, pStatus)

                # insert new package object into hash table
                hashtable.insert(pID, package)


# instantiate hash table for package objects
package_hashtable = ChainingHashTable(40)

# load new packages into hashtable
Load_newPackage_Obj_Data(package_hashtable)


# fetch data from package hash table
# display fields in readable format with data labels
def fetch_all_package_data(reference_time):
    print(f"\nAll Package Information @ {reference_time}:")
    # ensure address for package 9 is correct
    if reference_time >= datetime.timedelta(hours=10, minutes=20, seconds=00):
        package_hashtable.search(9).address_label = "Third District Juvenile Court"
        package_hashtable.search(9).address = "410 S State st"
        package_hashtable.search(9).zipcode = "84111"
    for i in range(len(package_hashtable.table)):
        # update package status for all packages
        package_hashtable.search(i+1).current_status(reference_time)
        if package_hashtable.search(i+1).status == "At Hub":
            package_hashtable.search(i+1).truck = None
            package_hashtable.search(i+1).departure_time = None
            package_hashtable.search(i+1).delivery_time = None
        elif package_hashtable.search(i+1).status == "En Route":
            package_hashtable.search(i+1).delivery_time = None
        # display package information
        print("Package ID: {}, Address:({}) {}, {}, {}, {}, DeadLine Time: {}, Weight:{}, Truck: {},"
              "Departure Time: {}, Delivery Time: {}, Status: {}".format(
                package_hashtable.search(i+1).ID, package_hashtable.search(i+1).address_label,
                package_hashtable.search(i+1).address, package_hashtable.search(i+1).city,
                package_hashtable.search(i+1).state, package_hashtable.search(i+1).zipcode,
                package_hashtable.search(i+1).Deadline_time, package_hashtable.search(i+1).weight,
                package_hashtable.search(i+1).truck, package_hashtable.search(i+1).departure_time,
                package_hashtable.search(i+1).delivery_time, package_hashtable.search(i+1).status))


# Fetch Package info for a single package
# Display information with data labels
def print_single_package(reference_time):
    print("\nEnter Package ID Number: ", end="")
    # get package ID from user
    pack_num = int(input())
    # ensure address for package 9 is correct
    if reference_time >= datetime.timedelta(hours=10, minutes=20, seconds=00):
        package_hashtable.search(9).address_label = "Third District Juvenile Court"
        package_hashtable.search(9).address = "410 S State st"
        package_hashtable.search(9).zipcode = "84111"
    # update package status
    package_hashtable.search(pack_num).current_status(reference_time)
    if package_hashtable.search(pack_num).status == "At Hub":
        package_hashtable.search(pack_num).truck = None
        package_hashtable.search(pack_num).departure_time = None
        package_hashtable.search(pack_num).delivery_time = None
    elif package_hashtable.search(pack_num).status == "En Route":
        package_hashtable.search(pack_num).delivery_time = None
    # display package information
    print("\nInformation For Package {} @ {}:".format(pack_num, reference_time))
    print("Package ID: {}, Address:({}) {}, {}, {}, {}, DeadLine Time: {}, Weight:{}, Truck: {}, Departure Time: {}, "
          "Delivery Time: {}, Status:{}".format(
            package_hashtable.search(pack_num).ID,
            package_hashtable.search(pack_num).address_label, package_hashtable.search(pack_num).address,
            package_hashtable.search(pack_num).city, package_hashtable.search(pack_num).state,
            package_hashtable.search(pack_num).zipcode,
            package_hashtable.search(pack_num).Deadline_time, package_hashtable.search(pack_num).weight,
            package_hashtable.search(pack_num).truck, package_hashtable.search(pack_num).departure_time,
            package_hashtable.search(pack_num).delivery_time, package_hashtable.search(pack_num).status))


# find distance between two addresses
def get_distance(addressID_1, addressID_2):
    if CSV_Distance[addressID_1][addressID_2] != "":
        # distance equals value at [1,2]
        distance = CSV_Distance[addressID_1][addressID_2]
    else:
        # distance equals value at [2,1]
        distance = CSV_Distance[addressID_2][addressID_1]
    return float(distance)


# format user-input time
def snapshot_time(time):
    (h, m, s) = time.split(":")
    reference_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    return reference_time


# nearest neighbor algorithm to compute the shortest path for delivering packages
def truck_delivering_route(Delivery_Truck):
    # put all vertices in an unvisited queue
    undelivered = []

    for package in Delivery_Truck.packages:
        # package ID can be used to get address_ID for distance calculation
        undelivered.append(package_hashtable.search(package))
        # update each packages assigned truck attribute
        package_hashtable.search(package).truck = Delivery_Truck.ID
    # clear packages list so items can be re-added in delivered order
    Delivery_Truck.packages.clear()

    # while there are still packages to deliver....
    while len(undelivered) > 0:
        smallest = 100
        current_address = None
        # loop through the packages on the truck
        for p in undelivered:
            # find the closest package delivery address to the trucks current address
            if get_distance(Delivery_Truck.address, p.address_ID) < smallest:
                smallest = get_distance(Delivery_Truck.address, p.address_ID)
                current_address = p
        # add current address to the trucks delivered packages list
        Delivery_Truck.packages.append(current_address)
        # remove the current package from the undelivered list
        undelivered.remove(current_address)
        # increase the trucks mileage by the distance traveled
        Delivery_Truck.mileage += smallest
        # update the trucks address to the current address for the delivered package
        Delivery_Truck.address = current_address.address_ID
        # add the time it took to travel to delivery address to truck.time
        Delivery_Truck.time += datetime.timedelta(hours=smallest / Delivery_Truck.speed)
        # update package status to "on truck"
        current_address.departure_time = Delivery_Truck.depart_time
        # update package delivery time
        current_address.delivery_time = Delivery_Truck.time
    Delivery_Truck.mileage = round(Delivery_Truck.mileage, 4)


# Create truck object truck1
truck1 = DeliveryTruck(1, 16, 18, None, [1, 2, 4, 7, 13, 14, 15, 16, 19, 20, 21, 29, 31, 34, 33, 40], 0.0, 0,
                       datetime.timedelta(hours=8))

# Create truck object truck2
truck2 = DeliveryTruck(2, 16, 18, None, [3, 9, 12, 17, 18, 22, 23, 24, 26, 27, 32, 35, 36, 38, 39], 0.0,
                       0, datetime.timedelta(hours=10, minutes=20))

# Create truck object truck3
# set departure time for after truck 1 returns
truck3 = DeliveryTruck(3, 16, 18, None, [5, 6, 8, 10, 11, 25, 28, 30, 37], 0.0,
                       0, datetime.timedelta(hours=9, minutes=20))


# simulate package delivery for trucks
truck_delivering_route(truck1)
truck_delivering_route(truck2)
truck_delivering_route(truck3)


# -------------- User Interface -------------------------------
class Main:
    # Program Header
    print("\nPackage Routing Program")
    # list user options
    print("\nMain Menu: \n-----------------\nSelect The Number: \n1. Truck & Mileage Information"
          " \n2. All Package Information \n3. Single Package Information \n4. Exit Program")
    try:
        option_1 = int(input())
        # return information for option selected by user
        if option_1 == 1:
            # display truck information
            print("\nTruck 1:\nDeparture Time: {}\nReturn Time: {}\nNumber of Packages: {}\nMileage: {}".format
                  (truck1.depart_time, truck1.time, len(truck1.packages), truck1.mileage))
            print("\nTruck 2:\nDeparture Time: {}\nReturn Time: {}\nNumber of Packages: {}\nMileage: {}".format
                  (truck2.depart_time, truck2.time, len(truck2.packages), truck2.mileage))
            print("\nTruck 3:\nDeparture Time: {}\nReturn Time: {}\nNumber of Packages: {}\nMileage: {}".format
                  (truck3.depart_time, truck3.time, len(truck3.packages), truck3.mileage))
            # display total miles
            print("\nTotal Miles: {}".format(round(truck1.mileage + truck2.mileage + truck3.mileage, 3)))
        elif option_1 == 2:
            # get reference time from user
            user_time = input("Enter A Reference Time (HH:MM:SS): ")
            # get all package details
            fetch_all_package_data(snapshot_time(user_time))

        elif option_1 == 3:
            # get reference time from user
            user_time = input("Enter A Reference Time (HH:MM:SS): ")
            # get single package details
            print_single_package(snapshot_time(user_time))
        else:
            exit()
    except ValueError:
        print("Invalid Entry. Program Terminated.")
        exit()

