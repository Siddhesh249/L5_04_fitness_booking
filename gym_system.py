"""Fitness Club Class Booking Ledger.

This module provides functionality to manage gym class rosters,
set class capacities, book and cancel classes, and export/import
schedules to and from JSON files.
"""

import glob
import json
import os

# Global state
class_capacity = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}


def book_class(member_id, class_name, attendance_log=None):
    """Book a member into a specified fitness class.

    Args:
        member_id: The ID of the member booking the class.
        class_name: The name of the fitness class.
        attendance_log: Optional list to record attendance.

    Returns:
        bool: True if booking was successful, False otherwise.
    """
    if attendance_log is None:
        attendance_log = []
    if class_name not in rosters:
        rosters[class_name] = []
    if len(rosters[class_name]) >= class_capacity.get(class_name, 0):
        print("Class full:", class_name)
        return False
    rosters[class_name].append(member_id)
    attendance_log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Cancel an existing booking for a member in a class.

    Args:
        member_id: The ID of the member whose booking is to be cancelled.
        class_name: The name of the fitness class.
    """
    try:
        rosters[class_name].remove(member_id)
    except (KeyError, ValueError):
        print("Nothing to cancel")


def set_capacity(class_name, seats):
    """Set the maximum seating capacity for a given class.

    Args:
        class_name: The name of the fitness class.
        seats: The maximum number of members allowed in the class.
    """
    if seats < 0:
        print(f"Invalid capacity for {class_name}: {seats}. "
              "Capacity must be non-negative.")
        return
    class_capacity[class_name] = seats


def add_members(class_name, count):
    """Add multiple guest members to a class roster.

    Args:
        class_name: The name of the fitness class.
        count: The number of guest members to book.
    """
    for i in range(count):
        book_class("GUEST-" + str(i), class_name)


def export_roster(filepath="gym_schedule.json"):
    """Export the current class rosters to a JSON file.

    Args:
        filepath: The path to the destination JSON file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rosters, f)


def clear_old_exports(prefix="old_"):
    """Safely remove previous JSON export files matching a given prefix.

    Args:
        prefix: Filename prefix pattern to match old export files.
    """
    for file_path in glob.glob(prefix + "*.json"):
        try:
            os.remove(file_path)
        except OSError:
            pass


def show_rosters():
    """Print the rosters for all fitness classes."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(str(m) for m in members))


def main():
    """Execute the fitness class booking demonstration."""
    book_class("M1", "Yoga")
    book_class("M2", "Yoga")
    book_class("M3", "Yoga")
    book_class("M4", "Yoga")
    book_class(55, "HIIT")
    book_class("M5", "Pilates")
    set_capacity("Spin", -2)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")
    n = input("How many walk-in guests for HIIT? (Enter for 1): ") or "1"
    try:
        guest_count = int(n)
        if guest_count < 0:
            print("Invalid guest count; defaulting to 1.")
            guest_count = 1
    except ValueError:
        print("Invalid input; defaulting to 1.")
        guest_count = 1
    add_members("HIIT", guest_count)
    clear_old_exports()
    export_roster()
    show_rosters()


if __name__ == "__main__":
    main()
