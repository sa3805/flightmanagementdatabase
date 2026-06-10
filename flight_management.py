import sqlite3 

#input validation functions:
def get_int(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        print("Please enter a valid number.")


def get_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_datetime(prompt):
    while True:
        value = input(prompt).strip()
        if len(value) >= 10 and "-" in value and ":" in value:
            return value
        print("Please enter a valid datetime (e.g. 2026-06-10 09:00)")

#database table creation:
def create_database():
    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Destination (
        DestinationID INTEGER PRIMARY KEY,
        AirportName TEXT,
        City TEXT,
        Country TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Plane (
        PlaneID INTEGER PRIMARY KEY,
        Manufacturer TEXT,
        Model TEXT,
        SeatCapacity INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pilot (
        PilotID INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        LicenceNumber TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Flight (
        FlightID INTEGER PRIMARY KEY,
        FlightNumber TEXT,
        Origin TEXT,
        Status TEXT,
        DepartureDateTime TEXT,
        ArrivalDateTime TEXT,
        DestinationID INTEGER,
        PlaneID INTEGER,
        FOREIGN KEY (DestinationID) REFERENCES Destination(DestinationID),
        FOREIGN KEY (PlaneID) REFERENCES Plane(PlaneID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS FlightPilot (
        FlightID INTEGER,
        PilotID INTEGER,
        PRIMARY KEY (FlightID, PilotID),
        FOREIGN KEY (FlightID) REFERENCES Flight(FlightID),
        FOREIGN KEY (PilotID) REFERENCES Pilot(PilotID)
    )
    """)

    conn.commit()
    conn.close()

#inserts sample data for each table 
def populate_database():

    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()

    destinations = [
        (1, "Los Angeles International Airport", "Los Angeles", "USA"),
        (2, "Kansai International Airport", "Osaka", "Japan"),
        (3, "Incheon International Airport", "Seoul", "South Korea"),
        (4, "Auckland Airport", "Auckland", "New Zealand"),
        (5, "Rio de Janeiro–Galeão International Airport", "Rio de Janeiro", "Brazil"),
        (6, "Singapore Changi Airport", "Singapore", "Singapore"),
        (7, "Tan Son Nhat International Airport", "Ho Chi Minh City", "Vietnam"),
        (8, "John F. Kennedy International Airport", "New York", "USA"),
        (9, "Heathrow Airport", "London", "United Kingdom"),
        (10, "Shanghai Pudong International Airport", "Shanghai", "China"),
        (11, "Charles de Gaulle Airport", "Paris", "France"),
        (12, "Amsterdam Airport Schiphol", "Amsterdam", "Netherlands")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO Destination VALUES (?, ?, ?, ?)",
        destinations
    )

    planes = [
        (1, "Boeing", "737-800", 189),
        (2, "Boeing", "787-9", 296),
        (3, "Airbus", "A320neo", 180),
        (4, "Airbus", "A350-900", 325),
        (5, "Boeing", "777-300ER", 396),
        (6, "Airbus", "A330-300", 277),
        (7, "Boeing", "737 MAX 8", 210),
        (8, "Airbus", "A321neo", 220),
        (9, "Boeing", "787-10", 330),
        (10, "Airbus", "A380-800", 525)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO Plane VALUES (?, ?, ?, ?)",
        planes
    )

    pilots = [
        (1, "Mark", "Scout", "LIC001"),
        (2, "Helena", "Eagan", "LIC002"),
        (3, "Dylan", "George", "LIC003"),
        (4, "Irving", "Bailiff", "LIC004"),
        (5, "Harmony", "Cobel", "LIC005"),
        (6, "Seth", "Milchick", "LIC006"),
        (7, "Ricken", "Hale", "LIC007"),
        (8, "Burt", "Goodman", "LIC008"),
        (9, "Natalie", "Kalen", "LIC009"),
        (10, "Doug", "Graner", "LIC010")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO Pilot VALUES (?, ?, ?, ?)",
        pilots
    )

    flights = [
    (1, "BA101", "London", "On Time", "2026-06-10 09:00", "2026-06-10 20:00", 1, 2),
    (2, "BA102", "London", "Delayed", "2026-06-11 10:00", "2026-06-12 08:00", 2, 4),
    (3, "BA103", "Paris", "On Time", "2026-06-12 11:00", "2026-06-13 07:00", 3, 5),
    (4, "BA104", "Amsterdam", "Cancelled", "2026-06-13 08:00", "2026-06-14 06:00", 4, 9),
    (5, "BA105", "London", "On Time", "2026-06-14 12:00", "2026-06-14 23:00", 5, 6),
    (6, "BA106", "Singapore", "On Time", "2026-06-15 13:00", "2026-06-16 07:00", 6, 10),
    (7, "BA107", "Seoul", "Delayed", "2026-06-16 14:00", "2026-06-17 06:00", 7, 4),
    (8, "BA108", "New York", "On Time", "2026-06-17 15:00", "2026-06-17 23:00", 8, 2),
    (9, "BA109", "Shanghai", "Delayed", "2026-06-18 16:00", "2026-06-19 10:00", 10, 5),
    (10, "BA110", "Rio de Janeiro", "On Time", "2026-06-19 17:00", "2026-06-19 19:00", 5, 3),
    (11, "BA111", "Auckland", "On Time", "2026-06-20 18:00", "2026-06-21 08:00", 4, 7),
    (12, "BA112", "Los Angeles", "On Time", "2026-06-21 19:00", "2026-06-22 09:00", 1, 8)
]

    cursor.executemany(
        "INSERT OR IGNORE INTO Flight VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        flights
    )

#associates flightID with a pilotID: 
    flight_pilots = [
        (1, 1), (1, 2),
        (2, 2), (2, 3),
        (3, 3), (3, 4),
        (4, 4), (4, 5),
        (5, 5), (5, 6),
        (6, 6), (6, 7),
        (7, 7), (7, 8),
        (8, 8), (8, 9),
        (9, 9), (9, 10),
        (10, 1), (10, 5),
        (11, 2), (11, 6),
        (12, 3), (12, 7)
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO FlightPilot VALUES (?, ?)",
        flight_pilots
    )

    conn.commit()
    conn.close()

#allows user to add a new flight 
def add_flight():

    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()

    flight_id = get_int("Flight ID: ")
    flight_number = get_non_empty("Flight Number: ")
    origin = get_non_empty("Origin: ")
    status = get_non_empty("Status: ")
    departure = get_datetime("Departure (YYYY-MM-DD HH:MM): ")
    arrival = get_datetime("Arrival (YYYY-MM-DD HH:MM): ")
    destination_id = get_int("Destination ID: ")
    plane_id = get_int("Plane ID: ")

    cursor.execute("""
        INSERT INTO Flight
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        flight_id,
        flight_number,
        origin,
        status,
        departure,
        arrival,
        destination_id,
        plane_id
    ))

    conn.commit()

    print("Flight added successfully")

    conn.close()

#allows user to retrieve flight based on criteria selected
#SQL join queries join flight and destination tables
def view_flights():

    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()

    print("\nView Flights By:")
    print("1. Destination")
    print("2. Status")
    print("3. Departure Date")

    choice = input("Choose an option: ")

    if choice == "1":

        destination = input("Enter destination city: ")

        cursor.execute("""
            SELECT
                f.FlightID,
                f.FlightNumber,
                d.City,
                f.Status,
                f.DepartureDateTime
            FROM Flight f
            JOIN Destination d
                ON f.DestinationID = d.DestinationID
            WHERE d.City = ?
        """, (destination,))

    elif choice == "2":

        status = input("Enter status (On Time, Delayed, Cancelled): ")

        cursor.execute("""
            SELECT
                f.FlightID,
                f.FlightNumber,
                d.City,
                f.Status,
                f.DepartureDateTime
            FROM Flight f
            JOIN Destination d
                ON f.DestinationID = d.DestinationID
            WHERE f.Status = ?
            """, (status,))

    elif choice == "3":

        date = input("Enter date (YYYY-MM-DD): ")

        cursor.execute("""
            SELECT
                f.FlightID,
                f.FlightNumber,
                d.City,
                f.Status,
                f.DepartureDateTime
            FROM Flight f
            JOIN Destination d
                ON f.DestinationID = d.DestinationID
            WHERE f.DepartureDateTime LIKE ?
            """, (date + "%",))

    else:
        print("Invalid option")
        conn.close()
        return

    results = cursor.fetchall()

    if len(results) == 0:
        print("No flights found")

    else:
        print("\nResults:")
        for row in results:
            print(row)

    conn.close()

#allows flight information to be updated or flight to be deleted
def update_flight():

    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()

    flight_id = input("Enter Flight ID to update: ")

    print("\nOptions:")
    print("1. Flight Status")
    print("2. Departure Date/Time")
    print("3. Delete Flight")

    choice = input("Choose an option: ")

    if choice == "1":

        new_status = get_non_empty(
            "Enter new status (On Time, Delayed, Cancelled): "
        )

        cursor.execute("""
            UPDATE Flight
            SET Status = ?
            WHERE FlightID = ?
        """, (new_status, flight_id))

        print("Flight status updated")
 
    elif choice == "2":

        new_departure = get_datetime(
            "Enter new departure date/time (YYYY-MM-DD HH:MM):"
        )

        cursor.execute("""
            UPDATE Flight
            SET DepartureDateTime = ?
            WHERE FlightID = ?
        """, (new_departure, flight_id))

        print("Departure updated")

    elif choice == "3":

        # deletes from junction table 
        cursor.execute("""
            DELETE FROM FlightPilot
            WHERE FlightID = ?
        """, (flight_id,))

        # deletes flight
        cursor.execute("""
            DELETE FROM Flight
            WHERE FlightID = ?
        """, (flight_id,))

        print("Flight deleted successfully")

    else:
        print("Invalid option")
        conn.close()
        return

    conn.commit()

    if cursor.rowcount > 0:
        print("Flight updated successfully")
    else:
        print("No matching flight found")

    conn.close()

#Inserts record into FlightPilot junction table to assign pilot to flight
def assign_pilot():

    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()

    flight_id = get_int("Flight ID: ")
    pilot_id = get_int("Pilot ID: ")

    try:
        cursor.execute("""
            INSERT INTO FlightPilot
            VALUES (?, ?)
        """, (flight_id, pilot_id))

        conn.commit()

        print("Pilot assigned successfully")

    except sqlite3.IntegrityError:
        print("Assignment already exists or invalid ID")

    conn.close()

#displays all flights assigned to selected pilot
#uses multiple JOIN statements to use multiple tables
def view_pilot_schedule():

    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()

    pilot_id = get_int("Pilot ID: ")

    cursor.execute("""
        SELECT
            f.FlightID,
            p.FirstName,
            p.LastName,
            f.FlightNumber,
            d.City,
            f.DepartureDateTime,
            f.Status
        FROM Pilot p
        JOIN FlightPilot fp
            ON p.PilotID = fp.PilotID
        JOIN Flight f
            ON fp.FlightID = f.FlightID
        JOIN Destination d
            ON f.DestinationID = d.DestinationID
        WHERE p.PilotID = ?
    """, (pilot_id,))

    results = cursor.fetchall()

    if len(results) == 0:
        print("No schedule found")

    else:
        print("\nPilot Schedule:")
        for row in results:
            print(
                f"Pilot: {row[1]} {row[2]} | "
                f"Flight ID: {row[0]} | "
                f"Flight Number: {row[3]} | "
                f"Destination: {row[4]} | "
                f"Departure: {row[5]} | "
                f"Status: {row[6]}"
            )

    conn.close()

def view_destinations():

    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Destination
    """)

    results = cursor.fetchall()

    for row in results:
        print(f"ID: {row[0]}")
        print(f"Airport: {row[1]}")
        print(f"City: {row[2]}")
        print(f"Country: {row[3]}")

    conn.close()

def update_destination():

    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()

    destination_id = get_int("Destination ID: ")
    airport = get_non_empty("Airport: ")
    city = get_non_empty("City: ")
    country = get_non_empty("Country: ")

    cursor.execute("""
        UPDATE Destination
        SET AirportName = ?,
            City = ?,
            Country = ?
        WHERE DestinationID = ?
    """, (
        airport,
        city,
        country,
        destination_id
    ))

    conn.commit()

    if cursor.rowcount > 0:
        print("Destination updated")

    else:
        print("Destination not found")

    conn.close()

def view_report():

    conn = sqlite3.connect("flight_management.db")
    cursor = conn.cursor()
#uses count and group queries to calculate totals
    print("\nReports")
    print("1. Flights Per Destination")
    print("2. Flights Per Pilot")

    choice = get_int("Choose report: ")

    if choice == 1:

        cursor.execute("""
            SELECT
                d.City,
                COUNT(f.FlightID)
            FROM Destination d
            LEFT JOIN Flight f
                ON d.DestinationID = f.DestinationID
            GROUP BY d.DestinationID
        """)

        results = cursor.fetchall()

        print("\nFlights Per Destination")

        for row in results:
            print(f"{row[0]} → {row[1]} flights")

    elif choice == 2:

        cursor.execute("""
            SELECT
                p.FirstName,
                p.LastName,
                COUNT(fp.FlightID)
            FROM Pilot p
            LEFT JOIN FlightPilot fp
                ON p.PilotID = fp.PilotID
            GROUP BY p.PilotID
        """)

        results = cursor.fetchall()

        print("\nFlights Per Pilot")

        for row in results:
            print(f"{row[0]} {row[1]} → {row[2]} flights")

    else:
        print("Invalid choice")

    conn.close()

#allows user navigation 
def main_menu():

    while True:

        print("\n===== Flight Management System =====")
        print("1. Add New Flight")
        print("2. View Flights by Criteria")
        print("3. Update Flight Information")
        print("4. Assign Pilot to Flight")
        print("5. View Pilot Schedule")
        print("6. View Destinations")
        print("7. Update Destination")
        print("8. Reports")
        print("9. Exit Program")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_flight()

        elif choice == "2":
            view_flights()

        elif choice == "3":
            update_flight()

        elif choice == "4":
            assign_pilot()

        elif choice == "5":
            view_pilot_schedule()

        elif choice == "6":
            view_destinations()

        elif choice == "7":
            update_destination()

        elif choice == "8":
            view_report()
        
        elif choice == "9":
            print("Goodbye")
            break

        else:
            print("Invalid choice.")

create_database()
# only run once to initialise DB:
populate_database()
main_menu()