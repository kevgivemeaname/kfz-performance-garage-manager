# KFZ Performance Garage Manager

A terminal-based vehicle management system built in Python for automotive enthusiasts, performance car owners, and garage-style record keeping.

The system allows users to manage multiple vehicles, record service history, track aftermarket modifications, calculate ownership costs, and store all garage data permanently using JSON file handling.

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


## Overview

**KFZ Performance Garage Manager** was designed as a motorsport-inspired garage management tool.  
It combines practical vehicle record keeping with a branded terminal interface, making it suitable for car enthusiasts who want to track servicing, modifications, and total build cost across multiple vehicles.

This project was developed as a Python-based system with a focus on:

- Object-Oriented Programming
- File handling with JSON
- Input validation
- Menu-driven terminal interaction
- Persistent data storage
- Clean formatted output
- Automotive-focused user experience

---

## Key Features

### Vehicle Management

- Add new vehicles
- View all vehicles in the garage
- Search vehicles by plate/rego
- Delete vehicles from the garage

### Service Records

- Add service records for a selected vehicle
- Store service date, description, odometer reading, and cost
- View formatted service history per vehicle

### Modification Records

- Add aftermarket modification records
- Store modification date, part name, category, and cost
- View modification history per vehicle

### Cost Tracking

- Calculate total service cost per vehicle
- Calculate total modification cost per vehicle
- Display overall ownership cost per vehicle
- Display total garage-wide cost summary

### Data Persistence

- Save garage data to a JSON file
- Load previously saved garage data on startup
- Automatically save data when exiting the program

---

## Technologies Used

- Python 3
- JSON file handling
- Object-Oriented System Design
- Object-Oriented Programming
- Terminal-based user interface
- Formatted table output

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

1. Make sure Python 3 is installed.

2. Open Terminal and navigate to the project folder:

```bash
cd path/to/KFZ-Performance-Garage-Manager
```

3. Run the program:

```bash
python3 main.py
```

---

## Example Use Cases

This system can be used to track:

- Daily driver maintenance
- Performance car service history
- Track car build costs
- Aftermarket modification records
- Workshop-style vehicle logs
- Ownership cost summaries

Example vehicles:

- Subaru WRX STI
- Audi RSQ8
- BMW M3 / M4
- Porsche GT3
- Nissan Skyline GT-R
- Toyota Supra

---

## Data Storage

Vehicle data is stored in `garage_data.json`.

Each vehicle record contains:

- Plate / rego
- Make
- Model
- Year
- Service records
- Modification records

The program rebuilds Python objects from the JSON file when loaded.

---

## Python Concepts Demonstrated

This project demonstrates several core Python concepts:

- Classes and objects
- Instance attributes
- Lists of objects
- Loops and conditional statements
- Functions and methods
- Exception handling
- JSON reading and writing
- String formatting
- User input validation
- Terminal menu design

---

## Future Development Roadmap

Possible future improvements include:

- Date format validation
- Edit service and modification records
- Export reports to CSV or PDF
- Rego and insurance expiry reminders
- Search and filter records
- Vehicle photo support
- Web dashboard version
- User login system
- Database integration with PostgreSQL
- Mobile-friendly interface
- Workshop management dashboard
- Performance build tracking
- Cloud-based garage storage
- Multi-user garage profiles

---

## Product Vision

The long-term vision of KFZ Performance Garage Manager is to become a digital garage platform for automotive enthusiasts.

Rather than being only a basic vehicle record system, it can evolve into a premium ownership and build-tracking tool for people who care about performance cars, modifications, maintenance, and car culture.

Designed for enthusiasts who view their vehicles as more than transportation.

---

## Author

Created by Kevin Zhang.

Project concept:  
**Performance Garage Manager for automotive enthusiasts and performance vehicle ownership tracking.**
