from flask import Flask, render_template, url_for, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    supplier  = db.Column(db.String(200), nullable = True)
    purchaser = db.Column(db.String(200), nullable = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)


    def __repr__(self):
        return '<item %r>' % self.id


@app.route('/')
def index():
    items = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', items = items)

@app.route('/delete/<int:id>')
def delete(id):
    item_delete = Todo.query.get_or_404(id)

    try: 
        db.session.delete(item_delete)
        db.session.commit()
        return redirect ('/')
    except: 
        return 'There was an error %r' %id

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id): 
    item = Todo.query.get_or_404(id)

    if request.method == 'POST':
        item.name = request.form['name']
        item.price = request.form['price']
        item.quantity = request.form['quantity']
        item.supplier = request.form['supplier']
        item.purchaser = request.form['purchaser']


        try: 
            db.session.commit()
            return redirect('/')
        except: 
            return 'There was an issue'
    
    else: 
        return render_template('update.html', item = item)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        item_name = request.form['name']
        item_price = request.form['price']
        item_quantity = request.form['quantity']
        item_supplier = request.form['supplier']
        item_purchaser = request.form['purchaser']

        new_item = Todo(name = item_name, price = item_price, quantity = item_quantity, supplier = item_supplier,
         purchaser = item_purchaser)

        try: 
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')

        except: 
            return 'There was an issue'

    else:
        return render_template('add.html')

@app.route('/export')
def export():
    items = Todo.query.order_by(Todo.date_created).all()

    with open('inventory.csv', 'w', newline = '') as f:
        writer = csv.writer(f)

        writer.writerow(['item', 'price', 'quantity', 'supplier', 'purchaser', 'date added'])
        
        for item in items: 
            writer.writerow([item.name, item.price, item.quantity, item.supplier, item.purchaser, item.date_created.isoformat()])
    
    return redirect ('/')


if __name__ == "__main__":
    app.run(debug = True)