from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'VenkataRavitejaKilaru'
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
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price,'stock': product.stock})

@app.route('/', methods=['GET'])
def All_products():
    product = Product.query.all()
    return render_template('index.html',product = product), 200


@app.route('/api/createProducts', methods=['GET','POST'])
def create_product():
    if request.method == 'POST':
        data = request.json
        product = Product.query.filter_by(name=data['name']).first()
        if product:
            product.price=float(data['price'])
            product.stock+=int(data['stock'])
            db.session.commit()
            return jsonify({'message': 'Product Updated successfully'}),201
        product = Product(name=data['name'], price=float(data['price']),stock=int(data['stock']))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product saved successfully'}),201
    return render_template('Create_Product.html')

@app.route('/api/order_products', methods=['GET','POST'])
def Order_product():
    if request.method == 'POST':
        data = request.json
        name=data['name']
        quantity = int(data['quantity'])
        product = Product.query.filter_by(name=name).first()
        if product:
            if quantity <= product.stock:
                order = Order(name = name, quantity = quantity)
                db.session.add(order)
                db.session.commit()
                product.stock-=quantity
                db.session.commit()
                return jsonify({"message" : "Your Order is places"}),201
            return jsonify({"message" : f"Insufficient stock! Available stock: {product.stock}"}),200
        return jsonify({"message" : f"Product not found!: {name}"}),200
    return render_template('order.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
