__author__ = "Joshua Akangah"

from database import *
import guizero

# creating an app and creating an instamce of the database class
app = guizero.App(title="ToDo", width=400, height=600)
database = Database("todo.sqlite")

# creating a table in the database, if a table already exists, we will get an sqlite Operational Error
# but will not halt the program
database.create_table()

# main function of the GUI
def refreshScreen():
    """
    function to re-draw items from the database to the listbox
    : return : None
    """
    task.clear()
    for item in database.retrieve_all():
        comp = ['Completed' if item[4] == 'True' else 'Pending']
        txt = guizero.Text(task, text=f"{item[0]}. {item[1]}            {comp[0]}")
        task.insert('end', txt.value)

def main():
    # making entertask a global variable so we can access its value from any method
    global enterTask
    global box

    enterTask = guizero.TextBox(app, text="Enter a Task", width=50)

    guizero.Text(app, text=" ")
    guizero.PushButton(app, command=addTask, text="Add Task")

    showAll()

    # drawing elements in the bottom of the screen
    # creating a box object to align to the bottom of the screen
    box = guizero.Box(app, width="fill", align="bottom")
    guizero.PushButton(box, text="Delete All", align="right", command=deleteAll)
    guizero.PushButton(box, text="Delete Selected", align="right", command=removeTask)
    guizero.PushButton(box, text="Complete task", align="left", command=completeTask)

def getValue(item):
    """
    function to return the value of the textbox
    :return : string
    """
    return item.value

def getList(item):
    """
    function to return the id of an object in the listbox
    : return : string
    """
    try:
        return item.value[0]
    except TypeError:
        pass

def completeTask():
    """
    function to mark a task as completed in the database
    : return : None
    """
    if getList(task) != None:
        if database.retrieve_task(getList(task))[4] == 'True':
            print(getList(task))
            # if task is already completed, implement a warning
            if guizero.yesno("Illegal action", "Task is already completed, Do you want to remove it instead?"):
                database.delete_task(getList(task))
                refreshScreen()
        else:
            print(getList(task))
            if database.complete_task(getList(task)):
                refreshScreen()
            else:
                # if there was a database error, raise a warning
                guizero.warn("Error", "Error completing task")
    else:
        # if no task has been selected
        guizero.warn("Task", "Select a task first")

def removeTask():
    """
    Function to remove a task from the listbox and the database
    : return None
    """
    if getList(task) == None:
        # if a task has not been selected
        guizero.warn("Illegal action", "Select a task first")
    else:
        if database.delete_task(getList(task)):
            refreshScreen()
        else:
            guizero.warn("Error", "Error removing task")

def addTask():
    """
    Function to add a task to the database
    : return: None
    """
    if getValue(enterTask) == '':
        guizero.warn("Illegal action", "Enter a task first")
    else:
        if database.insert_task(getValue(enterTask), datetime.datetime.now()):
            refreshScreen()
        else:
            guizero.warn("Error", "Could not add Task")
        
        

def showAll():
    """
    Function to display all tasks in the database to the GUI
    : return: None
    """
    global task
    # making task a global variable so it can be accessed from all methods throughout the code

    guizero.Text(app, text='')
    task = guizero.ListBox(app, scrollbar=True, width=750, height=450)

    for item in database.retrieve_all():
        comp = ['Completed' if item[4] == 'True' else 'Pending']
        txt = guizero.Text(task, text=f"{item[0]}. {item[1]}            {comp[0]}")
        task.insert('end', txt.value)

def deleteAll():
    """
    Function to delete all items from the database and listbox
    : return : None
    """
    if database.delete_all():
        task.clear()
    else:
        guizero.warn("Error", "Could not delete all tasks from database")

def sureQuit():
    """
    Function to confirm if user wants to quit
    """
    if guizero.yesno("Quit", "Do you want to exit?"):
        app.destroy()

if __name__ == "__main__":
    main()
    app.on_close(sureQuit)
    app.display()
