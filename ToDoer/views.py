from django.shortcuts import render
import pyrebase
import requests
from django.http import HttpResponse
from django.contrib import auth
import datetime
from .functions import *

config = {
    'apiKey': "AIzaSyBd7w652gzVMK2HCgM7GbS2pIYpiHypfJo",
    'authDomain': "todolist-comp41110.firebaseapp.com",
    'databaseURL': "https://todolist-comp41110.firebaseio.com",
    'projectId': "todolist-comp41110",
    'storageBucket': "todolist-comp41110.appspot.com",
    'messagingSenderId': "723004569445"
  }
firebase = pyrebase.initialize_app(config)
FirebaseAuth = firebase.auth()
database=firebase.database()

def index(request):
    """
    Returns index page when app is started
    :param request:
    :return:
    """
    return render(request, 'ToDoer/index.html')

def postLogin(request):
    """
    takes parameters on login, send to firebase authentication and returns the homepage fo the user
    :param request:
    :return:
    """
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
        user = FirebaseAuth.sign_in_with_email_and_password(email, password)
    except:
        message="Invalid email or password"
        return render(request, 'ToDoer/index.html', {"message":message})

    session_id=user['idToken']
    request.session['uid']=str(session_id)
    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)

    localID = session_token['users'][0]['localId']
    username= database.child('users').child(localID).child('details').child('Firstname').get().val()
    surname= database.child('users').child(localID).child('details').child('Surname').get().val()
    email= database.child('users').child(localID).child('details').child('email').get().val()
    timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()

    if timestamps != None:
        comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
        return render(request, 'ToDoer/welcome.html', {"username":username, "todo_list":comb_toDoList, "done_list":comb_doneList, "uid":localID, "surname":surname, "email":email})

    else:
        return render(request, 'ToDoer/welcome.html', {"username":username, "uid":localID, "surname":surname, "email":email})

def logout(request):
    """
    Logs the user out
    :param request:
    :return:
    """
    auth.logout(request)
    return render(request, "ToDoer/index.html")

def signUp(request):
    """
    Brings the user to the signUp page
    :param request:
    :return:
    """
    return render(request, "ToDoer/createAccount.html")

def postSignUp(request):
    """
    Takes data entered on sign up, creates an account and brings the user back to the sign in page
    :param request:
    :return:
    """
    fname=request.POST.get("firstname")
    sname=request.POST.get("surname")
    email=request.POST.get("email")
    password=request.POST.get("password")
    print(fname,sname,email,password)
    try:
        user=FirebaseAuth.create_user_with_email_and_password(email, password)
    except:
        message="Unable to create account. Please try again"
        return render(request, "ToDoer/createAccount.html", {"message":message})
    uid=user["localId"]
    print(uid)

    data={"Firstname":fname, "Surname":sname, "status":"1", "email":email}
    print(data)
    database.child("users").child(uid).child("details").set(data)
    return render(request, "ToDoer/index.html")

def postAddTask(request):
    """
    Takes the name of the task and its due date and adds the task to the list in the firebase cloud
    Returns an updated list of tasks
    :param request:
    :return:
    """
    import time
    millis = int(round(time.time() * 1000))
    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)
    localID = session_token['users'][0]['localId']

    task=request.POST.get("task")
    dueDate=request.POST.get("due")
    data={
        "task":task,
        "dueDate":dueDate,
        "status":"todo",
        "collaborators":"None"
    }
    database.child('users').child(localID).child("Tasks").child(millis).set(data)

    username= database.child('users').child(localID).child('details').child('Firstname').get().val()
    timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
    comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
    return render(request, 'ToDoer/welcome.html', {"username":username, "todo_list":comb_toDoList, "done_list":comb_doneList})

def deleteTask(request):
    """
    Removes tasks from the database and returns an updated list of tasks
    :param request:
    :return:
    """
    timestamp=request.POST.get("timestamp")

    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)
    localID = session_token['users'][0]['localId']

    database.child('users').child(localID).child("Tasks").child(timestamp).remove()

    timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
    comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
    return render(request, 'ToDoer/updatingTasks.html', {"todo_list":comb_toDoList, "done_list":comb_doneList})

def markAsDone(request):
    """
    Marks a task as done, and returns an updated list of tasks
    :param request:
    :return:
    """
    timestamp=request.POST.get("timestamp")
    status=request.POST.get("status")

    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)
    localID = session_token['users'][0]['localId']
    currentData= database.child('users').child(localID).child('Tasks').child(timestamp).shallow().get().val()
    print(currentData)
    currentVals=[]
    for val in currentData:
        task=database.child('users').child(localID).child('Tasks').child(timestamp).child(val).get().val()
        currentVals.append(task)
    print(currentData)
    print(currentVals)
    database.child('users').child(localID).child("Tasks").child(timestamp).update({"task":currentVals[2], "dueDate":currentVals[0] , "status":status})

    timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
    comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
    return render(request, 'ToDoer/updatingTasks.html', {"todo_list":comb_toDoList, "done_list":comb_doneList})

def editTask(request):
    """
    edits a given task and returns an updated list of tasks
    :param request:
    :return:
    """
    timestamp=request.POST.get("timestamp")
    task=request.POST.get("task")
    dueDate=request.POST.get("due")

    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)
    localID = session_token['users'][0]['localId']


    database.child('users').child(localID).child("Tasks").child(timestamp).update({"task":task, "dueDate":dueDate , "status":"todo"})


    timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
    comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
    return render(request, 'ToDoer/updatingTasks.html', {"todo_list":comb_toDoList, "done_list":comb_doneList})

def search(request):
    """
    Allows user to search for tasks in the database
    :param request:
    :return:
    """
    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)
    localID = session_token['users'][0]['localId']
    username= database.child('users').child(localID).child('details').child('Firstname').get().val()
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        search = search.lower()
        timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
        tasks_id=[]
        for t in timestamps:
            task_name = database.child('users').child(localID).child("Tasks").child(t).child('task').get().val()
            task_name = str(task_name)+"$"+str(t)
            tasks_id.append(task_name)
        tasks_id = [str(string) for string in tasks_id if search in string.lower()]
        print(tasks_id)
        matching_tasks=[]
        for i in tasks_id:
            work,ids=i.split('$')
            matching_tasks.append(ids)
        comb_toDoList, comb_doneList = loadTasksFromDB(matching_tasks, localID)
        return render(request, 'ToDoer/welcome.html', {"username":username, "todo_list":comb_toDoList, "done_list":comb_doneList})
    else:
        timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
        comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
        return render(request, 'ToDoer/welcome.html', {"username":username, "todo_list":comb_toDoList, "done_list":comb_doneList})

def clearSearch(request):
    """
    Clears the search item
    :param request:
    :return:
    """
    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)
    localID = session_token['users'][0]['localId']
    username= database.child('users').child(localID).child('details').child('Firstname').get().val()
    timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
    comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
    return render(request, 'ToDoer/welcome.html', {"username":username, "todo_list":comb_toDoList, "done_list":comb_doneList})

def shareTask(request):
    """
    Allows user to share a single task with another user
    :param request:
    :return:
    """
    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)
    localID = session_token['users'][0]['localId']

    timestamp=request.POST.get("timestamp")
    task=request.POST.get("task")
    dueDate=request.POST.get("due")
    status= database.child('users').child(localID).child('Tasks').child(timestamp).child('status').get().val();
    recipient=request.POST.get("recipient")

    users=database.child('users').shallow().get().val()
    user_emails=[]
    for user in users:
        email = database.child('users').child(user).child("details").child("email").get().val()
        email = str(email)+"$"+str(user)
        user_emails.append(email)
    tasks_id = [str(string) for string in user_emails if recipient in string.lower()]
    if len(tasks_id) != 0:
        email,userID=tasks_id[0].split('$')

        data={
            "task":task,
            "dueDate":dueDate,
            "status":status,
        }
        database.child('users').child(userID).child("Tasks").child(timestamp).set(data)

        timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
        comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
        return render(request, 'ToDoer/updatingTasks.html', {"todo_list":comb_toDoList, "done_list":comb_doneList})
    else:
        timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
        comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
        return render(request, 'ToDoer/updatingTasks.html', {"todo_list":comb_toDoList, "done_list":comb_doneList, "message":"User with address "+recipient+" does not exist. Please check and try again."})

def shareEntireList(request):
    """
    Allows user to share the entire to do list with another user
    :param request:
    :return:
    """
    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)
    localID = session_token['users'][0]['localId']
    timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()

    recipient=request.POST.get("recipient")
    users=database.child('users').shallow().get().val()
    user_emails=[]
    for user in users:
        email = database.child('users').child(user).child("details").child("email").get().val()
        email = str(email)+"$"+str(user)
        user_emails.append(email)
    tasks_id = [str(string) for string in user_emails if recipient in string.lower()]
    if len(tasks_id) != 0:
        email,userID=tasks_id[0].split('$')


        for key in timestamps:
            status = database.child('users').child(localID).child('Tasks').child(key).child('status').get().val()
            task = database.child('users').child(localID).child('Tasks').child(key).child('task').get().val()
            dueDate = database.child('users').child(localID).child('Tasks').child(key).child('dueDate').get().val()

            data={
                "task":task,
                "dueDate":dueDate,
                "status":status,
            }
            database.child('users').child(userID).child("Tasks").child(key).set(data)


        timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
        comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
        return render(request, 'ToDoer/updatingTasks.html', {"todo_list":comb_toDoList, "done_list":comb_doneList})
    else:
        timestamps = database.child('users').child(localID).child('Tasks').shallow().get().val()
        comb_toDoList, comb_doneList = loadTasksFromDB(timestamps, localID)
        return render(request, 'ToDoer/updatingTasks.html', {"todo_list":comb_toDoList, "done_list":comb_doneList, "message":"User with address "+recipient+" does not exist. Please check and try again."})

def settings(request):
    """
    Allows user to edit their name and email address in the database
    :param request:
    :return:
    """
    id_token=request.session['uid']
    session_token = FirebaseAuth.get_account_info(id_token)
    localID = session_token['users'][0]['localId']

    fname=request.POST.get("fname")
    sname=request.POST.get("sname")
    email=request.POST.get("email")
    print(fname, sname, email)

    data={"Firstname":fname, "Surname":sname, "status":"1", "email":email}
    database.child("users").child(localID).child("details").set(data)
    return render(request, 'ToDoer/settings.html', {"surname":sname, "email":email, "username":fname})

