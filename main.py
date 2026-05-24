import json
import os
import time

DATA_FILE = "garage_data.json"
HEADER_WIDTH = 45
TABLE_WIDTH = 75


class Car:
    """
    Represents one vehicle in the garage.
    Stores vehicle details, service records and modification records.
    """

    def __init__(self, plate, make, model, year):
        self.plate = plate.upper()
        self.make = make
        self.model = model
        self.year = year
        self.services = []
        self.modifications = []

    def display_info(self):
        print(f"{self.year} {self.make} {self.model} ({self.plate})")

    def add_service(self, service):
        self.services.append(service)

    def view_services(self):
        if not self.services:
            print("No service records found.")
            return

        print(f"\nService History for {self.plate}")
        print("-" * TABLE_WIDTH)
        self.display_info()
        print("-" * TABLE_WIDTH)
        print(f"{'DATE':<12}{'DESCRIPTION':<35}{'ODOMETER':>12}{'COST':>14}")
        print("-" * TABLE_WIDTH)

        for service in self.services:
            service.display_info()

        print("-" * TABLE_WIDTH)

    def add_modification(self, modification):
        self.modifications.append(modification)

    def view_modifications(self):
        if not self.modifications:
            print("No modification records found.")
            return

        print(f"\nModification History for {self.plate}")
        print("-" * TABLE_WIDTH)
        self.display_info()
        print("-" * TABLE_WIDTH)
        print(f"{'DATE':<12}{'PART':<35}{'CATEGORY':<15}{'COST':>12}")
        print("-" * TABLE_WIDTH)

        for modification in self.modifications:
            modification.display_info()

        print("-" * TABLE_WIDTH)

    def total_service_cost(self):
        return sum(service.cost for service in self.services)

    def total_modification_cost(self):
        return sum(modification.cost for modification in self.modifications)

    def view_cost_summary(self):
        service_total = self.total_service_cost()
        modification_total = self.total_modification_cost()
        overall_total = service_total + modification_total

        print(f"\nCost Summary for {self.plate}")
        print("-" * HEADER_WIDTH)
        print(f"{'Service Total:':<25} ${service_total:>10.2f}")
        print(f"{'Modification Total:':<25} ${modification_total:>10.2f}")
        print(f"{'Overall Total:':<25} ${overall_total:>10.2f}")
        print("-" * HEADER_WIDTH)

    def to_dict(self):
        return {
            "plate": self.plate,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "services": [service.to_dict() for service in self.services],
            "modifications": [modification.to_dict() for modification in self.modifications],
        }


class ServiceRecord:
    """Represents one service record for a car."""

    def __init__(self, date, description, odometer, cost):
        self.date = date
        self.description = description
        self.odometer = odometer
        self.cost = cost

    def display_info(self):
        print(
            f"{self.date:<12}"
            f"{self.description:<35}"
            f"{self.odometer:>10} km    "
            f"${self.cost:10.2f}"
        )

    def to_dict(self):
        return {
            "date": self.date,
            "description": self.description,
            "odometer": self.odometer,
            "cost": self.cost,
        }


class Modification:
    """Represents one modification record for a car."""

    def __init__(self, date, part_name, category, cost):
        self.date = date
        self.part_name = part_name
        self.category = category
        self.cost = cost

    def display_info(self):
        print(
            f"{self.date:<12}"
            f"{self.part_name:<35}"
            f"{self.category:<15}"
            f"${self.cost:>12.2f}"
        )

    def to_dict(self):
        return {
            "date": self.date,
            "part_name": self.part_name,
            "category": self.category,
            "cost": self.cost,
        }


class GarageManager:
    """
    Controls the main garage system, including menu flow,
    user input, searching, saving and loading data.
    """

    def __init__(self):
        self.cars = []

    def print_header(self, title):
        line = "=" * HEADER_WIDTH
        print(f"\n{line}")
        print(title.upper().center(HEADER_WIDTH))
        print(line)

    def pause(self):
        input("\nPress Enter to continue...")

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def get_text_input(self, prompt, uppercase=False):
        while True:
            value = input(prompt).strip()

            if value:
                return value.upper() if uppercase else value

            print("Input cannot be empty.")

    def get_float_input(self, prompt):
        while True:
            try:
                value = float(input(prompt))

                if value < 0:
                    raise ValueError("Value cannot be negative.")

                return value

            except ValueError as error:
                print(f"Invalid input: {error}")

    def get_int_input(self, prompt):
        while True:
            try:
                value = int(input(prompt))

                if value < 0:
                    raise ValueError("Value cannot be negative.")

                return value

            except ValueError as error:
                print(f"Invalid input: {error}")

    def load_data(self):
        """Load garage data from a JSON file and rebuild program objects."""
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            self.cars = []

            for car_data in data:
                car = Car(
                    car_data["plate"],
                    car_data["make"],
                    car_data["model"],
                    car_data["year"],
                )

                for service_data in car_data.get("services", []):
                    car.add_service(
                        ServiceRecord(
                            service_data["date"],
                            service_data["description"],
                            service_data["odometer"],
                            service_data["cost"],
                        )
                    )

                for modification_data in car_data.get("modifications", []):
                    car.add_modification(
                        Modification(
                            modification_data["date"],
                            modification_data["part_name"],
                            modification_data["category"],
                            modification_data["cost"],
                        )
                    )

                self.cars.append(car)

            print("Garage data loaded successfully.")

        except FileNotFoundError:
            print("No saved garage data found.")
        except json.JSONDecodeError:
            print("Garage data file is damaged or not valid JSON.")

    def save_data(self):
        """Save all garage data to a JSON file."""
        data = [car.to_dict() for car in self.cars]

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

        print("Garage data saved successfully.")

    def find_car(self, plate):
        for car in self.cars:
            if car.plate.lower() == plate.lower():
                return car
        return None

    def select_car(self):
        plate = self.get_text_input("Enter plate/rego: ", uppercase=True)
        car = self.find_car(plate)

        if car is None:
            print("Car not found.")
            return None

        return car

    def add_car(self):
        plate = self.get_text_input("Enter plate/rego: ", uppercase=True)

        if self.find_car(plate) is not None:
            print("This plate already exists in the garage.")
            return

        make = self.get_text_input("Enter make: ")
        model = self.get_text_input("Enter model: ")
        year = self.get_int_input("Enter year: ")

        self.cars.append(Car(plate, make, model, year))
        print("Car added successfully.")

    def view_cars(self):
        if not self.cars:
            print("No cars in garage.")
            return

        print("\n" + "-" * TABLE_WIDTH)
        print(f"{'PLATE':<12}{'MAKE':<15}{'MODEL':<20}{'YEAR':>8}")
        print("-" * TABLE_WIDTH)

        for car in self.cars:
            print(f"{car.plate:<12}{car.make:<15}{car.model:<20}{car.year:>8}")

        print("-" * TABLE_WIDTH)

    def search_car(self):
        car = self.select_car()
        if car is not None:
            car.display_info()

    def delete_car(self):
        car = self.select_car()

        if car is None:
            return

        self.cars.remove(car)
        print("Car deleted successfully.")

    def add_service_record(self):
        car = self.select_car()

        if car is None:
            return

        date = self.get_text_input("Enter service date (DD/MM/YYYY): ")
        description = self.get_text_input("Enter service description: ")
        odometer = self.get_int_input("Enter odometer: ")
        cost = self.get_float_input("Enter service cost: ")

        car.add_service(ServiceRecord(date, description, odometer, cost))
        print("Service record added successfully.")

    def view_service_records(self):
        car = self.select_car()
        if car is not None:
            car.view_services()

    def add_modification_record(self):
        car = self.select_car()

        if car is None:
            return

        date = self.get_text_input("Enter modification date (DD/MM/YYYY): ")
        part_name = self.get_text_input("Enter part name: ")
        category = self.get_text_input("Enter category: ")
        cost = self.get_float_input("Enter modification cost: ")

        car.add_modification(Modification(date, part_name, category, cost))
        print("Modification record added successfully.")

    def view_modification_records(self):
        car = self.select_car()
        if car is not None:
            car.view_modifications()

    def view_cost_summary(self):
        car = self.select_car()
        if car is not None:
            car.view_cost_summary()

    def view_garage_summary(self):
        self.print_header("Garage Summary")

        if not self.cars:
            print("No cars in garage.")
            return

        garage_total = 0

        for car in self.cars:
            service_total = car.total_service_cost()
            modification_total = car.total_modification_cost()
            vehicle_total = service_total + modification_total
            garage_total += vehicle_total

            print(f"\n{car.year} {car.make} {car.model} ({car.plate})")
            print("-" * HEADER_WIDTH)
            print(f"{'Service Total:':<25} ${service_total:>10.2f}")
            print(f"{'Modification Total:':<25} ${modification_total:>10.2f}")
            print(f"{'Vehicle Total:':<25} ${vehicle_total:>10.2f}")

        print("\n" + "=" * HEADER_WIDTH)
        print(f"{'Garage Total:':<25} ${garage_total:>10.2f}")

    def show_menu(self):
        self.print_header("KFZ Performance Garage Manager")
        print(" 1. Add Car")
        print(" 2. View Cars")
        print(" 3. Search Car")
        print(" 4. Add Service Record")
        print(" 5. View Service Records")
        print(" 6. Add Modification Record")
        print(" 7. View Modification Records")
        print("-" * HEADER_WIDTH)
        print(" 8. View Cost Summary Per Car")
        print(" 9. View Overall Garage Summary")
        print("-" * HEADER_WIDTH)
        print("10. Delete Car")
        print("11. Save Data")
        print("12. Load Data")
        print("-" * HEADER_WIDTH)
        print(" 0. Exit")

    def run(self):
        self.load_data()
        time.sleep(0.5)
        print("System ready.")
        print("\nWelcome back, Champion.")
        self.pause()

        menu_actions = {
            "1": self.add_car,
            "2": self.view_cars,
            "3": self.search_car,
            "4": self.add_service_record,
            "5": self.view_service_records,
            "6": self.add_modification_record,
            "7": self.view_modification_records,
            "8": self.view_cost_summary,
            "9": self.view_garage_summary,
            "10": self.delete_car,
            "11": self.save_data,
            "12": self.load_data,
        }

        while True:
            self.clear_screen()
            self.show_menu()
            choice = input("Select option: ").strip()

            if choice == "0":
                print("\nSynchronising garage records...")
                time.sleep(0.5)
                self.save_data()
                time.sleep(0.5)
                print("Shutting down KFZ Performance Garage Manager...")
                time.sleep(0.5)
                print("Goodbye Champion!")
                break

            action = menu_actions.get(choice)

            if action is None:
                print("Invalid option.")
            else:
                action()

            self.pause()


def show_logo():
    """Display the animated KFZ startup logo."""
    logo = [
        r"                                ",
        r"        ██╗  ██╗███████╗███████╗",
        r"        ██║ ██╔╝██╔════╝╚══███╔╝",
        r"        █████╔╝ █████╗    ███╔╝",
        r"        ██╔═██╗ ██╔══╝   ███╔╝",
        r"        ██║  ██╗██║     ███████╗",
        r"        ╚═╝  ╚═╝╚═╝     ╚══════╝",
        "",
        r"═══════ PERFORMANCE GARAGE MANAGER ═══════",
    ]

    for line in logo:
        for char in line:
            print(char, end="", flush=True)
            time.sleep(0.003)
        print()


def startup_sequence():
    show_logo()
    print("Starting KFZ Performance Garage Manager...")
    time.sleep(0.5)
    print("Initialising vehicle management modules...")
    time.sleep(1)
    print("Synchronising garage records...")

    for i in range(101):
        print(f"\rLoading: {i}%", end="", flush=True)
        time.sleep(0.01)

    print("\n")
    time.sleep(0.2)


def main():
    startup_sequence()
    manager = GarageManager()
    manager.run()


if __name__ == "__main__":
    main()
