from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  'apiKey': "AIzaSyAw9d3k1hZl2A1lGt4R7xTWcXxXipRb7gI",
  'authDomain': "individual-project-31ca2.firebaseapp.com",
  'projectId': "individual-project-31ca2",
  'storageBucket': "individual-project-31ca2.appspot.com",
  'messagingSenderId': "624878426579",
  'appId': "1:624878426579:web:e8933041c0c9e0d18ab726",
  'measurementId': "G-0PLK24QBNB",
  'databaseURL': "https://individual-project-31ca2-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {'email':email, 'password': password}
            UID = login_session['user']['localId']
            db.child('User').child(UID).set(user)
            return redirect(url_for('index'))
        except Exception as e:
            print("SIGN UP ERROR:", e)
            return render_template('signup.html')
    return render_template('signup.html')
#Code goes above here

@app.route('/', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session["user"] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('index'))
        except Exception as e:
            print("SIGN IN ERROR:", e)
            return render_template('signup.html')
    return render_template('signin.html')

@app.route('/index')
def index():
    items = db.child("Items").get().val()
    return render_template('index.html', items = items)

@app.route('/rate', methods = ['GET', 'POST'])
def rate():
    if request.method == "POST":
        text = request.form['text']
        rate = request.form['rate']
        try:
            UID = login_session['user']['localId']
            rate = {'text': text, 'rate':rate, 'UID':UID}
            print(UID)
            db.child('Rating').push(rate)
            return redirect(url_for('all_ratings'))
        except:
            print("ERROR IN RATING :(")
    return render_template('rate.html')

@app.route('/all_ratings', methods = ['GET', 'POST'])
def all_ratings():
    show_ratings = db.child('Rating').get().val()
    return render_template('all_ratings.html', show = show_ratings)


@app.route('/add_to_cart/<string:item_id>')
def add_to_cart(item_id):
    pass


@app.route('/just_pretend_you_are_making_a_route', methods = ['GET', 'POST'])
def give_the_illusion():
    return render_template('all_ratings.html')
# action = '/add_item' method = "POST"

@app.route('/add_item', methods=['GET','POST'])
def add_item():
    if request.method == 'POST':
        try:
            UID = login_session['user']['localId']
            item_name = request.form['item_name']
            item_image = request.form['item_image']
            item_link = request.form['item_link']
            item = {
            'item_name': item_name,
            'item_image': item_image,
            'item_link': item_link, 
            'uid': UID
            }
            db.child("Items").push(item)
            return redirect(url_for('index'))
        except Exception as e:
            print("ERROR IN ADD ITEM: " + str(e))
    return render_template("add_item.html")


@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    if request.method == 'POST':
        try:
            UID = login_session['user']['localId']
            updated_cart = {'cart': [] }
            db.child("Users").child(UID).update(updated_cart)
            return redirect (url_for('index'))
        except:
            return render_template('cart.html')
    return render_template('cart.html')

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/maps')
def maps():
    return render_template('maps.html')

if __name__ == '__main__':
    app.run(debug=True)