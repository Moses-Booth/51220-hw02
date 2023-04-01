# MPCS, Inc. -- Job Applicant Coding Assessment

## Run the program
- Run `python3 hw1.py` on the terminal

## 1. Make Reservations
- Enter `1` to make a reservation. Also please make sure to enter the correct number for the following requests.
- Choose the machine type & machine no. Each type of machine has their machine no. according to the numbers of that machine. For example, machine scanner no.1 are represented as "a1".
- Enter the date and time range of your reservation. Please make sure to strictly follow the format, such as `04/02/2023`, `09:30`, `13:00`. Please using the 24-hour system, and ensure the correct order of the time.
- Enter the name. This will become the customer identification.
- After you successfully make the reservation, the reservation id and cost will be provided.

## 2. Cancel Reservations
- Enter `1` to cancel a reservation.
- You'll need to give the reservation id you want to cancel.
- After you successfully cancel the reservation, the refund will be provided.

## 3. Find Reservations
- Enter `3` to find current reservations.
- Choose the filter you want. Based on the condition, the customer name or machine type & id are needed.
- Enter the date range, the system will find the reservation that happens in this range.

## 4. Find Transactions
- Enter `4` to find all transactions.
- Enter the date range, the system will find the transactions that was made in this range (not the reservation date).

## 5. Exit
- Exit the system and all the data will not be preserved.

## Something Simplified
- The cool down time of the machine is not handled this time.
- As long as you exit the system, the data is not preserved.
- Blocks related stuff is not handled.

## Special Requirements
- Special constraints: handled when checking the availability of the reservation.
- Special user functionality: implemented as the request `4`.
- Other special rules: since the block stuff is not implemented, these may be handled next times.

## bad design
- no self-built function
- no class & abstraction
- loads of nested if-statements
- unclear variable names
- duplicated code
- unnecessary comments
