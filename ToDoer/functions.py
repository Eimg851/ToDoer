from django.shortcuts import render
import pyrebase

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

def loadTasksFromDB(timestamps, localID):
    toDoOrder=[]
    doneOrder=[]
    for key in timestamps:
        status = database.child('users').child(localID).child('Tasks').child(key).child('status').get().val()
        if status == "done":
            doneOrder.append(key)
        else:
            toDoOrder.append(key)

    doneOrder.sort(reverse=True)
    toDoOrder.sort(reverse=True)

    #GetTask
    tasksDone = []
    tasksTodo = []
    for t in doneOrder:
        task=database.child('users').child(localID).child('Tasks').child(t).child('task').get().val()
        tasksDone.append(task)

    for t in toDoOrder:
        task=database.child('users').child(localID).child('Tasks').child(t).child('task').get().val()
        tasksTodo.append(task)


    #GetDueDay
    dueDaysTodo = []
    for t in toDoOrder:
        dueDay=database.child('users').child(localID).child('Tasks').child(t).child('dueDate').get().val()
        dueDaysTodo.append(dueDay)

    collaboratorsToDo = []
    collaboratorsDone= []
    for t in doneOrder:
        colab=database.child('users').child(localID).child('Tasks').child(t).child('collaborators').get().val()
        collaboratorsDone.append(colab)

    for t in toDoOrder:
        colab=database.child('users').child(localID).child('Tasks').child(t).child('collaborators').get().val()
        collaboratorsToDo.append(colab)

    #combine database lists
    comb_toDoList = zip(toDoOrder,dueDaysTodo,tasksTodo, collaboratorsToDo)
    comb_DoneList = zip(doneOrder,tasksDone, collaboratorsDone)
    return comb_toDoList, comb_DoneList



