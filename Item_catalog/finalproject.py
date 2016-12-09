from flask import Flask
app =  Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return "this page will show all my restaurants"

@app.route('/restaurants/new')
def newRestaurant():
    return("this page will be for making new restaurant")

@app.route('/restaurants/restaurant_id/edit')
def editRestaurant():
    return "this page will be for editing restaurant %s"

@app.route('/restaurants/restaurant_id/delete')
def deleteRestaurant():
    return "this page will be for deleting restaurant %s"

@app.route('/restaurants/restaurant_id/menu')
@app.route('/restaurants/restauant_id')
def showMenu():
    return "this page is the menu for restaurant %s"

@app.route('/restaurants/restaurant_id/menu/new')
def newMenuItem():
    return "this page is for making a new menu item for restaurant %s" 

@app.route('/restaurants/restaurant_id/menu_id/edit')
def editMenuItem():
    return "this page is for editing the menu item %s"

@app.route('/restaurants/restaurant_id/menu_id/delete')
def deleteMenuItem():
    return "this page is for  deleting the menu item %s"


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5003)
