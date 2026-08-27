"""
This is version 3 of my productivity application.
It allows tasks to be saved to a JSON file so they
remain available when the application is reopened.
Users can also edit tasks, sort tasks by importance,
mark tasks as complete or incomplete, add tasks from
the task viewing screen, and confirm before deleting them.
"""
import tkinter as tk
#Messagebox to display errors in user input
from tkinter import messagebox
#Calendar for the user to input the due date of their tasks
from tkcalendar import Calendar
#Allowing the application to know the current date
from datetime import datetime, date
#JSON for storing tasks between application sessions
import json

#Creating the Task class, giving each task attributes
class Task:
    def __init__(self, title, time, deadline, importance, category):
        self.title = title
        self.time = time
        self.deadline = deadline
        self.importance = importance
        self.category = category
        #Initially all tasks are uncompleted
        self.completed = False

    #Method used to change a task's completion status
    def mark_complete(self):
        #Changes True to False or False to True
        self.completed = not self.completed

#Creating an empty list for tasks to be added to or removed from
tasks = []
#Stores the name of the user so it can be displayed throughout the application
user_name = ""
#Stores the name of the JSON file used to save tasks
#This is set once the user enters their name, so each user gets their own file
#and does not see or overwrite another user's tasks
FILE_NAME = "tasks.json"
#Stores the index of the task currently being edited
editing_index = None
#Stores the current calendar window so multiple calendars cannot be opened
calendar_window = None

#Turn the user's entered name into a safe file name
def get_file_name_for_user(name):
    #Replace spaces with underscores and remove characters that
    #are not letters, numbers or underscores
    safe_name = "".join(
        char if char.isalnum() or char == " " else ""
        for char in name
    ).strip().lower().replace(" ", "_")
    return f"tasks_{safe_name}.json"

#Save the current tasks to the JSON file
def save_tasks():
    task_data = []
    #Loop through every Task object so its attributes can be stored
    for task in tasks:
        task_data.append({
            "title": task.title,
            "time": task.time,
            "deadline": task.deadline,
            "importance": task.importance,
            "category": task.category,
            "completed": task.completed
        })
    #Open the JSON file so the current task data can be written to it
    with open(FILE_NAME, "w") as file:
        json.dump(task_data, file, indent=4)

#Load previously saved tasks from the JSON file
def load_tasks():
    try:
        #Open the JSON file containing the saved tasks
        with open(FILE_NAME, "r") as file:
            task_data = json.load(file)
        #Create a Task object for each saved task
        for data in task_data:
            task = Task(
                data["title"],
                data["time"],
                data["deadline"],
                data["importance"],
                data["category"]
            )
            #Restore whether the task was completed
            task.completed = data["completed"]
            tasks.append(task)
    except (FileNotFoundError, json.JSONDecodeError):
        #Start with an empty task list if the file is missing or invalid
        pass

#Refresh the listbox whenever tasks change
def refresh_tasks():
    task_list.delete(0, tk.END)
    #If there are no tasks currently
    if len(tasks) == 0:
        task_list.insert(tk.END, "NO TASKS TO VIEW.")
    else:
        #Loop through every Task object so its information can be displayed
        for i in range(len(tasks)):
            #Check the Boolean completed attribute of the current task
            if tasks[i].completed:
                status = "✓"
            else:
                status = "✗"
            #Display the task information using the attributes stored in each object
            task_list.insert(
                tk.END,
                f"{i + 1}. [{status}] {tasks[i].title} | "
                f"{tasks[i].time} min | "
                f"Due: {tasks[i].deadline} | "
                f"Importance: {'★' * tasks[i].importance} | "
                f"{tasks[i].category}"
            )

#Sort tasks from highest to lowest importance
def sort_tasks():
    #Sort the task objects using their importance attribute
    tasks.sort(key=lambda task: task.importance, reverse=True)
    refresh_tasks()

#Open the calendar
def open_calendar():
    global calendar_window
    #If a calendar is already open, bring it to the front instead
    if calendar_window is not None and calendar_window.winfo_exists():
        calendar_window.lift()
        calendar_window.focus_force()
        return

    calendar_window = tk.Toplevel(root)
    calendar_window.title("Select Deadline")
    calendar_window.geometry("300x300")
    #Get the current date
    today = date.today()
    #Create the calendar
    calendar = Calendar(
        calendar_window,
        selectmode="day",
        date_pattern="dd/mm/yyyy",
        mindate=today
    )
    calendar.pack(pady=20)

    #Save the selected date
    def select_date():
        global calendar_window
        deadline_entry.delete(0, tk.END)
        deadline_entry.insert(0, calendar.get_date())
        calendar_window.destroy()
        calendar_window = None

    #Button to select the date
    select_button = tk.Button(
        calendar_window,
        text="SELECT DATE",
        font=("Arial", 12, "bold"),
        width=22,
        height=2,
        command=select_date
    )
    select_button.pack(pady=10)

#Check the user's name and age before allowing access to the application
def check_user():
    global user_name, FILE_NAME
    #Get information entered by the user
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    #Check that a name is entered
    if name == "":
        messagebox.showerror("Error", "Please enter your name.")
        return
    #Check that an age is entered
    if age == "":
        messagebox.showerror("Error", "Please enter your age.")
        return
    #Check that the age entered is a number
    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number.")
        return
    #Check that the user is old enough to use the application
    if int(age) < 12:
        messagebox.showerror(
            "Access denied",
            "You must be at least 12 years old to use this application."
        )
        root.destroy()
        return
    #Check that the age entered is realistic
    if int(age) > 120:
        messagebox.showerror(
            "Invalid age",
            "Please enter your real age."
        )
        return
    #Store the user's name so it can be used by the other frames
    user_name = name
    #Work out which JSON file belongs to this user
    FILE_NAME = get_file_name_for_user(user_name)
    #Clear any tasks left over from a previous user in this session
    tasks.clear()
    #Load this user's own saved tasks, if any exist
    load_tasks()
    #Change the headings to greet the user by name
    main_title.config(text=f"WELCOME, {user_name.upper()}!")
    add_title.config(
        text=f"ADD A TASK YOU WISH TO COMPLETE, {user_name.upper()}"
    )
    tasks_title.config(text=f"{user_name.upper()}'S TASKS")
    #Show the main menu after the user's information has been accepted
    show_main_frame()

#Check that all task information is valid
def validate_task_input():
    #Get the text entered by the user
    title = task_entry.get().strip()
    time = time_entry.get().strip()
    deadline = deadline_entry.get().strip()
    importance = len(importance_var.get())
    category = category_var.get()
    #If the user does not enter anything for the task
    if title == "":
        messagebox.showerror("Error", "Task cannot be empty.")
        return None
    #Check that a time has been entered
    if time == "":
        messagebox.showerror(
            "Error",
            "Please enter how long you think this task will take."
        )
        return None
    #Check that the time entered is a number
    if not time.isdigit():
        messagebox.showerror(
            "Error",
            "Time allocation must be a number."
        )
        return None
    #Check that the time entered is greater than zero
    if int(time) <= 0:
        messagebox.showerror(
            "Error",
            "Time allocation must be greater than zero."
        )
        return None
    #Convert the time to an integer
    time = int(time)
    #Check that a deadline has been entered
    if deadline == "":
        messagebox.showerror(
            "Error",
            "Please select a date from the calendar or type one manually."
        )
        return None
    #Check that the deadline is a valid date
    try:
        deadline_date = datetime.strptime(
            deadline,
            "%d/%m/%Y"
        ).date()
    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid date in DD/MM/YYYY format."
        )
        return None
    #Check that the deadline is not before today
    if deadline_date < date.today():
        messagebox.showerror(
            "Error",
            "The deadline cannot be before today."
        )
        return None
    return title, time, deadline, importance, category

#Allow user to add new tasks
def add_task():
    #Get validated task information
    task_data = validate_task_input()
    if task_data is None:
        return
    #Create a new Task object using the user's input
    task = Task(
        task_data[0],
        task_data[1],
        task_data[2],
        task_data[3],
        task_data[4]
    )
    #Add the new Task object to the list
    tasks.append(task)
    #Save the updated task list to the JSON file
    save_tasks()
    #Clear the input fields after adding the task
    clear_task_fields()
    #Return the cursor to the task entry box
    task_entry.focus()
    messagebox.showinfo("Success", "Task added successfully.")

#Open the selected task for editing
def edit_task():
    global editing_index
    #Find out which item the user has currently selected
    selection = task_list.curselection()
    if len(tasks) == 0:
        messagebox.showerror("Error", "No tasks to edit.")
        return
    #Check if the user has selected a task
    if not selection:
        messagebox.showerror(
            "Error",
            "Please select a task to edit."
        )
        return
    #curselection returns the selected Listbox position as a tuple
    #The first value gives the position of the selected task
    editing_index = selection[0]
    #Get the selected Task object
    selected_task = tasks[editing_index]
    #Put the existing information into the input fields
    task_entry.delete(0, tk.END)
    task_entry.insert(0, selected_task.title)
    time_entry.delete(0, tk.END)
    time_entry.insert(0, selected_task.time)
    deadline_entry.delete(0, tk.END)
    deadline_entry.insert(0, selected_task.deadline)
    importance_var.set("★" * selected_task.importance)
    category_var.set(selected_task.category)
    #Change the button so it saves the edited task
    add_button.config(
        text="SAVE CHANGES",
        command=save_edit
    )
    add_title.config(
        text=f"EDIT A TASK, {user_name.upper()}"
    )
    show_add_frame()

#Save changes made to an existing task
def save_edit():
    #Get validated task information
    task_data = validate_task_input()
    if task_data is None:
        return
    #Get the Task object being edited
    task = tasks[editing_index]
    #Update the object's attributes
    task.title = task_data[0]
    task.time = task_data[1]
    task.deadline = task_data[2]
    task.importance = task_data[3]
    task.category = task_data[4]
    #Save the updated task list
    save_tasks()
    #Clear the input fields
    clear_task_fields()
    #Reset the button to its normal add-task function
    reset_add_screen()
    messagebox.showinfo("Success", "Task updated successfully.")
    show_tasks_frame()

#Clear the task input fields
def clear_task_fields():
    task_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    importance_var.set("★★★")
    category_var.set("School")

#Reset the add task screen after editing
def reset_add_screen():
    global editing_index
    editing_index = None
    add_button.config(
        text="ADD TASK",
        command=add_task
    )
    add_title.config(
        text=f"ADD A TASK YOU WISH TO COMPLETE, {user_name.upper()}"
    )

#Let user mark a task as complete or incomplete
def complete_task():
    #Find out which item the user has currently selected
    selection = task_list.curselection()
    if len(tasks) == 0:
        messagebox.showerror("Error", "There are no tasks.")
        return
    #Check if the user has selected a task
    if not selection:
        messagebox.showerror(
            "Error",
            "Please select a task first."
        )
        return
    #Get the index of the selected task
    index = selection[0]
    #Call the method to switch between complete and incomplete
    tasks[index].mark_complete()
    #Save the updated task
    save_tasks()
    refresh_tasks()

#Delete a task
def delete_task():
    #Find out which item the user has currently selected
    selection = task_list.curselection()
    if len(tasks) == 0:
        messagebox.showerror("Error", "No tasks to delete.")
        return
    #Check if the user has selected a task
    if not selection:
        messagebox.showerror(
            "Error",
            "Please select a task to delete."
        )
        return
    #Get the index of the selected task
    index = selection[0]
    #Ask the user to confirm deletion
    answer = messagebox.askyesno(
        "Confirm deletion",
        "Are you sure you want to delete this task?"
    )
    if answer:
        #Remove the selected task
        tasks.pop(index)
        #Save the updated task list
        save_tasks()
        refresh_tasks()

#Open the add task screen from the task viewing screen
def add_task_from_view():
    clear_task_fields()
    reset_add_screen()
    show_add_frame()

#Confirm if the user wants to exit the application
def exit_application():
    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )
    if answer:
        root.destroy()

#Show the main menu frame
def show_main_frame():
    #If the user leaves the add screen, reset it
    reset_add_screen()
    clear_task_fields()
    main_frame.tkraise()

#Show the add task frame
def show_add_frame():
    add_frame.tkraise()
    task_entry.focus()

#Show the tasks frame
def show_tasks_frame():
    tasks_frame.tkraise()
    refresh_tasks()

#Main application window
root = tk.Tk()
root.title("PRODUCTIVITY APP")
root.geometry("700x700")

#User information frame
setup_frame = tk.Frame(
    root,
    bg="#9CC4D4"
)
setup_frame.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

#User information title
setup_title = tk.Label(
    setup_frame,
    text="WELCOME TO THE PRODUCTIVITY APP",
    font=("Arial", 26, "bold"),
    bg="#9CC4D4"
)
setup_title.pack(pady=70)

#Name label
name_label = tk.Label(
    setup_frame,
    text="Enter your name:",
    font=("Arial", 14, "bold"),
    bg="#9CC4D4"
)
name_label.pack()

#Name entry
name_entry = tk.Entry(
    setup_frame,
    width=30,
    font=("Arial", 14)
)
name_entry.pack(pady=5)

#Age label
age_label = tk.Label(
    setup_frame,
    text="Enter your age:",
    font=("Arial", 14, "bold"),
    bg="#9CC4D4"
)
age_label.pack(pady=(10, 0))

#Age entry
age_entry = tk.Entry(
    setup_frame,
    width=30,
    font=("Arial", 14)
)
age_entry.pack(pady=5)

#Button to continue to the application
continue_button = tk.Button(
    setup_frame,
    text="CONTINUE",
    font=("Arial", 14, "bold"),
    width=22,
    height=2,
    command=check_user
)
continue_button.pack(pady=20)

#Main menu frame
main_frame = tk.Frame(
    root,
    bg="#9CC4D4"
)
main_frame.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

#Main menu title
main_title = tk.Label(
    main_frame,
    text="PRODUCTIVITY APP",
    font=("Arial", 28, "bold"),
    bg="#9CC4D4"
)
main_title.pack(pady=70)

#Button to open the add task frame
add_task_menu_button = tk.Button(
    main_frame,
    text="ADD TASK",
    font=("Arial", 14, "bold"),
    width=22,
    height=2,
    command=show_add_frame
)
add_task_menu_button.pack(pady=10)

#Button to open the tasks frame
view_tasks_button = tk.Button(
    main_frame,
    text="VIEW TASKS",
    font=("Arial", 14, "bold"),
    width=22,
    height=2,
    command=show_tasks_frame
)
view_tasks_button.pack(pady=10)

#Button to close the application
exit_button = tk.Button(
    main_frame,
    text="EXIT",
    font=("Arial", 14, "bold"),
    width=22,
    height=2,
    command=exit_application
)
exit_button.pack(pady=10)

#Add task frame
add_frame = tk.Frame(
    root,
    bg="#A8CFA8"
)
add_frame.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

#Add task title
add_title = tk.Label(
    add_frame,
    text="ADD A TASK YOU WISH TO COMPLETE",
    font=("Arial", 26, "bold"),
    bg="#A8CFA8"
)
add_title.pack(pady=25)

#Task title
title_label = tk.Label(
    add_frame,
    text="ENTER TASK",
    font=("Arial", 14, "bold"),
    bg="#A8CFA8"
)
title_label.pack()

task_entry = tk.Entry(
    add_frame,
    width=30,
    font=("Arial", 14)
)
task_entry.pack(pady=5)

#Time allocation
time_label = tk.Label(
    add_frame,
    text="ESTIMATED TIME TO COMPLETE TASK (MINUTES)",
    font=("Arial", 12, "bold"),
    bg="#A8CFA8"
)
time_label.pack(pady=(8, 0))

time_entry = tk.Entry(
    add_frame,
    width=30,
    font=("Arial", 14)
)
time_entry.pack(pady=5)

#Deadline
deadline_label = tk.Label(
    add_frame,
    text="DEADLINE:",
    font=("Arial", 14, "bold"),
    bg="#A8CFA8"
)
deadline_label.pack(pady=(8, 0))

#Button to open the calendar
calendar_button = tk.Button(
    add_frame,
    text="📅  SELECT DATE",
    font=("Arial", 12, "bold"),
    width=22,
    height=2,
    command=open_calendar
)
calendar_button.pack(pady=5)

#Manual date label
manual_date_label = tk.Label(
    add_frame,
    text="TYPE DATE MANUALLY (DD/MM/YYYY):",
    font=("Arial", 11, "bold"),
    bg="#A8CFA8"
)
manual_date_label.pack(pady=(2, 0))

deadline_entry = tk.Entry(
    add_frame,
    width=22,
    font=("Arial", 14)
)
deadline_entry.pack(pady=5)

#Importance rating
importance_label = tk.Label(
    add_frame,
    text="IMPORTANCE:",
    font=("Arial", 14, "bold"),
    bg="#A8CFA8"
)
importance_label.pack(pady=(8, 0))

importance_var = tk.StringVar(value="★★★")

#Create the importance rating options
importance_menu = tk.OptionMenu(
    add_frame,
    importance_var,
    "★",
    "★★",
    "★★★",
    "★★★★",
    "★★★★★"
)
importance_menu.config(
    font=("Arial", 12),
    width=22,
    height=2
)
importance_menu.pack(pady=5)

#Task category
category_label = tk.Label(
    add_frame,
    text="CATEGORY:",
    font=("Arial", 14, "bold"),
    bg="#A8CFA8"
)
category_label.pack(pady=(8, 0))

category_var = tk.StringVar(value="School")

category_menu = tk.OptionMenu(
    add_frame,
    category_var,
    "School",
    "Home",
    "Fitness",
    "Family",
    "Other"
)
category_menu.config(
    font=("Arial", 12),
    width=22,
    height=2
)
category_menu.pack(pady=5)

#Button to add or save a task
add_button = tk.Button(
    add_frame,
    text="ADD A TASK",
    font=("Arial", 12, "bold"),
    width=22,
    height=2,
    command=add_task
)
add_button.pack(pady=8)

#Button to return to the main menu
back_from_add_button = tk.Button(
    add_frame,
    text="BACK",
    font=("Arial", 13, "bold"),
    width=22,
    height=2,
    command=show_main_frame
)
back_from_add_button.pack(pady=5)

#Tasks frame
tasks_frame = tk.Frame(
    root,
    bg="#D6D69B"
)
tasks_frame.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

#Tasks title
tasks_title = tk.Label(
    tasks_frame,
    text="YOUR TASKS",
    font=("Arial", 26, "bold"),
    bg="#D6D69B"
)
tasks_title.pack(pady=25)

#Task list
task_list = tk.Listbox(
    tasks_frame,
    width=75,
    height=12,
    font=("Arial", 12)
)
task_list.pack(pady=10)

#Button to add a task directly from the task viewing screen
view_add_button = tk.Button(
    tasks_frame,
    text="ADD TASK",
    font=("Arial", 13, "bold"),
    width=22,
    height=2,
    command=add_task_from_view
)
view_add_button.pack(pady=4)

#Button to sort tasks by importance
sort_button = tk.Button(
    tasks_frame,
    text="SORT BY IMPORTANCE",
    font=("Arial", 13, "bold"),
    width=22,
    height=2,
    command=sort_tasks
)
sort_button.pack(pady=4)

#Button to mark a task as complete or incomplete
complete_button = tk.Button(
    tasks_frame,
    text="COMPLETE / INCOMPLETE",
    font=("Arial", 13, "bold"),
    width=22,
    height=2,
    command=complete_task
)
complete_button.pack(pady=4)

#Button to edit a task
edit_button = tk.Button(
    tasks_frame,
    text="EDIT TASK",
    font=("Arial", 13, "bold"),
    width=22,
    height=2,
    command=edit_task
)
edit_button.pack(pady=4)

#Button to delete a task
delete_button = tk.Button(
    tasks_frame,
    text="DELETE TASK",
    font=("Arial", 13, "bold"),
    width=22,
    height=2,
    command=delete_task
)
delete_button.pack(pady=4)

#Button to return to the main menu
back_from_tasks_button = tk.Button(
    tasks_frame,
    text="BACK",
    font=("Arial", 13, "bold"),
    width=22,
    height=2,
    command=show_main_frame
)
back_from_tasks_button.pack(pady=10)

#Tasks are now loaded per-user inside check_user(), once we know
#who is using the application, instead of being loaded here

#Show the user information screen when the application starts
setup_frame.tkraise()
name_entry.focus()

#The application keeps running until the window is closed
root.mainloop()
