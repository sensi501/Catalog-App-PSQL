from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from flask import session as login_session
from flask import make_response 
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from database_schema import Base, User, Category, Item
import random
import string
import httplib2
import json
import requests

# Prevents This application.py File From Being Accessed From Another Python Program
app = Flask(__name__)

# Google Sever Authentication Access Information
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog"

# Database Access Code
engine = create_engine('postgresql://catalog:Catalog1@localhost:5432/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Catalog Application Login and Hash Code Generator
@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Google Login and Server Authentication
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
    
# Create User Database Entry Utilizing Flask Login Session Info
def create_user(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

#   Get User Database Information
def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Get User ID(email address)
def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Logout From Google Account
@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON API To View All Items And Information
@app.route('/catalog.json')
def all_items_JSON():
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])

# JSON API To View All Specified Category Items And Information
@app.route('/catalog/<category_name>.json')
def category_items_JSON(category_name):
    category = session.query(Category.id).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return jsonify(items=[i.serialize for i in items])

# Read categories And Latest Items
@app.route('/')
@app.route('/catalog/')
def read_latest_items():
    categories = session.query(Category).order_by(asc(Category.name)).all()
    items =  session.query(Item).order_by(desc(Item.id)).limit(10)
    if 'username' not in login_session:
        return render_template('publiccatalog.html', categories=categories, items=items)
    else:
        return render_template('catalog.html', categories=categories, items=items)

# Read Specified Category Items
@app.route('/catalog/<category_name>/')
@app.route('/catalog/<category_name>/items')
def read_category_items(category_name):
    categories = session.query(Category).order_by(asc(Category.name)).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    length = len(items)
    if 'username' not in login_session:
        return render_template('publiccategories.html', category=category, categories=categories, items=items, length=length)
    else:
        return render_template('categories.html', category=category, categories=categories, items=items, length=length)

# Read Specified Category Item Information
@app.route('/catalog/<category_name>/<item_name>')
def read_item_information(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one
    item = session.query(Item).filter_by(name=item_name).one()
    if 'username' not in login_session:
        return render_template('publicitem.html', item=item)
    else:
        return render_template('item.html', item=item)

# Create Catalog Item
@app.route('/catalog/new/', methods=['GET', 'POST'])
def create_item():
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    if request.method == 'POST':
        category = session.query(Category).filter_by(name=request.form['category']).one()
        item_name = request.form['name']
        item_name = item_name.replace(' ', '_')
        new_item = Item(
            name=item_name, 
            description=request.form['description'], 
            category_id=category.id, 
            user_id=login_session['user_id']
            )
        session.add(new_item)
        session.commit()
        flash('%s Item Successfully Created' % (new_item.name).replace('_', ' '))
        return redirect(url_for('read_latest_items'))
    else:
        return render_template('createitem.html', categories=categories)

# Edit Catalog Item
@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def update_item(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    edited_item = session.query(Item).filter_by(name=item_name).one()
    if login_session['user_id'] != edited_item.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this item. Please edit your own items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            edited_item.name = request.form['name']
        if request.form['description']:
            edited_item.description = request.form['description']
        if request.form['category']:
            edited_item.category_id = request.form['category']
        session.add(edited_item)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('read_latest_items'))
    else:
        return render_template('updateitem.html', categories=categories, item_name=item_name, item=edited_item)

# Delete Item
@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def delete_item(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    item_to_delete = session.query(Item).filter_by(name=item_name).one()
    if login_session['user_id'] != item_to_delete.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this item. Please delete your own items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('read_latest_items'))
    else:
        return render_template('deleteitem.html', item=item_to_delete)

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('read_latest_items'))
    else:
        flash("You were not logged in")
        return redirect(url_for('read_latest_items'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run()
