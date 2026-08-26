""" 
This is version 2 of my productivity application.  It incorporates distinct frames to better organise the graphical user interface, 
making the application appear more professional to navigate. Tasks are given time allocations and are categorized according
to their type and their priority rating to give the user more insight. The application also uses a calendar for selecting deadlines. 
The pack method is used to organize the layout of widgets in each frame. Users are now asked for their name for a more personalized
experience, as well as their age to ensure that people of the appropriate age are utilizing the application.
""" 

import tkinter as tk 
#Messagebox to display important messages to the user 
from tkinter import messagebox 
#Calendar for the user to input the due date of their tasks 
from tkcalendar import Calendar 
#Allowing the application to know the current date 
from datetime import datetime, date 
 
#Creating the Task class, giving each object (task) attributes 
class Task: 
    def __init__(self, title, time, deadline, importance, category): #task attributes being initialized

        #Stores the task title as an attribute of the task object, so each task can have its own title.
        self.title = title 
        self.time = time 
        self.deadline = deadline 
        self.importance = importance 
        self.category = category 
 
        #Completed attribute, initially all tasks are not yet completed
        self.completed = False 
 
    #Method used to change a task's completion status 
    def mark_complete(self): 
        self.completed = True 
 
#Creating an empty list for tasks to be added to or removed from 
tasks = [] 
 
#Storing the name of the user so it can be displayed throughout the application 
user_name = "" 
 
#Refresh the listbox whenever tasks change 
def refresh_tasks(): 
    task_list.delete(0, tk.END) 
 
    #If there are no tasks currently 
    if len(tasks) == 0: 
        task_list.insert(tk.END, "NO TASKS TO VIEW.") 
    else: 
        #Loop through every Task object in the list so its attributes can be displayed 
        for i in range(len(tasks)): 
 
            #Check the Boolean completed attribute of the current task 
            if tasks[i].completed: 
                status = "✓" 
            else: 
                status = "✗" 
 
            #Display the task information, using the attributes stored in each Task object 
            task_list.insert( 
                tk.END, 
                f"{i + 1}. [{status}] {tasks[i].title} | " 
                f"{tasks[i].time} min | " 
                f"Due: {tasks[i].deadline} | " 
                f"Importance: {'★' * tasks[i].importance} | " 
                f"{tasks[i].category}" 
            ) 
 
#Open the calendar 
def open_calendar(): 
    calendar_window = tk.Toplevel(root)#creates a new window for the calendar 
    calendar_window.title("Select Deadline") 
    calendar_window.geometry("300x300") 
 
    #Getting the current date 
    today = date.today() 
 
    #Creating the calendar 
    calendar = Calendar( 
        calendar_window, 
        selectmode="day", 
        date_pattern="dd/mm/yyyy", 
        mindate=today 
    ) 
    calendar.pack(pady=20) 
 
    #Save the selected date 
    def select_date(): 
        deadline_entry.delete(0, tk.END) 
        deadline_entry.insert(0, calendar.get_date()) 
        calendar_window.destroy() 
 
    #Button to select the date 
    select_button = tk.Button( 
        calendar_window, 
        text="SELECT DATE", 
        font=("Arial", 12, "bold"), 
        command=select_date 
    ) 
    select_button.pack(pady=10) 
 
#Check the user's name and age before giving access to the application 
def check_user():
    #Allow the user's name to be accessed by the rest of the program
    global user_name 
 
    #Get information entered by the user 
    name = name_entry.get().strip()#.strip() removes accidental spaces
    age = age_entry.get().strip()#Currently gets age as a string, this will be converted to integer later. 
 
    #Check that a name is entered 
    if name == "": 
        messagebox.showerror( 
            "Error", 
            "Please enter your name." 
        ) 
        return 
 
    #Check that an age is entered 
    if age == "": 
        messagebox.showerror( 
            "Error", 
            "Please enter your age." 
        ) 
        return 
 
    #Check that the age entered is a integer 
    if not age.isdigit(): 
        messagebox.showerror( 
            "Error", 
            "Age must be an integer." 
        ) 
        return

    #converts age from a string to an integer
    age = int(age)
 
   
    #Check that the age entered is realistic 
    if age > 120: 
        messagebox.showerror( 
            "Invalid age", 
            "Please enter your real age." 
        ) 
        return

    #Check that the user is old enough to use the application 
    if age < 12: 
        messagebox.showerror( 
            "Access denied", 
            "You must be at least 12 years old to use this application." 
        ) 
        root.destroy() 
        return

 
    #Store the user's name so it can be used anywhere in the program
    user_name = name 
 
    #Change the headings to greet the user by name 
    main_title.config( 
        text=f"WELCOME, {user_name.upper()}!" 
    ) 
 
    add_title.config( 
        text=f"ADD A TASK, {user_name.upper()}" 
    ) 
 
    tasks_title.config( 
        text=f"{user_name.upper()}'S TASKS" 
    ) 
 
    #Show the main menu after the user's information has been accepted 
    show_main_frame() 
 
#Allow user to add new tasks 
def add_task(): 
    #Get the text entered by the user 
    title = task_entry.get().strip() 
    time = time_entry.get().strip() 
    deadline = deadline_entry.get().strip() 
    importance = len(importance_var.get()) 
    category = category_var.get() 
 
    #If the user does not enter anything for adding a new task 
    if title == "": 
        messagebox.showerror( 
            "Error", 
            "Task cannot be empty." 
        ) 
        return 
 
    #Check that a time has been entered 
    if time == "": 
        messagebox.showerror( 
            "Error", 
            "Please enter a time allocation." 
        ) 
        return 
 
    #Check that the time entered is a number 
    if not time.isdigit(): 
        messagebox.showerror( 
            "Error", 
            "Time allocation must be an integer." 
        ) 
        return 
 
    #Check that the time entered is greater than zero 
    if int(time) <= 0: 
        messagebox.showerror( 
            "Error", 
            "Time allocation must be greater than zero." 
        ) 
        return 
 
    #Convert the time to an integer so the Task object stores it as a number 
    time = int(time) 
 
    #Check that a deadline has been entered 
    if deadline == "": 
        messagebox.showerror( 
            "Error", 
            "Please select or enter a deadline." 
        ) 
        return 
 
    #Check that deadline is a valid date in the correct format
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
        return 
 
    #Check that the deadline is not before today 
    if deadline_date < date.today(): 
        messagebox.showerror( 
            "Error", 
            "The deadline cannot be before today." 
        ) 
        return 
 
    #Create a new Task object using the user's inputs
    task = Task(title, time, deadline, importance, category) 
 
    #Add the new Task object to the list so it can later be displayed, completed or deleted 
    tasks.append(task) 
 
    #Clear the input fields after adding the task 
    task_entry.delete(0, tk.END) 
    time_entry.delete(0, tk.END) 
    deadline_entry.delete(0, tk.END) 
 
    #Return the cursor to the task entry box by default
    task_entry.focus() 
 
    messagebox.showinfo( 
        "Success", 
        "Task added successfully." 
    ) 
 
#Let user mark a task as complete 
def complete_task(): 
    #curselection returns the task the user has currently selected as a tuple
    selection = task_list.curselection() 
    #Identify if there are no current tasks
    if len(tasks) == 0: 
        messagebox.showerror( 
            "Error", 
            "No tasks to mark as complete." 
        ) 
        return 
 
    #Check if the user has selected a task 
    if not selection: 
        messagebox.showerror( 
            "Error", 
            "Please select a task to complete." 
        ) 
        return 
 
    #Get the index of the selected task so it matches its position in the tasks list 
    index = selection[0] 
 
    #Call the Task object's method to change its completion status 
    tasks[index].mark_complete() 
    refresh_tasks() 
 
#Delete a task 
def delete_task(): 
    #Find out which item the user has currently selected 
    selection = task_list.curselection() 
 
    if len(tasks) == 0: 
        messagebox.showerror( 
            "Error", 
            "No tasks to delete." 
        ) 
        return 
 
    #Check whether the user has selected a task 
    if not selection: 
        messagebox.showerror( 
            "Error", 
            "Please select a task to delete." 
        ) 
        return 
 
    #Get the index of the selected task so the same position can be removed from the tasks list 
    index = selection[0] 
 
    #Remove the selected task 
    tasks.pop(index) 
    refresh_tasks() 
 
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
root.geometry("700x650") 
 
#User information frame 
setup_frame = tk.Frame( 
    root, 
    bg="light blue" 
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
    bg="light blue" 
) 
setup_title.pack(pady=70) 
 
#Name label 
name_label = tk.Label( 
    setup_frame, 
    text="Enter your name:", 
    font=("Arial", 14, "bold"), 
    bg="light blue" 
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
    bg="light blue" 
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
    width=15, 
    height=2, 
    command=check_user 
) 
continue_button.pack(pady=20) 
 
#Main menu frame 
main_frame = tk.Frame( 
    root, 
    bg="light blue" 
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
    bg="light blue" 
) 
main_title.pack(pady=70) 
 
#Button to open the add task frame 
add_task_menu_button = tk.Button( 
    main_frame, 
    text="ADD TASK", 
    font=("Arial", 14, "bold"), 
    width=20, 
    height=2, 
    command=show_add_frame 
) 
add_task_menu_button.pack(pady=10) 
 
#Button to open the tasks frame 
view_tasks_button = tk.Button( 
    main_frame, 
    text="VIEW TASKS", 
    font=("Arial", 14, "bold"), 
    width=20, 
    height=2, 
    command=show_tasks_frame 
) 
view_tasks_button.pack(pady=10) 
 
#Button to close the application 
exit_button = tk.Button( 
    main_frame, 
    text="EXIT", 
    font=("Arial", 14, "bold"), 
    width=20, 
    height=2, 
    command=exit_application 
) 
exit_button.pack(pady=10) 
 
#Add task frame 
add_frame = tk.Frame( 
    root, 
    bg="light green" 
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
    text="ADD A TASK", 
    font=("Arial", 26, "bold"), 
    bg="light green" 
) 
add_title.pack(pady=30) 
 
#Task title 
title_label = tk.Label( 
    add_frame, 
    text="Task:", 
    font=("Arial", 14, "bold"), 
    bg="light green" 
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
    text="Time allocation (minutes):", 
    font=("Arial", 14, "bold"), 
    bg="light green" 
) 
time_label.pack(pady=(10, 0)) 
 
time_entry = tk.Entry( 
    add_frame, 
    width=30, 
    font=("Arial", 14) 
) 
time_entry.pack(pady=5) 
 
#Deadline 
deadline_label = tk.Label( 
    add_frame, 
    text="Deadline (dd/mm/yyyy):", 
    font=("Arial", 14, "bold"), 
    bg="light green" 
) 
deadline_label.pack(pady=(10, 0)) 
 
deadline_entry = tk.Entry( 
    add_frame, 
    width=22, 
    font=("Arial", 14) 
) 
deadline_entry.pack(pady=5) 
 
#Button to open the calendar 
calendar_button = tk.Button( 
    add_frame, 
    text="SELECT DATE", 
    font=("Arial", 12, "bold"), 
    command=open_calendar 
) 
calendar_button.pack(pady=5) 
 
#Importance rating 
importance_label = tk.Label( 
    add_frame, 
    text="Importance:", 
    font=("Arial", 14, "bold"), 
    bg="light green" 
) 
importance_label.pack(pady=(10, 0)) 
 
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
    font=("Arial", 14), 
    width=10 
) 
 
importance_menu.pack(pady=5) 
 
#Task category 
category_label = tk.Label( 
    add_frame, 
    text="Category:", 
    font=("Arial", 14, "bold"), 
    bg="light green" 
) 
category_label.pack(pady=(10, 0)) 
 
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
    width=10 
) 
 
category_menu.pack(pady=5) 
 
#Button to add a task 
add_button = tk.Button( 
    add_frame, 
    text="ADD TASK", 
    font=("Arial", 14, "bold"), 
    width=15, 
    height=2, 
    command=add_task 
) 
add_button.pack(pady=10) 
 
#Button to return to the main menu 
back_from_add_button = tk.Button( 
    add_frame, 
    text="BACK", 
    font=("Arial", 14, "bold"), 
    width=15, 
    height=2, 
    command=show_main_frame 
) 
back_from_add_button.pack(pady=5) 
 
#Tasks frame 
tasks_frame = tk.Frame( 
    root, 
    bg="light yellow" 
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
    bg="light yellow" 
) 
tasks_title.pack(pady=30) 
 
#Task list 
task_list = tk.Listbox( 
    tasks_frame, 
    width=75, 
    height=12, 
    font=("Arial", 12) 
) 
task_list.pack(pady=15) 
 
#Button to mark a task as complete 
complete_button = tk.Button( 
    tasks_frame, 
    text="MARK COMPLETE", 
    font=("Arial", 13, "bold"), 
    width=18, 
    height=2, 
    command=complete_task 
) 
complete_button.pack(pady=5) 
 
#Button to delete a task 
delete_button = tk.Button( 
    tasks_frame, 
    text="DELETE TASK", 
    font=("Arial", 13, "bold"), 
    width=18, 
    height=2, 
    command=delete_task 
) 
delete_button.pack(pady=5) 
 
#Button to return to the main menu 
back_button = tk.Button( 
    tasks_frame, 
    text="BACK", 
    font=("Arial", 13, "bold"), 
    width=18, 
    height=2, 
    command=show_main_frame 
) 
back_button.pack(pady=15) 
 
#Show the user the information screen when the application starts 
setup_frame.tkraise() 
name_entry.focus() 
 
#The application keeps running until the window is closed 
root.mainloop()
