import os
import requests
import random
from functools import wraps
from cs50 import *
from flask import *
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")


def login_required(f):
    "to determine if login is required or not"
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():

    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        x = request.form.get("username")
        y = request.form.get("password")
        if not x:
            return render_template("login.html", prompt=1, Error="Blank Username")
        elif not y:
            return render_template("login.html", prompt=1, Error="Blank Password")

        user = db.execute(
            "SELECT * from users where username = ? and password = ?", x, y)
        if len(user) != 1:
            return render_template("login.html", prompt=1, Error="Username not present or Password doesnot match")
        session["user_id"] = user[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html", prompt=0)


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():

    session.clear()
    if request.method == "POST":
        x = request.form.get("username")
        y = request.form.get("password")
        z = request.form.get("confirmation")
        if not x:
            return render_template("register.html", prompt=2, Error="Blank Username")
        elif not y:
            return render_template("register.html", prompt=2, Error="Blank Password")
        elif not z:
            return render_template("register.html", prompt=2, Error="Blank Confirmation")
        elif y != z:
            return render_template("register.html", prompt=2, Error="Passwords must match")

        check = db.execute("SELECT * from users where username=?", x)
        if len(check) != 0:
            return render_template("register.html", prompt=2, Error="Username taken")
        id = random.randint(100000, 999999)
        db.execute(
            "INSERT INTO users(id,username,password,cash,cashG) VALUES(?,?,?,?,?)", id, x, y, 0, 0)
        session["user_id"] = id
        return redirect("/")
    else:
        return render_template("register.html", prompt=0)


@app.route("/sword")
@login_required
def sword():

    x = db.execute(
        "SELECT * from objects where CAST(objectID AS VARCHAR) LIKE '1_____' and listing='l' ")
    return render_template("sword.html", x=x)


@app.route("/axe")
@login_required
def axe():

    x = db.execute(
        "SELECT * from objects where CAST(objectID AS VARCHAR) LIKE '3_____' and listing='l' ")
    return render_template("axe.html", x=x)


@app.route("/shield")
@login_required
def shield():

    x = db.execute(
        "SELECT * from objects where CAST(objectID AS VARCHAR) LIKE '2_____'  and listing='l' ")
    return render_template("shield.html", x=x)


@app.route("/scythe")
@login_required
def scythe():

    x = db.execute(
        "SELECT * from objects where CAST(objectID AS VARCHAR) LIKE '4_____' and listing='l'  ")
    return render_template("scythe.html", x=x)


@app.route("/pickaxe")
@login_required
def pickaxe():

    x = db.execute(
        "SELECT * from objects where CAST(objectID AS VARCHAR) LIKE '5_____'  and listing='l' ")
    return render_template("pickaxe.html", x=x)


@app.route("/spear")
@login_required
def spear():

    x = db.execute(
        "SELECT * from objects where CAST(objectID AS VARCHAR) LIKE '6_____'  and listing='l' ")
    return render_template("spear.html", x=x)


@app.route("/potions")
@login_required
def potions():

    x = db.execute(
        "SELECT * from objects where CAST(objectID AS VARCHAR) LIKE '7_____'  and listing='l' ")
    return render_template("potions.html", x=x)


@app.route("/books")
@login_required
def books():

    x = db.execute(
        "SELECT * from objects where CAST(objectID AS VARCHAR) LIKE '8_____'  and listing='l' ")
    return render_template("books.html", x=x)


@app.route("/ingredients")
@login_required
def ingredients():

    x = db.execute(
        "SELECT * from objects where CAST(objectID AS VARCHAR) LIKE '9_____'  and listing='l' ")
    return render_template("ingredients.html", x=x)


@app.route("/gold", methods=["POST", "GET"])
@login_required
def gold():
    if request.method == "POST":
        x = request.form.get("gold")
        x = int(float(x))
        cash = db.execute("Select cash from users where id = ?",
                      session["user_id"])
        cash = cash[0]["cash"]
        cash = int(float(cash))
        if x > cash:
            return render_template("gold.html", cash=cash, prompt=1, Error="Invalid Amount")
        cash = cash-x
        db.execute("update users set cash = ? where id = ?",
               cash, session["user_id"])
        x = x*2000
        db.execute("update users set cashG = ? where id = ?",
               x, session["user_id"])
        return render_template("gold.html",cash=cash)
    else:
        cash = db.execute("Select cash from users where id = ?",
                      session["user_id"])
        cash = cash[0]["cash"]
        return render_template("gold.html",cash=cash)



@app.route('/store', methods=['POST'])
@login_required
def store():
    data = request.get_json()
    a = data.get('id')
    b = data.get('objectId')
    c = data.get('price')
    d = data.get('priceg')
    id = session["user_id"]
    a = int(float(a))
    id = int(float(id))
    if a == id:
        return redirect("/")
    x = db.execute(
        "SELECT * from cart where id=? and objectID=? and b_id=?", a, b, id)
    if len(x) != 0:
        return redirect("/")

    db.execute(
        "Insert into cart(id,objectID,price,priceg,b_id) values(?,?,?,?,?)", a, b, c, d, id)
    return jsonify({'message': 'Item added to cart'})


@app.route('/buy', methods=["POST", "GET"])
@login_required
def buy():

    if request.method == "POST":
        a = request.form.get("username")
        b = request.form.get("password")
        c = request.form.get("confirmation")
        d = request.form.get("amount")
        if not a:
            return render_template("buy.html", prompt=1, Error="Blank name")

        if not b:
            return render_template("buy.html", prompt=1, Error="Blank password")

        if not c:
            return render_template("buy.html", prompt=1, Error="Blank confirmation")

        if not d:
            return render_template("buy.html", prompt=1, Error="Blank amount")

        if b != c:
            return render_template("buy.html", prompt=1, Error="Not matching")

        z = db.execute(
            "select * from bank where bank_username = ? and bank_pswd = ?", a, b)
        if len(z) == 0:
            return render_template("buy.html", prompt=1, Error="Doesnot exist")

        cash1 = db.execute(
            "Select * from users where id = ?", session["user_id"])
        cash1 = cash1[0]["cash"]
        cash1 = float(cash1)
        cash2 = z[0]["bank_cash"]
        cash2 = float(cash2)
        d = float(d)
        if d > cash2:
            return render_template("buy.html", prompt=1, Error="Not enough funds")
        cash1 = cash1 + d
        cash2 = cash2 - d
        cash1 = int(cash1)
        cash2 = int(cash2)
        z = z[0]["bank_id"]
        db.execute("Update users set cash = ? where id = ?",
                   cash1, session["user_id"])
        db.execute("Update bank set bank_cash = ? where bank_id=?", cash2, z)
        return redirect("/")

    else:
        return render_template("buy.html", prompt=0)


@app.route('/uncart', methods=["POST", "GET"])
@login_required
def uncart():
    if request.method == "POST":
        data = request.get_json()
        a = data.get('id')
        b = data.get('objectId')
        c = data.get('price')
        d = data.get('priceg')
        x = db.execute(
            "delete from cart where id =? and objectID=? and b_id=?", a, b, session["user_id"])
        x = db.execute(
        "select c.id,c.objectID,o.name,c.price,c.priceg,o.rating from objects as o , cart as c where c.id=o.id and c.objectID=o.objectID and c.b_id=?", session["user_id"])
        cash = db.execute(
        "select sum(price) from cart where b_id=?", session["user_id"])
        cashg = db.execute(
        "select sum(priceG) from cart where b_id=?", session["user_id"])
        cash = cash[0]["sum(price)"]
        cashg = cashg[0]["sum(priceG)"]
        return render_template("cart.html", x=x, cash=cash, cashg=cashg,prompt=2,Error="Press Reload to see changes")

    else:
        x = db.execute(
        "select c.id,c.objectID,o.name,c.price,c.priceg,o.rating from objects as o , cart as c where c.id=o.id and c.objectID=o.objectID and c.b_id=?", session["user_id"])
        cash = db.execute(
        "select sum(price) from cart where b_id=?", session["user_id"])
        cashg = db.execute(
        "select sum(priceG) from cart where b_id=?", session["user_id"])
        cash = cash[0]["sum(price)"]
        cashg = cashg[0]["sum(priceG)"]
        return render_template("cart.html", x=x, cash=cash, cashg=cashg)

@app.route('/cart')
@login_required
def cart():
    x = db.execute(
        "select c.id,c.objectID,o.name,c.price,c.priceg,o.rating from objects as o , cart as c where c.id=o.id and c.objectID=o.objectID and c.b_id=?", session["user_id"])
    cash = db.execute(
        "select sum(price) from cart where b_id=?", session["user_id"])
    cashg = db.execute(
        "select sum(priceG) from cart where b_id=?", session["user_id"])
    cash = cash[0]["sum(price)"]
    cashg = cashg[0]["sum(priceG)"]
    return render_template("cart.html", x=x, cash=cash, cashg=cashg)


@app.route('/ccheckout', methods=["POST", "GET"])
@login_required
def ccheckout():
    if request.method == "POST":
        id = session["user_id"]
        total = db.execute("Select sum(price) from cart where b_id=?", id)
        total = total[0]["sum(price)"]
        cash = db.execute("Select cash from users where id=?", id)
        cash = cash[0]["cash"]
        if total==None:
            x = db.execute(
                "select c.id,c.objectID,o.name,c.price,c.priceg,o.rating from objects as o , cart as c where c.id=o.id and c.objectID=o.objectID and c.b_id=?", session["user_id"])
            cash = db.execute("select sum(price) from cart where b_id=?", id)
            cashg = db.execute("select sum(priceG) from cart where b_id=?", id)
            cash = cash[0]["sum(price)"]
            cashg = cashg[0]["sum(priceG)"]
            return render_template("cart.html", x=x, cash=cash, cashg=cashg, prompt=1, Error="Empty Cart")
        total = int(float(total))
        cash = int(float(cash))
        if total>cash:
            x = db.execute(
                "select c.id,c.objectID,o.name,c.price,c.priceg,o.rating from objects as o , cart as c where c.id=o.id and c.objectID=o.objectID and c.b_id=?", session["user_id"])
            cash = db.execute("select sum(price) from cart where b_id=?", id)
            cashg = db.execute("select sum(priceG) from cart where b_id=?", id)
            cash = cash[0]["sum(price)"]
            cashg = cashg[0]["sum(priceG)"]
            return render_template("cart.html", x=x, cash=cash, cashg=cashg, prompt=1, Error="Insufficient funds")
        cash = cash - total
        db.execute("Update users set cash=? where id=?", cash, id)
        x = db.execute("Select objectID from cart where b_id=?", id)
        for i in x:
            t = i["objectID"]
            t = int(float(t))
            db.execute(
                "update objects set id = ?,listing = 'r' where objectID = ?", id, t)
        amount = db.execute(
            "Select cash from users where id = (Select id from cart where b_id=?)", id)
        amount = amount[0]["cash"]
        amount = int(float(amount))
        amount = amount + total
        db.execute(
            "Update users set cash = ? where id=(Select id from cart where b_id=?)", amount, id)
        db.execute("Delete from cart")
        return redirect("/balance")
    else:

        return redirect("/balance")


@app.route('/gcheckout',methods=["POST","GET"])
@login_required
def gcheckout():
    if request.method == "POST":
        id = session["user_id"]
        total = db.execute("Select sum(priceg) from cart where b_id=?", id)
        total = total[0]["sum(priceg)"]
        cash = db.execute("Select cashG from users where id=?", id)
        cash = cash[0]["cashG"]
        if total==None:
            x = db.execute(
                "select c.id,c.objectID,o.name,c.price,c.priceg,o.rating from objects as o , cart as c where c.id=o.id and c.objectID=o.objectID and c.b_id=?", session["user_id"])
            cash = db.execute("select sum(price) from cart where b_id=?", id)
            cashg = db.execute("select sum(priceG) from cart where b_id=?", id)
            cash = cash[0]["sum(price)"]
            cashg = cashg[0]["sum(priceG)"]
            return render_template("cart.html", x=x, cash=cash, cashg=cashg, prompt=1, Error="Empty Cart")
        total = int(float(total))
        cash = int(float(cash))
        if total>cash:
            x = db.execute(
                "select c.id,c.objectID,o.name,c.price,c.priceg,o.rating from objects as o , cart as c where c.id=o.id and c.objectID=o.objectID and c.b_id=?", session["user_id"])
            cash = db.execute("select sum(price) from cart where b_id=?", id)
            cashg = db.execute("select sum(priceG) from cart where b_id=?", id)
            cash = cash[0]["sum(price)"]
            cashg = cashg[0]["sum(priceG)"]
            return render_template("cart.html", x=x, cash=cash, cashg=cashg, prompt=1, Error="Insufficient Gold")
        cash = cash - total
        db.execute("Update users set cashG=? where id=?", cash, id)
        x = db.execute("Select objectID from cart where b_id=?", id)
        for i in x:
            t = i["objectID"]
            t = int(float(t))
            db.execute(
                "update objects set id = ?,listing = 'r' where objectID = ?", id, t)
        amount = db.execute(
            "Select cashG from users where id = (Select id from cart where b_id=?)", id)
        amount = amount[0]["cashG"]
        amount = int(float(amount))
        amount = amount + total
        db.execute(
            "Update users set cashG = ? where id=(Select id from cart where b_id=?)", amount, id)
        db.execute("Delete from cart")
        return redirect("/balance")
    else:

        return redirect("/balance")


@app.route('/changepassword', methods=["POST", "GET"])
@login_required
def changepassword():
    if request.method == "POST":
        x = request.form.get("username")
        y = request.form.get("password")
        z = request.form.get("confirmation")
        pswd = db.execute(
            "select password from users where id=?", session["user_id"])
        pswd = pswd[0]["password"]
        if x != pswd:
            return render_template("changepassword.html", prompt=1, Error="Password not matching")
        if not x:
            return render_template("changepassword.html", prompt=1, Error="No Current Password")
        if not y:
            return render_template("changepassword.html", prompt=1, Error="No New Password")
        if not z:
            return render_template("changepassword.html", prompt=1, Error="No New Password Confirmation")
        if y != z:
            return render_template("changepassword.html", prompt=1, Error="New Password not matching")
        if x == y:
            return render_template("changepassword.html", prompt=1, Error="Old and New Passwords matching")

        db.execute("update users set password=? where id = ?",
                   y, session["user_id"])
        return redirect("/")

    else:
        return render_template("changepassword.html")


@app.route('/balance')
@login_required
def balance():
    cash = db.execute("select cash from users where id = ?",
                      session["user_id"])
    cashG = db.execute(
        "select cashG from users where id = ?", session["user_id"])
    cash = cash[0]["cash"]
    cashG = cashG[0]["cashG"]
    return render_template("balance.html", cash=cash, cashG=cashG)


@app.route('/sell', methods=["POST", "GET"])
@login_required
def sell():
    if request.method == "POST":
        a = request.form.get("cash")
        b = request.form.get("gold")
        c = request.form.get("item")
        if not a:
            x = db.execute(
                "select * from objects where id = ? and listing = 'r'", session["user_id"])
            y = db.execute(
            "select * from objects where id = ? and listing = 'l'",session["user_id"])
            return render_template("sell.html", x=x,y=y, prompt=1, Error="Blank Cash")
        if not b:
            x = db.execute(
                "select * from objects where id = ? and listing = 'r'", session["user_id"])
            y = db.execute(
            "select * from objects where id = ? and listing = 'l'",session["user_id"])

            return render_template("sell.html", x=x,y=y, prompt=1, Error="Blank Gold")
        if not c:
            x = db.execute(
                "select * from objects where id = ? and listing = 'r'", session["user_id"])
            y = db.execute(
                "select * from objects where id = ? and listing = 'l'",session["user_id"])

            return render_template("sell.html", x=x,y=y, prompt=1, Error="Blank item")

        a = int(float(a))
        b = int(float(b))
        db.execute("update objects set price=?,priceG=?,listing='l' where id=? and name=?",
                   a, b, session["user_id"], c)
        return redirect("/")
    else:
        x = db.execute(
            "select * from objects where id = ? and listing = 'r'", session["user_id"])
        y = db.execute(
            "select * from objects where id = ? and listing = 'l'",session["user_id"])

        return render_template("sell.html", x=x,y=y)

@app.route('/unlist', methods=["POST", "GET"])
@login_required
def unlist():
    if request.method == "POST":
        a = request.form.get("itema")
        if not a:
             x = db.execute(
            "select * from objects where id = ? and listing = 'r'", session["user_id"])
             y = db.execute(
            "select * from objects where id = ? and listing = 'l'",session["user_id"])

             return render_template("sell.html", x=x,y=y,prompt=1,Error="Blank item")
        db.execute("update objects set listing = 'r' where id = ? and listing = 'l' and name = ?",session["user_id"],a)
        return redirect("/sell")


    else:
        x = db.execute(
            "select * from objects where id = ? and listing = 'r'", session["user_id"])
        y = db.execute(
            "select * from objects where id = ? and listing = 'l'",session["user_id"])

        return render_template("sell.html", x=x,y=y)



