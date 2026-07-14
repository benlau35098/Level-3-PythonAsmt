'''This is version 1 of my productivity application. It is a basic console foundation that allows users to track tasks simply.
It contains usage of a class, method, and functions.'''

#Creating the Task class, giving each task attributes
class Task:
    def __init__(self, title):
        self.title = title
        #initially all tasks are uncompleted
        self.completed = False


tasks = []

#Set of choices the user can make
def display_menu():
    print("\n============ Productivity App ============")
    print("1. Add a Task")
    print("2. View all Tasks")
    print("3. Mark Task as Complete")
    print("4. Delete Task")
    print("5. Exit")

#Allow user to add new tasks
def add_task():
    
    while True:
       title = input("Enter the name of a task you wish to do: ")
       
       if title == "":
           print("Task cannot be empty.")
           

       else:
           task = Task(title)
           tasks.append(task)
           print("Task added.")
           break

#Let user view existing tasks, completed or otherwise
def view_tasks():
    if len(tasks) == 0:
        print("No tasks to view.")
    else:
        print("\nTasks:")
        #Using crosses and ticks to show the user whether each task is completed or not
        for i in range(len(tasks)):
            if tasks[i].completed:
                status = "✓"
            else:
                status = "✗"

            print(f"{i + 1}. [{status}] {tasks[i].title}")

#Let user mark a task as complete
def complete_task():
    if len(tasks) == 0:
        print("No tasks to complete.")
        return

    view_tasks()
    while True:
        try:
            task_number = int(input("Enter task number to mark as complete: "))
            #ensuring that the input is valid
            if 1 <= task_number <= len(tasks):
                #accounting for index numbers being 1 less than counting numbers
                tasks[task_number - 1].completed = True
                print("Successfully marked task completed.")
                break
            else:
                print("Invalid task number.")

        except ValueError:
            print("Please enter a valid number.")


def delete_task():
    #Message if there are no current tasks
    if len(tasks) == 0:
        print("No tasks to delete.")
        return

    view_tasks()
    while True:
        try:
            task_number = int(input("Enter task number to delete: "))
            #Ensuring inputted number is valid (falls within the possible range of number of tasks)
            if 1 <= task_number <= len(tasks):
                
                deleted = tasks.pop(task_number - 1)
                print(f"Deleted '{deleted.title}'.")
                break
            else:
                print("Invalid task number.")

        except ValueError:
            print("Please enter a valid number.")


while True:
    #Repeatedly calling display menu function for the user to see all the choices both initially and after making any choice aside from exit.
    display_menu()
    choice = input("Enter an option (1-5): ")
    #calling specific functions performing different features of the application based on user input
    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        complete_task()

    elif choice == "4":
        delete_task()

    elif choice == "5":
        print("Thank you for using the application. Goodbye!")
        break
    elif choice == "":
        print("Choice cannot be blank.")

    else:
        print("Invalid option.")
