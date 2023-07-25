# Gamestore
#### Video Demo:  https://youtu.be/D1fSQ4jb07I
#### Description:
I have made a Gamestore web application which lets registered users buy and sell items stored
inside their gaming account. The application catalogues the items into different types and presents
an interface for user to interact.

project.db is the database file used for this application as it stores multiple tables which contains
information about various functions which we will discuss further. The database contains the table:-
users,objects,bank and cart which contain information.

users table contain data about all the players of the game along with their id,password,username,
real life money present in account and in game currency gold in account. Each id is unique in nature
and registration is compulsory to gain access to features of this application.

objects table contain the data associated with the objects present in the game. The table contains the
headers:- id,objectID,name,rating,price,priceG,listing where id is the user id of the owner of the object,
objectID is the unique ID associated with the object,name is the name of the object,rating is the game's
official way of showing how rare the item is, price is the owner's registered price in USD for the object
and priceG is the owner's registered price in Gold for the object. Listing decides whether the object is
up for sale or not.

cart table contains the attributes id,objectID,price,priceg,b_id where id is the object owner's id,objectID
is the unique id associated with the object,price and priceG are the cost of weapons in USD and Gold
respectively and b_id is the buyer's user id. The cart table contains all the objects selected by user
to purchase.

bank table is a table associated with transfer of USD from a bank to users account. Every purchase in the
application only exhausts the money present in users. Whereas money in bank is only withdrawn when the user
desires to increase his monetary reserves in his account.

app.py is the file which contains all the backend logic to be used for the application. The python file uses
cs50 library, flask library and other libraries to provide logic to the runnig of the Gamestore web application. The app.py file recieves and applies several functions to cater all the needs in the web
application while using flask and SQL.

input.sql is the file used to test all the commands required in SQL from table creation to updating all the
tables in the database.

requirements.txt contains several lines which help is starting a flask session.

flask_session is a folder used to store sessions while using the web applications.

static folder contains the styles.css which provides style components for our webpage.

templates folder contains all the html files used in our web application.

layout.html is the main layout page and home.html is the homepage for our web application. It displays the types of items present in the game as well as several nav options to choose. An unregistered user can only see register and login which is mandatory for the user to view other parts of the application. If the user is logged in then the nav menu contains several options which are cart,sell,add funds,balance and forgot password.

Every option leads the user to a page extended by layout which shows us a table full of items which have been
listed by the their owners for sale. The table contains their name,rating and price in USD and Gold along with a cart button which upon click carts the item for purchase and sets button to carted. This is implemented by using AJAX which sends data back to app.py for inclusion in cart.html. sword.html is the main
html page which is extended by rest of the options excluding gold. Each object has a specific pattern regarding their objectID which helps the application recognise which item belongs to which category.

gold.html leads to a page which lets the user transfer their accounts USD to gold in thier account. 1 USD is
equal to 2000 Gold and the logic is sufficiently handled by the app.py.

register.html and login.html extends layout.html to provide textboxes and buttons to register and log users inside the web application.

changepassword.html provides a logged in user to change their password provided that he/she remember their current password.

sell.html contains 2 drop down boxes along with two buttons which list and delists items from the catalogue of items to be sold. The boxes contain the items listed and delisted respectivelt and the text boxes enable the user to set a price in USD and GOld for the item being listed for sale.

cart.html lets the user see which item they are going to buy and adds up the total bill required to be paid by the user. This page handles the transfer of funds from one user to another and also changes the ownership of the object from one user to another. The page can also uncart items and changes in the cart can be seen through the help of the reload button.

All the possible error and exceptions are handled by app.py and the execution of sql commands during runtime of the web application is done by the app.py. The web application can be implemented by usinf flask run on bash after downloading the whole project folder.

