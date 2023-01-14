# Password Manager
#### Video Demo:  <https://youtu.be/o0jz5F0D0ew>
#### Description:
##### This is a final project for CS50x course
I decided to do a password manager web app using simple cryptography, SQLite, Flask, FlaskSQLAlchemy library, and other libraries I found online to solve my problems as well as simple javascript and bootstrap framework.
### The first and most important file is the **app.py**, it handles the basic logic of the web app
Here i decided to use Flask SQL-Alchemy library to turn SQLite tables into objects and to provide myself some functionality for encryption. I had to learn about classes in Python.
First of all, i built this app on a carcass of the app i made for Finance problem set.
I found Fernet library for Python to encrypt and decrypt certain items, because I didn't want to store these passwords as plain text and
after some googling I found out about SQL-Alchemy-utils library, which uses fernet encryption logic for easy encryption and decryption of certain database columns.
Each password item contains title, optional link to the website this password associated with, password itself and optional description.
If user provides a link, it is being validated using small validation library for python to prevent it from being incorrect format. That allows me to guarantee that link is going to be clickable, when password item will be rendered with jinja template.

Each password has the **Edit** and **Delete** buttons. Delete is self explanatory, but it is deleting that password id via **POST** request. Edit renders template associated with that password using **GET**. I implemented a small check that if current user tries to access password that is not associated with his acccount, he will encounter 403 Forbidden code.

**Change password** button on a navbar simply changes account master password via updating the database.
### **crypto.py** contains two functions I *found online*
One generates key and writes it to a file in that directory. The second one loads that key from a file, so it is not stored as plaintext in app.py. Then the KEY is used for encrypting and decrypting the database
### **helpers.py** is from Finance problem set on CS50
Apology for rendering error messages if something goes wrong
### Templates are just templates.
Those contain Jinja templating
### On static I implemented simple js code and css styling
Javascript language allowed me to hide passwords when mouse is not pointing at them, and show it when it does. I also added a button to copy password to the clipboard.
The search bar on the index page is making AJAX requests to the /search route, then on the server side app renders a template for that search query.
**form.js** just handles the logic for show/hide password checkbox and for generating a password using a cycle , **index.js** handles the logic for search and delete/edit buttons via cycle so it is applied for all password items.
