'''This is version 1 of my productivity application.
It uses Tkinter to provide a graphical user interface while
containing basic task management features.'''

import tkinter as tk
#messagebox to display errors in user input
from tkinter import messagebox


#Creating the Task class, a blueprint for each task object 
class Task:
    
    def __init__(self, title):#giving each task attributes:
        self.title = title
        #initially all tasks are not completed
        self.completed = False

    def mark_complete(self):
        self.completed = True

#Creating an empty list, tasks
tasks = []


#Refresh the listbox whenever tasks change
def refresh_tasks():
    task_list.delete(0, tk.END)
    #If there are no tasks currently 
    if len(tasks) == 0:
        task_list.insert(tk.END, "No tasks to view.")
    else:
     
        for i in range(len(tasks)):
            if tasks[i].completed:
                status = "✓"
            else:
                status = "✗"

            task_list.insert(tk.END, f"{i+1}. [{status}] {tasks[i].title}")


#Allow user to add new tasks
def add_task():
    title = task_entry.get()
    #If the user does not enter anything for adding a new task
    if title == "":
        messagebox.showerror("Error", "Task cannot be empty.")
    else:
        task = Task(title)
        tasks.append(task)
        task_entry.delete(0, tk.END)
        refresh_tasks()


#Let user mark a task as complete
def complete_task():
    #task that the user has last clicked (selected)
    selection = task_list.curselection()
    if len(tasks) == 0:
        messagebox.showerror("Error", "No tasks to mark as complete.")
        return
    elif not selection:
        messagebox.showerror("Error", "Please select a task to complete.")
        return

    index = selection[0]

    

    tasks[index].mark_complete()
    refresh_tasks()


    
def delete_task():
    #Find out which item the user has currently selected 
    selection = task_list.curselection()
    if len(tasks) == 0:
        messagebox.showerror("Error", "No tasks to delete.")
        return
    
    elif not selection:
        messagebox.showerror("Error", "Please select a task to delete.")
        return

    
    #deletion of a task
    
    index = selection[0]
    tasks.pop(index)
    refresh_tasks()


#GUI

#Main application window
root = tk.Tk()
root.title("Productivity App")
root.geometry("400x400")

title_label = tk.Label(root, text="Productivity App", font=("Arial", 16))
title_label.pack(pady=10)

task_entry = tk.Entry(root, width=30)
task_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=5)

task_list = tk.Listbox(root, width=40, height=10)
task_list.pack(pady=10)

complete_button = tk.Button(root, text="Mark Complete", command=complete_task)
complete_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)

refresh_tasks()

#The application keeps running until the window is closed.
root.mainloop()
