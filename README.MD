# KFZ Performance Garage Manager

Current Version: V2.4

A terminal-based vehicle management system built in Python for automotive enthusiasts, performance car owners, and garage-style record keeping.

The system allows users to manage multiple vehicles, record service history, track aftermarket modifications, calculate ownership costs, analyse garage statistics, search/filter vehicles, sort garage data, and permanently store all records using JSON file handling.

---

## Project Roadmap

See the development roadmap here:

- V1.0 — Core CRUD System
- V2.0 — Full CRUD Expansion
- V2.1 — Garage Analytics System
- V2.2 — Date Validation System
- V2.3 — Search & Filter System
- V2.4 — Vehicle Sorting System
- V3.0 — Planned Web Dashboard Version

---

## Screenshots

### Startup Screen
![Startup Screen](screenshots/startup.png)

### Main Menu
![Main Menu](screenshots/main-menu.png)

### Service History
![Service History](screenshots/service-history.png)

### Garage Summary
![Garage Summary](screenshots/garage-summary.png)

---

## Overview

**KFZ Performance Garage Manager** was designed as a motorsport-inspired garage management tool.

It combines practical vehicle record keeping with a branded terminal interface, making it suitable for enthusiasts who want to track servicing, modifications, and total ownership cost across multiple vehicles.

The project evolved from a basic CRUD terminal application into a structured multi-version software system with analytics, filtering, sorting, validation, and modular system design.

This project was developed with a focus on:

- Object-Oriented Programming
- Object-Oriented System Design
- JSON data persistence
- Modular software architecture
- Input validation
- Search and filtering systems
- Sorting and ranking systems
- Terminal-based user experience
- Automotive-focused software design

---

# Key Features

## Vehicle Management

- Add new vehicles
- View all vehicles
- Search vehicles by plate/rego
- Delete vehicles
- Store multiple vehicles simultaneously

---

## Service Record Management

- Add service records
- View service history
- Edit service records
- Delete service records
- Track service dates
- Store odometer readings
- Store service costs

---

## Modification Record Management

- Add modification records
- View modification history
- Edit modification records
- Delete modification records
- Store modification categories
- Track aftermarket build costs

---

## Garage Analytics System

- Calculate total ownership cost
- Calculate garage-wide cost totals
- Display average ownership cost
- Find most expensive vehicle
- Find most modified vehicle
- Find highest service cost
- Find highest modification cost

---

## Search & Filter System

Search vehicles by:

- Make
- Year
- Plate/Rego
- Modification category

---

## Vehicle Sorting System

Sort vehicles by:

- Highest ownership cost
- Most modified vehicle
- Year
- Plate/Rego

---

## Date Validation System

- Validates all service dates
- Validates all modification dates
- Uses Python `datetime.strptime()`
- Prevents invalid date formats

Example accepted format:

```text
DD/MM/YYYY
```

---

## Data Persistence

- Save garage data to JSON
- Load garage data on startup
- Automatic save on exit
- Rebuild Python objects from JSON

---

## Technologies Used

- Python 3
- JSON file handling
- Object-Oriented Programming (OOP)
- Terminal UI systems
- Python datetime module
- Structured menu systems
- Formatted terminal table output

---

## Project Structure

```text
KFZ-Performance-Garage-Manager/
│
├── main.py
├── garage_data.json
├── README.md
│
└── screenshots/
    ├── startup.png
    ├── main-menu.png
    ├── service-history.png
    └── garage-summary.png
```

---

## How to Run

### 1. Install Python 3

Check Python version:

```bash
python3 --version
```

### 2. Open Terminal and navigate to the project folder

```bash
cd path/to/KFZ-Performance-Garage-Manager
```

### 3. Run the application

```bash
python3 main.py
```

---

## Example Use Cases

This system can be used to track:

- Daily driver maintenance
- Performance car service history
- Track car ownership costs
- Aftermarket build costs
- Workshop-style vehicle logs
- Garage-wide financial summaries
- Multi-vehicle enthusiast garages

Example vehicles:

- Subaru WRX STI
- Audi RSQ8
- Porsche GT3 RS
- BMW M3 / M4
- Nissan Skyline GT-R
- Toyota Supra

---

## Data Storage

Vehicle data is stored in:

```text
garage_data.json
```

Each vehicle record contains:

- Plate/Rego
- Make
- Model
- Year
- Service records
- Modification records

The application rebuilds Python class objects from the JSON file when loaded.

---

## Python Concepts Demonstrated

This project demonstrates:

- Classes and objects
- Object composition
- Lists of objects
- Nested loops
- Conditional logic
- Functions and methods
- Exception handling
- JSON reading and writing
- Input validation
- CRUD system architecture
- Search and filtering systems
- Sorting systems
- Analytics calculations
- Lambda expressions
- Python datetime validation
- Terminal UI design

---

## Future Development Roadmap

Planned future improvements include:

- CSV/PDF export system
- Rego & insurance reminders
- Vehicle image support
- PostgreSQL database integration
- Flask web dashboard
- User authentication system
- Cloud-based garage storage
- Mobile-friendly interface
- Multi-user garage profiles
- Workshop management dashboard
- Vehicle build timeline tracking

---

## Product Vision

The long-term vision of KFZ Performance Garage Manager is to evolve into a modern digital garage platform for automotive enthusiasts.

Rather than being only a simple vehicle record system, the platform is designed to grow into a premium ownership and build-tracking ecosystem focused on:

- Performance vehicles
- Garage analytics
- Maintenance history
- Modification tracking
- Automotive lifestyle management
- Enthusiast-focused user experience

Designed for enthusiasts who view their vehicles as more than transportation.

---

# Version History

## V2.4

- Added vehicle sorting system
- Sort by highest ownership cost
- Sort by most modified vehicle
- Sort by year
- Sort by plate/rego

---

## V2.3

- Added search and filter system
- Search by make
- Search by year
- Search by plate/rego
- Search by modification category

---

## V2.2

- Added date validation system
- Added datetime.strptime()
- Prevented invalid date inputs

---

## V2.1

- Added garage analytics system
- Added garage statistics dashboard
- Added highest-cost calculations
- Added average ownership calculations

---

## V2.0

- Added full CRUD management system
- Added edit/delete functionality
- Improved menu workflow
- Refactored system structure

---

## Author

Created by Kevin Zhang.

Project Concept:

**Performance Garage Manager for automotive enthusiasts and performance vehicle ownership tracking.**