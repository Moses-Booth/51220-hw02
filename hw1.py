from datetime import date, datetime

def choose_datetimes():
    """
    Function that allows user to select dates and times of reservation

    Output: start time and end time as datetime objects
    """
    print("Choose the date of your reservation")
    print("Weekday: 09:00 - 18:00, Saturday: 10:00 - 16:00, Sunday: closed")
    reservation_date = input("Enter the date (mm/dd/yyyy): ")
    mm, dd, yyyy = reservation_date.split("/")
    mm, dd, yyyy = int(mm), int(dd), int(yyyy)
    reserv_date = date(yyyy, mm, dd)

    start = input("Enter the start time of your reservation (e.g. 09:30): ")
    hr, min = start.split(":")
    start = datetime(yyyy, mm, dd, int(hr), int(min))

    end = input("Enter the end time of your reservation (e.g. 13:00): ")
    hr, min = end.split(":")
    end = datetime(yyyy, mm, dd, int(hr), int(min))

    return reserv_date, start, end

def machines_available(machine, reserv, start, end):
    """
    Function that determines if machines are available for reservation

    Input:
    - machine: type of machine that has been requested for reservation
    - reserv: list of reservations
    - start: reservation start time request
    - end: reservation end time request

    Output: True if machines are available for reservation
    """
    avail = True
    scanners_used = 0
    for record in reserv:

        record_occupied = not (start <= record["end"] and end >= record["start"])

        if record["machine"] == machine:

            if record_occupied:
                avail = False
                print("The machine is occupied that time.")
                break
        
        # special requirements, when machine is a scanner
        if machine[0] == "a" and record["machine"][0] == "a":

            if record_occupied:
                scanners_used += 1
        
        if machine[0] == "a" and record["machine"][0] == "c":

            if record_occupied:
                avail = False
                print("Sorry. A 1.21 gigawatt lightning harvester occupies the power at that time.")
                break
    
    if scanners_used > 2:
        avail = False
        print("Sorry. There're already 3 scanners running at that time.")
    
    return avail

def get_charges(machine, hours, reserv_date):
    """
    Function that calculates charges for machine usage

    Input:
    - machine: machine type
    - hours: total hours the machine is needed for
    - reserv_date: date of reservation request

    Output: total cost of using machine for specified hours
    """
    if machine[0] == "a":
        total = 990 * hours
    elif machine[0] == "b":
        total = 1000 * hours
    elif machine[0] == "c":
        total = 88000

    if discount_available(reserv_date):
            total = total * 0.75
    
    return total

def discount_available(reserv_date):
    """
    Function that determines if discount is applicable

    Input: reservation date requested
    Output: True if a discount can be applied
    """
    today = str(date.today())
    c_yyyy, c_mm, c_dd = today.split("-")
    today = date(int(c_yyyy), int(c_mm), int(c_dd))
    day = (reserv_date-today).days
    return day > 13

def make_reservation(reserv, transac, reservation_id):
    """
    Function that allows user to make a reservation

    Input: 
    - reserv: list of reservations
    - transac: list of transactions
    - reservation_id: current reservation identifier

    Output: creates a reservation and adds it to the reservation list
    """

    # set the machine type and no, represented by "a1" or "b2" etc.
    print("a. multi-phasic radiation scanner")
    print("b. ore scooper")
    print("c. 1.21 gigawatt lightning harvester")

    machine = input("Choose the machine type you want (enter a, b, or c): ")

    if machine != "c":
        no = input("Choose the scanner no. you want (enter number 1~4): ")
        machine = machine + no
    else:
        machine = "c1"

    reserv_date, start_time, end_time = choose_datetimes()

    # handle payment when available
    if machines_available(machine, reserv, start_time, end_time):

        name = input("Enter you name: ")
        today = str(date.today())
        hours = (end_time - start_time).total_seconds()/3600
        total_charges = get_charges(machine, hours, reserv_date)
        reservation_id += 1

        record = {
        "id": reservation_id, 
        "machine": machine, 
        "start": start_time, 
        "end": end_time, 
        "customer": name, 
        "fee": total_charges
        }

        reserv.append(record)
        print(f"The reservation is made! Your reservation id is {reservation_id}. Your down payment cost is ${total_charges*0.5}. Your total cost is ${total_charges}.")

        transaction = {
            "machine": machine, 
            "date": today, 
            "customer": name, 
            "fee": total_charges, 
            "type": "make reservation"
            }
        transac.append(transaction)

def cancel_reservation(reserv, transac):
    """
    Function that allows user to cancel reservation

    Input: 
    - reserv: list of reservations
    - transac: list of transactions

    Output: cancels a reservation and removes it from the input lists
    """
    
    id = input("Enter your reservation id: ")
    for i in range(len(reserv)):

        if reserv[i]["id"] == int(id):

            fee = reserv[i]["fee"]

            # check the day difference
            today = str(date.today())
            c_yyyy, c_mm, c_dd = today.split("-")
            date1 = datetime(int(c_yyyy), int(c_mm), int(c_dd), 10, 0)
            date2 = reserv[i]["start"]
            day = (date2-date1).days

            refund = 0
            if day > 6:
                refund = fee * 0.5 * 0.75
            elif day > 1:
                refund = fee * 0.5 * 0.5
            
            # add to the transaction
            c_date = date(int(c_yyyy), int(c_mm), int(c_dd))
            record = {
                "machine": reserv[i]["machine"], 
                "date": c_date, 
                "customer": reserv[i]["customer"], 
                "fee": refund, 
                "type": "cancel reservation"
                }
            transac.append(record)
            
            del reserv[i]
            print(f"You reservation {id} has been canceled. The refund is ${refund}.")
            break

def find_reservation(reserv):
    """
    Function that allows user to find a specific reservation

    Input:
    - list of reservations

    Output: reservations that fall under the search criteria specified by the user
    """
    print("1. By date range")
    print("2. By customer & date range")
    print("3. By machine & date range")
    inp = input("Choose your filter (enter number 1~3): ")

    # List the current reservations for any given date range
    if inp == "1":

        start = get_startdate()
        end = get_enddate()

        for record in reserv:
            if start < record["start"] and end > record["end"]:
                print(record)

    # List the current reservations for a given customer for a given date range, including the cost of the reservation
    elif inp == "2":
        name = input("Enter your name: ")

        start = get_startdate()
        end = get_enddate()

        for record in reserv:
            if name == record["customer"] and start < record["start"] and end > record["end"]:
                print(record)

    
    # List the current reservations for a given machine for a given date range
    elif inp == "3":
        print("a. multi-phasic radiation scanner")
        print("b. ore scooper")
        print("c. 1.21 gigawatt lightning harvester")
        machine = input("Choose the machine type (enter a, b, or c): ")
        if machine == "a":
            no = input("Choose the scanner no. (enter number 1~4): ")
            machine = machine + no
        elif machine == "b":
            no = input("Choose the scooper no. (enter number 1~4): ")
            machine = machine + no
        elif machine == "c":
            machine = "c1"
        
        start = get_startdate()
        end = get_enddate()

        for record in reserv:
            if machine == record["machine"] and start < record["start"] and end > record["end"]:
                print(record)
        
    else:
        print("Please enter number 1~3.")

def find_transaction(transac):
    """
    Function that finds transactions based on the user criteria

    Input: list of transactions

    Output: transactions in the starting and ending date range
    """
    start = input("Enter the start date (mm/dd/yyyy): ")
    mm, dd, yyyy = start.split("/")
    start = date(int(yyyy), int(mm), int(dd))

    end = input("Enter the end date (mm/dd/yyyy): ")
    mm, dd, yyyy = end.split("/")
    end = date(int(yyyy), int(mm), int(dd))

    for record in transac:
        if start < record["date"] and end > record["date"]:
            print(record)


def get_startdate():
    """
    Get start time for bookings

    Output: start datetime
    """
    start = input("Enter the start date (mm/dd/yyyy): ")
    mm, dd, yyyy = start.split("/")
    start = datetime(int(yyyy), int(mm), int(dd), 0, 1)
    return start
    
def get_enddate():
    """
    Get end time for bookings

    Output: end datetime
    """
    end = input("Enter the end date (mm/dd/yyyy): ")
    mm, dd, yyyy = end.split("/")
    end = datetime(int(yyyy), int(mm), int(dd), 23, 59)
    return end

def booking():
    """
    Function that allows users to book machines

    Parameters:

    - reserv: List storing reservations
    - transac: List storing transactions
    - reservation_id: Unique identifier for each reservation made
    """

    reserv = []
    transac = []
    reservation_id = 0

    while True:
        print("Welcome to Station 13.")
        print("1. Make Reservations")
        print("2. Cancel Reservations")
        print("3. Find Reservations")
        print("4. Find Transactions")
        print("5. Exit")

        inp = input("Make your request (enter number 1~5): ")

        if inp == "1":
            make_reservation(reserv, transac, reservation_id)

        elif inp == "2":
            cancel_reservation(reserv, transac)
            
        elif inp == "3":
            find_reservation(reserv)
        
        elif inp == "4":
            find_transaction(transac)

        elif inp == "5":
            print("bye bye")
            break

def main():
    booking()

if __name__ == "__main__":
    main()