from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/category/<int:category_id>/')
def menuCategories(category_id):
    category = session.query(Category).filter_by(id=category_id).one()    
    items = session.query(CategoryItem).filter_by(category_id = category.id)
    return render_template('menu.html',category=category, items=items)

@app.route('/category/<int:category_id>/new/', methods=['GET','POST'])
def newCategoryItem(category_id):
    if request.method == 'POST':
        newItem = CategoryItem(name=request.form['name'],category_id=category_id)
        session.add(newItem)
        session.commit()  
        flash("New category item created!!")  
        return redirect(url_for('menuCategories', category_id=category_id))
    else:
        return render_template('newcategoryitem.html', category_id=category_id)    

@app.route('/category/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Category item Updated!!") 
        return redirect(url_for('menuCategories', category_id=category_id))
    else:
        return render_template('editcategoryitem.html', category_id = category_id, item_id = item_id, item = editedItem)

@app.route('/category/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Category item Deleted!!") 
        return redirect(url_for('menuCategories', category_id = category_id))
    else:
        return render_template('deletecategoryitem.html', item=itemToDelete)
    return "page to delete a category  item. Task 3 complete!"
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)