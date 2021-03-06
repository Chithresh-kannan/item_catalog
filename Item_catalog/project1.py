from flask import Flask,render_template, request, redirect,url_for,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)
# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newitem = MenuItem(name = request.form('name'),restaurant_id = restaurant_id)
        session.add(newitem)
        session.commit()
        flash("new menu item created!!")
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))

    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    edited_item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'post':
        if request.form['name']:
            edited_item.name = request.form['name']
        session.add(edited_item)
        session.commit()
        flash("Menu item has been deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = edited_item)
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods = ['get','post'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(Restaurant).filter_by(id = menu_id).one()
    if request.method == 'post':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu item has been deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:  
        return render_template('deleteMenuItem.html', i = itemToDelete)

if __name__ == '__main__':
    app.secret_key = 'my_name_is_khan'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
