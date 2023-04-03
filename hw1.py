from datetime import date, datetime

def get_startdate():
    """
    Get start time for bookings
    """
    start = input("Enter the start date (mm/dd/yyyy): ")
    mm, dd, yyyy = start.split("/")
    start = datetime(int(yyyy), int(mm), int(dd), 0, 1)
    return start
    
def get_enddate():
    """
    Get end time for bookings
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
    - count: count..???
    """

    reserv = []
    transac = []
    count = 0


    while True:
        print("Welcome to Station 13.")
        print("1. Make Reservations")
        print("2. Cancel Reservations")
        print("3. Find Reservations")
        print("4. Find Transactions")
        print("5. Exit")


        inp = input("Make your request (enter number 1~5): ")

        # when the user chooses to make a reservation
        if inp == "1":

            # set the machine type and no, represented by "a1" or "b2" etc.
            print("a. multi-phasic radiation scanner")
            print("b. ore scooper")
            print("c. 1.21 gigawatt lightning harvester")
            machine = input("Choose the machine type you want (enter a, b, or c): ")
            if machine == "a":
                no = input("Choose the scanner no. you want (enter number 1~4): ")
                machine = machine + no
            elif machine == "b":
                no = input("Choose the scooper no. you want (enter number 1~4): ")
                machine = machine + no
            elif machine == "c":
                machine = "c1"


            print("Choose the date of your reservation")
            print("Weekday: 09:00 - 18:00, Saturday: 10:00 - 16:00, Sunday: closed")
            r_date = input("Enter the date (mm/dd/yyyy): ")
            # get the month, day, year using split method
            mm, dd, yyyy = r_date.split("/")
            mm, dd, yyyy = int(mm), int(dd), int(yyyy)

            # create the datetime object for the start and end time
            start = input("Enter the start time of your reservation (e.g. 09:30): ")
            hr, min = start.split(":")
            start = datetime(yyyy, mm, dd, int(hr), int(min))

            end = input("Enter the end time of your reservation (e.g. 13:00): ")
            hr, min = end.split(":")
            end = datetime(yyyy, mm, dd, int(hr), int(min))

            # check availability here
            avail = True
            scan = 0
            for record in reserv:
                if record["machine"] == machine:
                    if start <= record["start"] and end <= record["start"] or start >= record["end"] and end >= record["end"]:
                        pass
                    else:
                        avail = False
                        print("The machine is occupied that time.")
                        break
                
                # special requirements, when machine is a scanner
                if machine[0] == "a" and record["machine"][0] == "a":
                    if start <= record["start"] and end <= record["start"] or start >= record["end"] and end >= record["end"]:
                        pass
                    else:
                        scan += 1
                
                if machine[0] == "a" and record["machine"][0] == "c":
                    if start <= record["start"] and end <= record["start"] or start >= record["end"] and end >= record["end"]:
                        pass
                    else:
                        avail = False
                        print("Sorry. A 1.21 gigawatt lightning harvester occupies the power at that time.")
                        break
            
            if scan >= 3:
                avail = False
                print("Sorry. There're already 3 scanners running at that time.")




            if avail:

                # when the appointed machine is available, handle the payment
                name = input("Enter you name: ")
        
                # calculate the hour range and fee
                hours = (end - start).total_seconds()/3600

                if machine[0] == "a":
                    total = 990 * hours
                elif machine[0] == "b":
                    total = 1000 * hours
                elif machine[0] == "c":
                    total = 88000

                # check if the discount is available
                today = str(date.today())
                c_yyyy, c_mm, c_dd = today.split("-")
                date1 = date(int(c_yyyy), int(c_mm), int(c_dd))
                date2 = date(yyyy, mm, dd)
                day = (date2-date1).days
                if day >= 14:
                    total = total * 0.75
                
                # make the reservation
                count += 1
                record = {"id": count, "machine": machine, "start": start, "end": end, "customer": name, "fee": total}
                reserv.append(record)
                print(f"The reservation is made! Your reservation id is {count}. Your down payment cost is ${total*0.5}. Your total cost is ${total}.")

                # add into the transaction record
                record2 = {"machine": machine, "date": date1, "customer": name, "fee": total, "type": "make reservation"}
                transac.append(record2)
                


                


        # when the user chooses to cancel a reservation 
        elif inp == "2":
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

                    if day >= 7:
                        refund = fee * 0.5 * 0.75
                    elif day >= 2:
                        refund = fee * 0.5 * 0.5
                    else:
                        refund = 0
                    
                    # add to the transaction
                    c_date = date(int(c_yyyy), int(c_mm), int(c_dd))
                    record = {"machine": reserv[i]["machine"], "date": c_date, "customer": reserv[i]["customer"], "fee": refund, "type": "cancel reservation"}
                    transac.append(record)
                    

                    
                    del reserv[i]
                    print(f"You reservation {id} has been canceled. The refund is ${refund}.")
                    break



        

        # when the user chooses to find a reservation
        elif inp == "3":
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
        
        elif inp == "4":
            # for record in transac:
            #     print(record)
            # this is something we can update in terms of code being used over and over again
            start = input("Enter the start date (mm/dd/yyyy): ")
            mm, dd, yyyy = start.split("/")
            start = date(int(yyyy), int(mm), int(dd))

            end = input("Enter the end date (mm/dd/yyyy): ")
            mm, dd, yyyy = end.split("/")
            end = date(int(yyyy), int(mm), int(dd))

            for record in transac:
                if start < record["date"] and end > record["date"]:
                    print(record)


        elif inp == "5":
            print("bye bye")
            break

def main():
    booking()

if __name__ == "__main__":
    main()