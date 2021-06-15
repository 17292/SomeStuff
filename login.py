from flask import Flask,g, render_template, request, redirect  
import sqlite3

app = Flask(__name__)

DATEBASE = "blog.db"

user = {}
status = ""

def displayMenu():
    status = input("Are you registered? y/n? Press q to quit")
    if status == "y":
        olderUser()
    elif status == "n":
        newUser()

def newUser():
    createLogin = input("Create login name: ")

    if createLogin in user:
        print("/n Login name already exist! /n")
    else:
        createPassw = input("Create password: ")
        user[createLogin] = createPassw
        print ("\n User created \n")

def olderUser():
    login = input("Enter login name: ")
    passw = input("Enter password: ")
    if login in user and user[login] == passw:
        print("\n Login sucessful! \n")
    else: 
        print("\n User doesn't exist or wrong password! \n")

while status != "q":
    displayMenu()

