from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

app = Flask(__name__)
#app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/sagapattern"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ProductModel(db.Model):
	__tablename__ = 'products'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	price = db.Column(db.Integer)
	quantity = db.Column(db.Integer)
	remaining_quantity = db.Column(db.Integer)

	def __init__(self, name, price,quantity,remaining_quantity):
		self.name = name
		self.price = price
		self.quantity = quantity
		self.remaining_quantity = remaining_quantity


	def __repr__(self):
		return f"<Product {self.name}>" 


class StockModel(db.Model):
	__tablename__ = 'stocks'

	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer)
	quantity = db.Column(db.Integer)
	remaining_quantity = db.Column(db.Integer)
	
	def __init__(self, product_id, quantity,remaining_quantity):
		self.product_id = product_id
		self.quantity = quantity
		self.remaining_quantity = remaining_quantity
	def __repr__(self):
		return f"<Stock {self.product_id}>" 

class OrderModel(db.Model):
	__tablename__ = 'orders'

	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer)
	quantity = db.Column(db.Integer)
	total_amount = db.Column(db.Integer)
	order_status = db.Column(db.String())
	
	def __init__(self, product_id,quantity, total_amount, order_status):
		self.order_status = order_status
		self.product_id = product_id
		self.quantity = quantity
		self.total_amount = total_amount
		
	def __repr__(self):
		return f"<Order {self.product_id}>"

class PaymentModel(db.Model):
	__tablename__ = 'payments'

	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer)
	amount = db.Column(db.Integer)
	payment_status = db.Column(db.String())
	
	def __init__(self,order_id, amount, payment_status):
		self.order_id = order_id
		self.payment = payment
		self.payment_status = payment_status
		
	def __repr__(self):
		return f"<Payments {self.order_id}>"		
# Imports and ProjectModel truncated



@app.route('/products', methods=['POST', 'GET'])
def handle_product():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			product = ProductModel(name=data['name'], price=data['price'],quantity=data['quantity'],remaining_quantity=data['quantity'])
			db.session.add(product)
			db.session.commit()
			# if "quantity" in data:
			# 	stock = StockModel(product_id=product.id, quantity=data['quantity'],remaining_quantity=data['quantity'])
			# 	db.session.add(stock)
			# 	db.session.commit()
			return {"message": f"project {product.name} has been created successfully."}
		else:
			return {"error": "The request payload is not in JSON format"}

	elif request.method == 'GET':
		products = ProductModel.query.all()
		results = []
		for product in products:
			# total_quantity = 0
			# stocks = StockModel.query.filter(StockModel.product_id == product.id)
			# for stock in stocks:
			# 	total_quantity += stock.quantity
			result = {	
				"product_id":product.id,
				"name": product.name,
				"price": product.price,
				"quantity": product.quantity

			}
			results.append(result)

		return {"count": len(results), "products": results}


# @app.route('/get_product_stock',methods = ['POST'])
# def handle_product_stock():
# 	if request.method == 'POST':
# 		if request.is_json:
# 			data = request.get_json()
# 			stocks = StockModel.query.filter(StockModel.product_id == data['product_id'])
# 			stocks = stocks.all()
# 			total = 0
# 			for stock in stocks:
# 				total += stock.remaining_quantity
# 			return { "total":total }


@app.route('/get_product_stock',methods = ['POST'])
def handle_product_stock():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			if "product_id" not in data:
				return { "error":"product_id not define" }

			stock = ProductModel.query.get(data['product_id'])
			if stock:
				return { "total":stock.remaining_quantity }
			else:
				return { "error":"product id is not valid" }	

@app.route('/product/update',methods = ['POST'])
def handle_product_update():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			if "product_id" not in data:
				return { "error":"product_id not define" }

			product = ProductModel.query.get(data['product_id'])
			if product:
				product.remaining_quantity = product.remaining_quantity - data['quantity']
				db.session.commit()
				return { "total": product.remaining_quantity }
			else:
				return { "error":"product id is not valid" }


if __name__ == '__main__':
	app.run(debug=True)   

