import csv
from datetime import datetime

# Define the Employee class
class Employee:
    def __init__(self, emp_id, name):
        self.emp_id = emp_id
        self.name = name

    def __repr__(self):
        return f"Employee(ID: {self.emp_id}, Name: {self.name})"

    def to_dict(self):
        """Convert the Employee object to a dictionary."""
        return {"emp_id": self.emp_id, "name": self.name}

    @staticmethod
    def from_dict(data):
        """Create an Employee object from a dictionary."""
        return Employee(data["emp_id"], data["name"])

# Define the AttendanceManager class
class AttendanceManager:
    def __init__(self, employees_file="employees.csv", attendance_file="attendance.csv"):
        self.employees_file = employees_file
        self.attendance_file = attendance_file
        self.employees = self.load_employees()
        self.attendance_records = self.load_attendance()

    def load_employees(self):
        """Load employee data from the employees CSV file."""
        employees = []
        try:
            with open(self.employees_file, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    employees.append(Employee.from_dict(row))
        except FileNotFoundError:
            print("Employees file not found. No employees data available.")
        return employees

    def load_attendance(self):
        """Load attendance records from the attendance CSV file."""
        attendance = []
        try:
            with open(self.attendance_file, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    attendance.append(row)
        except FileNotFoundError:
            print("Attendance file not found. No attendance records available.")
        return attendance

    def save_employees(self):
        """Save employee data to the employees CSV file."""
        with open(self.employees_file, "w", newline="") as file:
            fieldnames = ["emp_id", "name"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for emp in self.employees:
                writer.writerow(emp.to_dict())

    def save_attendance(self):
        """Save attendance records to the attendance CSV file."""
        with open(self.attendance_file, "w", newline="") as file:
            fieldnames = ["emp_id", "date", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.attendance_records:
                writer.writerow(record)

    def add_employee(self, name):
        """Add a new employee."""
        emp_id = len(self.employees) + 1  # Generate employee ID
        new_employee = Employee(emp_id, name)
        self.employees.append(new_employee)
        self.save_employees()
        print(f"Employee {name} added successfully.")

    def mark_attendance(self, emp_id, status):
        """Mark attendance for an employee."""
        date = datetime.now().strftime("%Y-%m-%d")
        record = {
            "emp_id": emp_id,
            "date": date,
            "status": status
        }
        self.attendance_records.append(record)
        self.save_attendance()
        print(f"Attendance for Employee ID {emp_id} on {date} marked as {status}.")

    def view_attendance(self, emp_id=None):
        """View attendance for all employees or a specific employee."""
        if emp_id:
            # View attendance for a specific employee
            records = [record for record in self.attendance_records if record["emp_id"] == emp_id]
        else:
            # View all attendance records
            records = self.attendance_records

        if not records:
            print("No attendance records found.")
        else:
            for record in records:
                emp_name = next((emp.name for emp in self.employees if emp.emp_id == int(record["emp_id"])), "Unknown")
                print(f"Employee: {emp_name}, ID: {record['emp_id']}, Date: {record['date']}, Status: {record['status']}")

    def generate_report(self, start_date, end_date):
        """Generate attendance report for a specific date range."""
        filtered_records = [record for record in self.attendance_records if start_date <= record["date"] <= end_date]
        if not filtered_records:
            print("No attendance records found for the given date range.")
        else:
            print(f"Attendance report from {start_date} to {end_date}:")
            for record in filtered_records:
                emp_name = next((emp.name for emp in self.employees if emp.emp_id == int(record["emp_id"])), "Unknown")
                print(f"Employee: {emp_name}, ID: {record['emp_id']}, Date: {record['date']}, Status: {record['status']}")

# Main program for the Employee Attendance System
def main():
    attendance_manager = AttendanceManager()

    while True:
        print("\nEmployee Attendance System")
        print("1. Add Employee")
        print("2. Mark Attendance")
        print("3. View Attendance")
        print("4. Generate Attendance Report")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter employee name: ")
            attendance_manager.add_employee(name)

        elif choice == '2':
            emp_id = int(input("Enter employee ID: "))
            status = input("Enter status (Present/Absent): ").capitalize()
            if status in ["Present", "Absent"]:
                attendance_manager.mark_attendance(emp_id, status)
            else:
                print("Invalid status. Please enter 'Present' or 'Absent'.")

        elif choice == '3':
            emp_id = input("Enter employee ID to view attendance (leave blank to view all): ")
            if emp_id:
                attendance_manager.view_attendance(int(emp_id))
            else:
                attendance_manager.view_attendance()

        elif choice == '4':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            attendance_manager.generate_report(start_date, end_date)

        elif choice == '5':
            print("Exiting Employee Attendance System.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
