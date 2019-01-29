from flask import Flask, render_template, request, url_for, redirect , session 
import database
from database import get_one
app = Flask(__name__)
identity = 0

@app.route('/')
def fpage():
    return render_template("fpage.html")

@app.route('/mainpage')
def mainpage():
    #equivalent of saying "Is there a user logged in?"
    if "login" in session and session["login"]:
        username = session["username"]
        info = database.get_user_info(username)
        return render_template("mainpage.html", info=info if info else [])
    # elif "signout" in session and session["signout"]:
    else:    
        
        return "you're not logged in"


@app.route('/details/<int:i>')
def detail_log(i):
    if "login" in session and session["login"]:
        username = session["username"]
        # info = database.get_user_info(username)
        ip = get_one(i)
        return render_template("details.html", ip = ip)
    else:
        return "you're not logged in"
@app.route('/sign-up', methods=["POST", "GET"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == "POST":
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        

        try:
            database.add_account(first_name, last_name, username, password, age)
            return redirect(url_for('login'))
            
        except Exception as e:
            print("Error")
            return render_template("signup.html", error_message=str(e.__repr__()))
        return redirect(url_for('fpage'))

@app.route('/log-in', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if database.check_user_and_pass(request.form['username'], request.form['password']) == True:
            session['login'] = True
            session['username'] = request.form['username']
            print("success")
            # run a differnet function
            info = database.get_user_info(session["username"])
            return redirect(url_for("mainpage", info=info if info else []))
        else:
            print('error:username or password are incorrect!!')
            return render_template('login.html', incorrect_user_or_pass='error:username or password are incorrect!! ')
    return redirect(url_for('fpage'))

@app.route('/add_info', methods=['GET', 'POST'])
def add_info():
    if "login" in session and session["login"]:
        username = session["username"] 

        if request.method =='GET':
            return render_template ("add_info.html")
        elif request.method=='POST':
            
                # identity= session['identity']
                name = request.form['name']
                quantity = request.form['quantity']

                database.add_info(name,quantity, submitted=session["username"])
                info = database.print_info()

                print(name, quantity)

            # return redirect(url_for('mainpage'),add=add)
                
                return redirect(url_for("mainpage"))
    else:
        return"you are not logged in"
    return redirect(url_for("mainpage"))    

@app.route("/decrease", methods=["POST"])
def decrease_item():
    identity = request.form["identity"]
    database.decrease_quantity(identity)
    return redirect(url_for("detail_log", i=identity))

@app.route("/increase", methods=["POST"])
def increase_item():
    identity = request.form["identity"]
    database.increase_quantity(identity)
    return redirect(url_for("detail_log", i=identity))

@app.route("/delete", methods=["POST"])
def delete_item():
    identity = request.form["identity"]
    database.delete_item(identity)
    return redirect(url_for("mainpage", i=identity))



@app.route('/signout')
def signout():
    # session['signout']=True
    session.clear()
    return redirect(url_for('fpage'))



if __name__ == '__main__':
    app.secret_key = 'super secret key'    
    app.run(debug=True)

