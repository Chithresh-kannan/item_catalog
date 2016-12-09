from flask import Flask
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import base, Restaurant,MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantmenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    output = ""
    for i in items:
        output += i.name
        output += "</br>"
        output += i.price
        output += "</br>"
        output += i.description
        output += "</br></br>"
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
