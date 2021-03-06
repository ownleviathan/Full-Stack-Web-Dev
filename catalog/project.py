from flask import (Flask, render_template, request, redirect, jsonify,
                   url_for, flash, make_response)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Google Login


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()

    result = json.loads(h.request(url, 'GET')[1].decode('utf8'))

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['access_token'] = credentials.access_token
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
                  150px;-webkit-border-radius: 150px;-moz-border-radius:\
                  150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/logout')
def logout():
    """Log out the currently connected user."""

    if 'username' in login_session:
        gdisconnect()
        del login_session['provider']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        flash("You have been successfully logged out!")
        return redirect(url_for('homePage'))
    else:
        flash("You were not logged in!")
        return redirect(url_for('homePage'))
# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
                                'Failed to revoke token for given user.',
                                400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Route to main page
@app.route('/')
def homePage():
    categories = session.query(Category).order_by(Category.name).all()
    return render_template('index.html', categories=categories,
                           login_session=login_session)


# Create Category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
        category = session.query(Category).filter_by(
                   name=request.form['category-name']).first()

        if category is not None:
            flash('The entered category already exists.')
            return redirect(url_for('newCategory'))

        newCategory = Category(name=request.form['category-name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash("New category was created!!")
        return redirect(url_for('homePage'))
    else:
        return render_template('newcategory.html')


# Edit Category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):

    category = session.query(Category).filter_by(id=category_id).first()

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))

    if login_session['user_id'] != category.user_id:
        flash("You are not authorized to modify %s category." % category.name)
        return redirect(url_for('homePage'))

    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
        session.add(category)
        session.commit()
        flash("Category was Updated!!")
        return redirect(url_for('homePage'))
    else:
        return render_template('editcategory.html', category=category)


# Delete Category Item
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):

    categoryToDelete = session.query(Category).filter_by(
                       id=category_id).first()

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))

    if login_session['user_id'] != categoryToDelete.user_id:
        flash("You are not authorized to delete %s category."
              % categoryToDelete.name)
        return redirect(url_for('homePage'))

    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash("Category was Deleted!!")
        return redirect(url_for('homePage'))
    else:
        return render_template('deletecategory.html',
                               category=categoryToDelete)


# CRUD FOR ITEMS
# Select all items of a Category
@app.route('/category/<int:category_id>/')
def itemsCategories(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    return render_template('itemsCategory.html', category=category,
                           items=items)


# Create item for a Category
@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))

    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':

        newItem = CategoryItem(name=request.form['name'],
                               price='$' + request.form['price'],
                               description=request.form['description'],
                               category_id=category_id)
        session.add(newItem)
        session.commit()
        flash("New category item created!!")
        return redirect(url_for('itemsCategories', category_id=category_id))
    else:
        return render_template('newcategoryitem.html', category_id=category_id,
                               category=category)


# Edit Category Item
@app.route('/category/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):

    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))

    if login_session['user_id'] != editedItem.user_id:
        flash("You are not authorized to edit %s item."
              % editedItem.name)
        return redirect(url_for('homePage'))

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            editedItem.price = '$' + request.form['price']
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash("Category item Updated!!")
        return redirect(url_for('itemsCategories', category_id=category_id))
    else:
        return render_template('editcategoryitem.html',
                               category_id=category_id,
                               item_id=item_id, item=editedItem)


# Delete Category Item
@app.route('/category/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()

    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))

    if login_session['user_id'] != itemToDelete.user_id:
        flash("You are not authorized to delete %s item."
              % itemToDelete.name)
        return redirect(url_for('homePage'))

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Category item Deleted!!")
        return redirect(url_for('itemsCategories', category_id=category_id))
    else:
        return render_template('deletecategoryitem.html', item=itemToDelete)


# Check if the category exists in the database.
def exists_category(category_id):
    """Check if the category exists in the database.
       Returns a Boolean True or False
    """
    category = session.query(Category).filter_by(id=category_id).first()
    if category is not None:
        return True
    else:
        return False


# Check if the item exists in the database,
def exists_item(item_id):
    """Check if the item exists in the database.
       Return a Boolean True of False
    """
    item = session.query(CategoryItem).filter_by(id=item_id).first()
    if item is not None:
        return True
    else:
        return False


# JSON Endpoints
# Return JSON of all the items in the catalog.
@app.route('/api/v1/catalog.json')
def show_catalog_json():
    """Return JSON of all the items in the catalog."""

    categories = session.query(Category).order_by(Category.name).all()
    return jsonify(catalog=[i.serialize for i in categories])


# Return JSON of a particular item in the catalog.
@app.route(
    '/api/v1/categories/<int:category_id>/item/<int:item_id>/JSON')
def catalog_item_json(category_id, item_id):
    """Return JSON of a particular item in the catalog."""

    if exists_category(category_id) and exists_item(item_id):
        item = session.query(CategoryItem)\
               .filter_by(id=item_id, category_id=category_id).first()
        if item is not None:
            return jsonify(item=item.serialize)
        else:
            return jsonify(
                error='item {} is not part of the category {}.'
                .format(item_id, category_id))
    else:
        return jsonify(error='The item or the category does not exist.')


# Return JSON of all the categories in the catalog.
@app.route('/api/v1/categories/JSON')
def categories_json():
    """Returns JSON of all the categories in the catalog."""

    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000, debug=True)
