#This is version 1 of my productivity application. It is a basic console foundation that can allow users to track tasks simply.

class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False

tasks = []

def display_menu():
    print("\n=== Productivity App ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

def add_task():
    
def view_tasks():

def complete_task():

def delete_task():


while True:
    display_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        # Add task

    elif choice == "2":
        # View tasks

    elif choice == "3":
        # Complete task

    elif choice == "4":
        # Delete task

    elif choice == "5":
        break

    else:
        print("Invalid option.")
