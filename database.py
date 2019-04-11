import sqlite3
import datetime

__author__ = "Joshua Akangah"

class Database:
    def __init__(self, name='database.db'):
        self.name = name
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        # close the connection
        self.connection.close()

    def create_table(self):
        """
        creates a table in the database
        : return : Bool, error
        """
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                CREATE TABLE TASKS (ID INTEGER PRIMARY KEY, TASK TEXT NOT NULL, ENTERED TIMESTAMP NOT NULL, DUE TIMESTAMP NOT NULL, COMPLETED TEXT NOT NULL)
            """)
            self.connection.commit()
            self.connection.close()
            return True

        except sqlite3.OperationalError as error:
            # this error is returned for debugging reasons
            return error

    def insert_task(self, task, dateDue, dateEntered=datetime.datetime.today(), completed=False):
        """
        method to insert a 'task' into the database, a date is inserted along with the function parameters
        : param task: Task to be inserted into database
        : param dateDue: The date which the task will be due
        : param dateEntered: The date which the task was entered
        : param completed: Mark whether a given task has been completed, default is False
        : return : Bool, sqlite.OperationalError if otherwise
        """
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                INSERT INTO TASKS (TASK, ENTERED, DUE, COMPLETED) VALUES (?, ?, ?, ?)
            """, (task, dateEntered, dateDue, str(completed)))
            self.connection.commit()
            self.connection.close()
            # print(type(dateEntered))
            return True

        except sqlite3.OperationalError as error:
            return error

    def delete_task(self, id):
        """
        method to delete a task from the database
        : param id: ID of the task to be deleted
        : return : Bool, sqlite.OperationalError if otherwise
        """
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"DELETE FROM TASKS WHERE ID={id}")
            self.connection.commit()
            self.cursor.execute("SELECT * FROM TASKS")
            for item in self.cursor.fetchall():
                self.cursor.execute(f"UPDATE TASKS SET ID={item[0]-1} WHERE ID={item[0]} AND ID>{id}")
                self.connection.commit()
            self.connection.close()
            return True

        except sqlite3.OperationalError as error:
            return error

    def complete_task(self, id):
        """
        method to mark a task as completed in the database
        : param id: The ID of the task to mark as completed
        : return : Bool, sqlite.OPerationalError
        """
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"UPDATE TASKS SET COMPLETED='{True}' WHERE ID={id}")
            self.connection.commit()
            self.connection.close()
            return True

        except sqlite3.OperationalError as error:
            return error

    def retrieve_task(self, id):
        """
        method to retrieve a task from the database along with all its information
        : param id: ID of the task to retrieve
        : return : Tuple, sqlite.OperationalError
        """
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SELECT * FROM TASKS WHERE ID={id}")
            return self.cursor.fetchone()

        except sqlite3.OperationalError as error:
            return error

        finally:
            self.connection.close()

    def retrieve_all(self):
        """
        method to retrieve all tasks from the database
        : return : List, sqlite.OperationalError
        """
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT * FROM TASKS")
            return self.cursor.fetchall()

        except sqlite3.OperationalError as error:
            return error

        finally:
            self.connection.close()

    def delete_all(self):
        """
        method to delete all items from the database
        : return : Bool, sqlite.OperationalError
        """
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT * FROM TASKS")
            for item in self.cursor.fetchall():
                self.cursor.execute(f"DELETE FROM TASKS WHERE ID={item[0]}")
                self.connection.commit()
            self.connection.close()
            return True

        except sqlite3.OperationalError as error:
            return error
