from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price})

@app.route('/api/allproducts', methods=['GET'])
def All_products():
    product = Product.query.all()
    print(product)
    return render_template('index.html',product = product), 200

@app.route('/add_product')
def add_product():
    return render_template('Create_Product.html')

@app.route('/api/createProducts', methods=['POST'])
def create_product():
    data = request.json
    product = Product(name=data['name'], price=data['price'],stock=data['stock'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product saved successfully'}),201

@app.route('/api/order_products', methods=['GET','POST'])
def Order_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        order = Order(name = name, quantity = quantity)
        return jsonify({"message":"Your Order is places"}), 200
    return render_template('order.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
