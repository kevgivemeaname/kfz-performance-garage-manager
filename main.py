"""
KFZ Performance Garage Manager - V2.4

A terminal-based vehicle management system for tracking cars,
service records, modification records, ownership costs and garage analytics.

Version 2.4 adds a vehicle sorting system on top of the V2.3 search and filter system.
"""

import json
import os
import time
from datetime import datetime


DATA_FILE = "garage_data.json"


class Car:
    """
    Represents one vehicle in the garage.
    Stores vehicle details, service records and modification records.
    """

    def __init__(self, plate, make, model, year):
        self.plate = plate
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
        if len(self.services) == 0:
            print("No service records found.")
            return

        print(f"\nService History for {self.plate}")
        print("-" * 75)
        self.display_info()
        print("-" * 75)

        print(
            f"{'DATE':<12}"
            f"{'DESCRIPTION':<35}"
            f"{'ODOMETER':>12}"
            f"{'COST':>14}"
        )
        print("-" * 75)

        for service in self.services:
            service.display_info()

        print("-" * 75)

    def add_modification(self, modification):
        self.modifications.append(modification)

    def view_modifications(self):
        if len(self.modifications) == 0:
            print("No modification records found.")
            return

        print(f"\nModification History for {self.plate}")
        print("-" * 75)
        self.display_info()
        print("-" * 75)

        print(
            f"{'DATE':<12}"
            f"{'PART':<35}"
            f"{'CATEGORY':<15}"
            f"{'COST':>12}"
        )
        print("-" * 75)

        for modification in self.modifications:
            modification.display_info()

        print("-" * 75)

    def total_service_cost(self):
        total = 0

        for service in self.services:
            total += service.cost

        return total

    def total_modification_cost(self):
        total = 0

        for modification in self.modifications:
            total += modification.cost

        return total

    def total_ownership_cost(self):
        return self.total_service_cost() + self.total_modification_cost()

    def view_cost_summary(self):
        service_total = self.total_service_cost()
        modification_total = self.total_modification_cost()
        overall_total = self.total_ownership_cost()

        print(f"\nCost Summary for {self.plate}")
        print("-" * 45)
        print(f"{'Service Total:':<25} ${service_total:>10.2f}")
        print(f"{'Modification Total:':<25} ${modification_total:>10.2f}")
        print(f"{'Overall Total:':<25} ${overall_total:>10.2f}")
        print("-" * 45)

    def to_dict(self):
        services_data = []

        for service in self.services:
            services_data.append(service.to_dict())

        modifications_data = []

        for modification in self.modifications:
            modifications_data.append(modification.to_dict())

        return {
            "plate": self.plate,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "services": services_data,
            "modifications": modifications_data
        }


class ServiceRecord:
    """
    Represents one service record for a vehicle.
    """

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
            "cost": self.cost
        }


class Modification:
    """
    Represents one modification record for a vehicle.
    """

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
            "cost": self.cost
        }


class GarageManager:
    """
    Controls the main garage system, including menu flow,
    user input, searching, saving and loading data.
    """

    def __init__(self):
        self.cars = []

    def print_header(self, title):
        line = "=" * 45

        print()

        for char in line:
            print(char, end="", flush=True)
            time.sleep(0.003)

        print()
        print(title.upper().center(45))

        for char in line:
            print(char, end="", flush=True)
            time.sleep(0.003)

        print()

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input("\nPress Enter to continue...")

    def get_text_input(self, prompt):
        while True:
            value = input(prompt).strip()

            if value == "":
                print("Input cannot be empty.")
            else:
                return value

    def get_date_input(self, prompt):
        """
        Gets a valid date from the user in DD/MM/YYYY format.

        datetime.strptime() is used to validate the date so invalid values
        such as 99/99/9999 or 31/02/2026 are rejected.
        """

        while True:
            date_input = input(prompt).strip()

            try:
                datetime.strptime(date_input, "%d/%m/%Y")
                return date_input

            except ValueError:
                print("Invalid date format. Use DD/MM/YYYY.")

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
        """
        Loads garage data from a JSON file and rebuilds Car,
        ServiceRecord and Modification objects.
        """

        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            self.cars = []

            for car_data in data:
                car = Car(
                    car_data["plate"],
                    car_data["make"],
                    car_data["model"],
                    car_data["year"]
                )

                for service_data in car_data["services"]:
                    service = ServiceRecord(
                        service_data["date"],
                        service_data["description"],
                        service_data["odometer"],
                        service_data["cost"]
                    )

                    car.add_service(service)

                for modification_data in car_data["modifications"]:
                    modification = Modification(
                        modification_data["date"],
                        modification_data["part_name"],
                        modification_data["category"],
                        modification_data["cost"]
                    )

                    car.add_modification(modification)

                self.cars.append(car)

            print("Garage data loaded successfully.")

        except FileNotFoundError:
            print("No saved garage data found.")

        except json.JSONDecodeError:
            print("Garage data file is corrupted or invalid.")

        except KeyError as error:
            print(f"Garage data is missing required field: {error}")

    def save_data(self):
        """
        Saves all garage data to a JSON file.

        Objects are converted into dictionaries before writing,
        because JSON cannot directly store Python class instances.
        """

        data = []

        for car in self.cars:
            data.append(car.to_dict())

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

        print("Garage data saved successfully.")

    def find_car(self, plate):
        """
        Searches for a car by plate/rego.
        Returns the Car object if found, otherwise returns None.
        """

        for car in self.cars:
            if car.plate.lower() == plate.lower():
                return car

        return None

    def select_car(self):
        plate = self.get_text_input("Enter plate/rego: ").upper()

        car = self.find_car(plate)

        if car is None:
            print("Car not found.")
            return None

        return car

    def add_car(self):
        plate = self.get_text_input("Enter plate/rego: ").upper()

        existing_car = self.find_car(plate)

        if existing_car is not None:
            print("This plate already exists in the garage.")
            return

        make = self.get_text_input("Enter make: ")
        model = self.get_text_input("Enter model: ")
        year = self.get_int_input("Enter year: ")

        new_car = Car(plate, make, model, year)
        self.cars.append(new_car)

        print("Car added successfully.")

    def view_cars(self):
        if len(self.cars) == 0:
            print("No cars in garage.")
            return

        print()
        print("-" * 75)

        print(
            f"{'PLATE':<12}"
            f"{'MAKE':<15}"
            f"{'MODEL':<20}"
            f"{'YEAR':>8}"
        )

        print("-" * 75)

        for car in self.cars:
            print(
                f"{car.plate:<12}"
                f"{car.make:<15}"
                f"{car.model:<20}"
                f"{car.year:>8}"
            )

        print("-" * 75)

    def search_car(self):
        plate = self.get_text_input("Enter plate/rego to search: ").upper()

        car = self.find_car(plate)

        if car is None:
            print("Car not found.")
            return

        car.display_info()

    def delete_car(self):
        car = self.select_car()

        if car is None:
            return

        confirm = self.get_text_input(
            f"Type DELETE to confirm removal of {car.plate}: "
        )

        if confirm == "DELETE":
            self.cars.remove(car)
            print("Car deleted successfully.")
        else:
            print("Delete cancelled.")

    def add_service_record(self):
        car = self.select_car()

        if car is None:
            return

        date = self.get_date_input("Enter service date (DD/MM/YYYY): ")
        description = self.get_text_input("Enter service description: ")
        odometer = self.get_int_input("Enter odometer: ")
        cost = self.get_float_input("Enter service cost: ")

        service = ServiceRecord(date, description, odometer, cost)
        car.add_service(service)

        print("Service record added successfully.")

    def view_service_records(self):
        car = self.select_car()

        if car is None:
            return

        car.view_services()

    def edit_service_record(self):
        car = self.select_car()

        if car is None:
            return

        if len(car.services) == 0:
            print("No service records found.")
            return

        print("\nService Records")
        print("-" * 60)

        for index, service in enumerate(car.services, start=1):
            print(
                f"{index}. {service.date} - {service.description} "
                f"({service.odometer} km, ${service.cost:.2f})"
            )

        print("-" * 60)

        record_number = self.get_int_input("Select service record number: ")

        if record_number < 1 or record_number > len(car.services):
            print("Invalid selection.")
            return

        service = car.services[record_number - 1]

        print("\nCurrent Record:")
        service.display_info()

        print("\nEnter new service details")
        service.date = self.get_date_input("New date (DD/MM/YYYY): ")
        service.description = self.get_text_input("New description: ")
        service.odometer = self.get_int_input("New odometer: ")
        service.cost = self.get_float_input("New cost: ")

        print("Service record updated successfully.")

    def delete_service_record(self):
        car = self.select_car()

        if car is None:
            return

        if len(car.services) == 0:
            print("No service records found.")
            return

        print("\nService Records")
        print("-" * 60)

        for index, service in enumerate(car.services, start=1):
            print(
                f"{index}. {service.date} - {service.description} "
                f"({service.odometer} km, ${service.cost:.2f})"
            )

        print("-" * 60)

        record_number = self.get_int_input("Select service record number to delete: ")

        if record_number < 1 or record_number > len(car.services):
            print("Invalid selection.")
            return

        service = car.services[record_number - 1]

        confirm = self.get_text_input(
            f"Type DELETE to confirm deletion of '{service.description}': "
        )

        if confirm == "DELETE":
            car.services.pop(record_number - 1)
            print("Service record deleted successfully.")
        else:
            print("Delete cancelled.")

    def add_modification_record(self):
        car = self.select_car()

        if car is None:
            return

        date = self.get_date_input("Enter modification date (DD/MM/YYYY): ")
        part_name = self.get_text_input("Enter part name: ")
        category = self.get_text_input("Enter category: ")
        cost = self.get_float_input("Enter modification cost: ")

        modification = Modification(date, part_name, category, cost)
        car.add_modification(modification)

        print("Modification record added successfully.")

    def view_modification_records(self):
        car = self.select_car()

        if car is None:
            return

        car.view_modifications()

    def edit_modification_record(self):
        car = self.select_car()

        if car is None:
            return

        if len(car.modifications) == 0:
            print("No modification records found.")
            return

        print("\nModification Records")
        print("-" * 60)

        for index, modification in enumerate(car.modifications, start=1):
            print(
                f"{index}. {modification.date} - {modification.part_name} "
                f"({modification.category}, ${modification.cost:.2f})"
            )

        print("-" * 60)

        record_number = self.get_int_input("Select modification record number: ")

        if record_number < 1 or record_number > len(car.modifications):
            print("Invalid selection.")
            return

        modification = car.modifications[record_number - 1]

        print("\nCurrent Record:")
        modification.display_info()

        print("\nEnter new modification details")
        modification.date = self.get_date_input("New date (DD/MM/YYYY): ")
        modification.part_name = self.get_text_input("New part name: ")
        modification.category = self.get_text_input("New category: ")
        modification.cost = self.get_float_input("New cost: ")

        print("Modification record updated successfully.")

    def delete_modification_record(self):
        car = self.select_car()

        if car is None:
            return

        if len(car.modifications) == 0:
            print("No modification records found.")
            return

        print("\nModification Records")
        print("-" * 60)

        for index, modification in enumerate(car.modifications, start=1):
            print(
                f"{index}. {modification.date} - {modification.part_name} "
                f"({modification.category}, ${modification.cost:.2f})"
            )

        print("-" * 60)

        record_number = self.get_int_input(
            "Select modification record number to delete: "
        )

        if record_number < 1 or record_number > len(car.modifications):
            print("Invalid selection.")
            return

        modification = car.modifications[record_number - 1]

        confirm = self.get_text_input(
            f"Type DELETE to confirm deletion of '{modification.part_name}': "
        )

        if confirm == "DELETE":
            car.modifications.pop(record_number - 1)
            print("Modification record deleted successfully.")
        else:
            print("Delete cancelled.")

    def view_cost_summary(self):
        car = self.select_car()

        if car is None:
            return

        car.view_cost_summary()

    def view_garage_summary(self):
        self.print_header("Garage Summary")

        if len(self.cars) == 0:
            print("No cars in garage.")
            return

        garage_total = 0

        for car in self.cars:
            service_total = car.total_service_cost()
            modification_total = car.total_modification_cost()
            overall_total = car.total_ownership_cost()

            garage_total += overall_total

            print(f"\n{car.year} {car.make} {car.model} ({car.plate})")
            print("-" * 45)
            print(f"{'Service Total:':<25} ${service_total:>10.2f}")
            print(f"{'Modification Total:':<25} ${modification_total:>10.2f}")
            print(f"{'Vehicle Total:':<25} ${overall_total:>10.2f}")

        print("\n" + "=" * 45)
        print(f"{'Garage Total:':<25} ${garage_total:>10.2f}")

    def view_garage_statistics(self):
        """
        Displays garage-level analytics.

        This method turns stored vehicle, service and modification data into
        meaningful business-style summaries, such as total garage cost,
        average vehicle cost, highest individual expenses and most modified car.
        """

        self.print_header("Garage Statistics")

        if len(self.cars) == 0:
            print("No cars in garage.")
            return

        # Aggregate garage-wide totals across all vehicles.
        garage_total = 0
        total_service_cost = 0
        total_modification_cost = 0
        total_service_records = 0
        total_modification_records = 0

        # Track the highest individual service record.
        highest_service = None
        highest_service_car = None

        # Track the highest individual modification record.
        highest_modification = None
        highest_modification_car = None

        for car in self.cars:
            garage_total += car.total_ownership_cost()
            total_service_cost += car.total_service_cost()
            total_modification_cost += car.total_modification_cost()
            total_service_records += len(car.services)
            total_modification_records += len(car.modifications)

            # Find the most expensive single service item.
            for service in car.services:
                if highest_service is None or service.cost > highest_service.cost:
                    highest_service = service
                    highest_service_car = car

            # Find the most expensive single modification item.
            for modification in car.modifications:
                if (
                    highest_modification is None
                    or modification.cost > highest_modification.cost
                ):
                    highest_modification = modification
                    highest_modification_car = car

        # Find the vehicle with the highest combined service and modification cost.
        most_expensive_vehicle = max(
            self.cars,
            key=lambda car: car.total_ownership_cost()
        )

        # Find the vehicle with the largest number of modification records.
        most_modified_vehicle = max(
            self.cars,
            key=lambda car: len(car.modifications)
        )

        average_vehicle_cost = garage_total / len(self.cars)

        print(f"{'Vehicles Stored:':<30} {len(self.cars):>12}")
        print(f"{'Service Records:':<30} {total_service_records:>12}")
        print(f"{'Modification Records:':<30} {total_modification_records:>12}")
        print("-" * 45)

        print(f"{'Total Service Cost:':<30} ${total_service_cost:>11.2f}")
        print(f"{'Total Modification Cost:':<30} ${total_modification_cost:>11.2f}")
        print(f"{'Garage Total Cost:':<30} ${garage_total:>11.2f}")
        print(f"{'Average Vehicle Cost:':<30} ${average_vehicle_cost:>11.2f}")
        print("-" * 45)

        print(
            f"{'Most Expensive Vehicle:':<30} "
            f"{most_expensive_vehicle.plate}"
        )
        print(
            f"{'Vehicle Total Cost:':<30} "
            f"${most_expensive_vehicle.total_ownership_cost():>11.2f}"
        )

        print(
            f"{'Most Modified Vehicle:':<30} "
            f"{most_modified_vehicle.plate}"
        )
        print(
            f"{'Number of Modifications:':<30} "
            f"{len(most_modified_vehicle.modifications):>12}"
        )
        print("-" * 45)

        if highest_service is not None:
            print(
                f"{'Highest Service Cost:':<30} "
                f"${highest_service.cost:>11.2f}"
            )
            print(
                f"{'Service Vehicle:':<30} "
                f"{highest_service_car.plate}"
            )
            print(
                f"{'Service Description:':<30} "
                f"{highest_service.description}"
            )
        else:
            print("No service cost data available.")

        print("-" * 45)

        if highest_modification is not None:
            print(
                f"{'Highest Modification Cost:':<30} "
                f"${highest_modification.cost:>11.2f}"
            )
            print(
                f"{'Modification Vehicle:':<30} "
                f"{highest_modification_car.plate}"
            )
            print(
                f"{'Modification Part:':<30} "
                f"{highest_modification.part_name}"
            )
        else:
            print("No modification cost data available.")

    def display_vehicle_search_results(self, results):
        """
        Displays a list of vehicles returned by a search or filter operation.
        """

        if len(results) == 0:
            print("No matching vehicles found.")
            return

        print()
        print("-" * 75)
        print(
            f"{'PLATE':<12}"
            f"{'MAKE':<15}"
            f"{'MODEL':<20}"
            f"{'YEAR':>8}"
            f"{'TOTAL COST':>18}"
        )
        print("-" * 75)

        for car in results:
            print(
                f"{car.plate:<12}"
                f"{car.make:<15}"
                f"{car.model:<20}"
                f"{car.year:>8}"
                f"${car.total_ownership_cost():>17.2f}"
            )

        print("-" * 75)

    def search_by_make(self):
        """
        Finds all vehicles matching a selected manufacturer.
        """

        make = self.get_text_input("Enter make to search: ")

        results = []

        for car in self.cars:
            if car.make.lower() == make.lower():
                results.append(car)

        self.display_vehicle_search_results(results)

    def search_by_year(self):
        """
        Finds all vehicles from a selected year.
        """

        year = self.get_int_input("Enter year to search: ")

        results = []

        for car in self.cars:
            if car.year == year:
                results.append(car)

        self.display_vehicle_search_results(results)

    def search_by_plate(self):
        """
        Finds a vehicle by plate/rego and displays its full basic information.
        """

        plate = self.get_text_input("Enter plate/rego to search: ").upper()
        car = self.find_car(plate)

        if car is None:
            print("No matching vehicle found.")
            return

        print()
        print("-" * 45)
        car.display_info()
        print(f"{'Service Records:':<25} {len(car.services):>10}")
        print(f"{'Modification Records:':<25} {len(car.modifications):>10}")
        print(f"{'Total Ownership Cost:':<25} ${car.total_ownership_cost():>10.2f}")
        print("-" * 45)

    def search_by_modification_category(self):
        """
        Finds vehicles that contain at least one modification
        matching the selected category.

        This demonstrates nested traversal because the system searches
        through each vehicle and then through each vehicle's modifications.
        """

        category = self.get_text_input("Enter modification category: ")

        results = []

        for car in self.cars:
            for modification in car.modifications:
                if modification.category.lower() == category.lower():
                    if car not in results:
                        results.append(car)

        self.display_vehicle_search_results(results)

    def search_and_filter_menu(self):
        """
        Displays a submenu for search and filter features.
        """

        if len(self.cars) == 0:
            print("No cars in garage.")
            return

        while True:
            self.clear_screen()
            self.print_header("Search & Filter Vehicles")

            print("1. Search by Make")
            print("2. Search by Year")
            print("3. Search by Plate/Rego")
            print("4. Search by Modification Category")
            print("0. Back")
            print("-" * 45)

            choice = input("Select option: ").strip()

            if choice == "1":
                self.search_by_make()
                self.pause()

            elif choice == "2":
                self.search_by_year()
                self.pause()

            elif choice == "3":
                self.search_by_plate()
                self.pause()

            elif choice == "4":
                self.search_by_modification_category()
                self.pause()

            elif choice == "0":
                break

            else:
                print("Invalid option.")
                self.pause()

    def sort_by_highest_ownership_cost(self):
        """
        Sorts vehicles from highest to lowest total ownership cost.
        """

        sorted_cars = sorted(
            self.cars,
            key=lambda car: car.total_ownership_cost(),
            reverse=True
        )

        self.display_vehicle_search_results(sorted_cars)

    def sort_by_most_modified(self):
        """
        Sorts vehicles from most modified to least modified.
        """

        sorted_cars = sorted(
            self.cars,
            key=lambda car: len(car.modifications),
            reverse=True
        )

        self.display_vehicle_search_results(sorted_cars)

    def sort_by_year(self):
        """
        Sorts vehicles from newest to oldest.
        """

        sorted_cars = sorted(
            self.cars,
            key=lambda car: car.year,
            reverse=True
        )

        self.display_vehicle_search_results(sorted_cars)

    def sort_by_plate(self):
        """
        Sorts vehicles alphabetically by plate/rego.
        """

        sorted_cars = sorted(
            self.cars,
            key=lambda car: car.plate
        )

        self.display_vehicle_search_results(sorted_cars)

    def sort_vehicles_menu(self):
        """
        Displays a submenu for sorting vehicles by different ranking methods.
        """

        if len(self.cars) == 0:
            print("No cars in garage.")
            return

        while True:
            self.clear_screen()
            self.print_header("Sort Vehicles")

            print("1. Sort by Highest Ownership Cost")
            print("2. Sort by Most Modified")
            print("3. Sort by Year")
            print("4. Sort by Plate/Rego")
            print("0. Back")
            print("-" * 45)

            choice = input("Select option: ").strip()

            if choice == "1":
                self.sort_by_highest_ownership_cost()
                self.pause()

            elif choice == "2":
                self.sort_by_most_modified()
                self.pause()

            elif choice == "3":
                self.sort_by_year()
                self.pause()

            elif choice == "4":
                self.sort_by_plate()
                self.pause()

            elif choice == "0":
                break

            else:
                print("Invalid option.")
                self.pause()

    def show_menu(self):
        self.print_header("KFZ Performance Garage Manager")

        print(" 1. Add Car")
        print(" 2. View Cars")
        print(" 3. Search Car")
        print("-" * 45)
        print(" 4. Add Service Record")
        print(" 5. View Service Records")
        print(" 6. Edit Service Record")
        print(" 7. Delete Service Record")
        print("-" * 45)
        print(" 8. Add Modification Record")
        print(" 9. View Modification Records")
        print("10. Edit Modification Record")
        print("11. Delete Modification Record")
        print("-" * 45)
        print("12. View Cost Summary Per Car")
        print("13. View Overall Garage Summary")
        print("14. View Garage Statistics")
        print("15. Search & Filter Vehicles")
        print("16. Sort Vehicles")
        print("-" * 45)
        print("17. Delete Car")
        print("18. Save Data")
        print("19. Load Data")
        print("-" * 45)
        print(" 0. Exit")

    def run(self):
        """
        Runs the main menu loop.

        The dictionary below maps menu choices to methods,
        keeping the main loop cleaner than a long if/elif chain.
        """

        menu_actions = {
            "1": self.add_car,
            "2": self.view_cars,
            "3": self.search_car,
            "4": self.add_service_record,
            "5": self.view_service_records,
            "6": self.edit_service_record,
            "7": self.delete_service_record,
            "8": self.add_modification_record,
            "9": self.view_modification_records,
            "10": self.edit_modification_record,
            "11": self.delete_modification_record,
            "12": self.view_cost_summary,
            "13": self.view_garage_summary,
            "14": self.view_garage_statistics,
            "15": self.search_and_filter_menu,
            "16": self.sort_vehicles_menu,
            "17": self.delete_car,
            "18": self.save_data,
            "19": self.load_data
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
    """
    Displays the animated KFZ startup logo.
    Raw strings are used to preserve ASCII-art formatting.
    """

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

    manager.load_data()
    time.sleep(1)

    print("System ready.")
    time.sleep(0.5)

    print("\nWelcome back, Champion.")

    manager.pause()
    manager.run()


if __name__ == "__main__":
    main()
