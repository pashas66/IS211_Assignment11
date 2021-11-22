#Week 11 -­ Web Development with Flask (1/2)

from flask import Flask, render_template, redirect, request
import pickle
import re
app = Flask(__name__)

class Task(): #creating a task class
    #constructor:
    def __init__ (self, task, email, priority):
        self.task = task
        self.email = email
        self.priority = priority

#This is the first route to show To Do items in a HTML table, and showing an HTML form to submit a new To Do list item.
@app.route('/')
def index():

    #here we have to use index.html in templates directory and pass it to task list and message. 
    return render_template('index.html', todo_list = todo_list, message = message)

#This is the second controller, that will accept data from the HTML form, add the To Do list item to a global list of items, and redirect back to the first controller.
@app.route('/submit', methods = ['POST'])
def submit():
    
    global message
    global todo_list
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    #this is a check to make sure if the task field is empty
    if task == '':
        message = 'Unable to Add Task - Task Field is Blank'
        return redirect("/")

    #regex pattern:
    email_reg = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

    #check to make sure if email field is empty
    if email == '':
        message = 'Unable to Add Task - Email Field is Blank'
        return redirect("/")
    
    #check to make sure that the email input is indeed an email
    elif not re.search(email_reg, email):
        message = 'Unable to Add Task - Email Format is Not Valid'
        return redirect("/")
    
    #check to make sure if priority was set
    if priority == 'Blank':
        message = 'Unable to Add Task - Priority Was Not Set'
        return redirect("/")
      
    new_task = Task(task, email, priority)
    
    #the controller should append a new To Do item to the list
    todo_list.append(new_task)
    message = ''

    # redirect to the html page
    return redirect("/")

#This is the last controller, which will be responsible for clearing the list of To Do items, and redirecting back to the first controller
@app.route('/clear', methods = ['POST'])
def clear():

    global todo_list
    global message

    #set todo list to empty list
    todo_list = []
    message = ''
    
    #redirect to html page
    return redirect("/")

#Extra Credit II -­ Delete Individual Items
#creating a route to delete individual task
@app.route('/delete', methods=['POST'])
def delete():

    global todo_list
    
    #get index value for row to delete
    index = int(request.form['index'])

    #delete object in list at that index
    del todo_list[index]
    
    #redirect to html page
    return redirect("/")

#Extra Credit I ­- Save the List:
#creating a route to save tasks to file
@app.route('/save', methods=['POST'])
def save():

    global todo_list
    global message

    #dump list to file using the pickle module  
    pickle.dump(todo_list, open('todo.p', 'wb'))

    message = 'To Do List Saved'

    #redirect to index page
    return redirect("/")


if __name__ == '__main__':
    message = ''
    try:
        todo_list = pickle.load(open('todo.p', 'rb'))
    except:
        todo_list = []
    app.run()
    #end of the code