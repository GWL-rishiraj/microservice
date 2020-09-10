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


import pika
import uuid
class PaymentRpcClient(object):

	def __init__(self):
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host='localhost'))

		self.channel = self.connection.channel()

		result = self.channel.queue_declare(queue='', exclusive=True)
		self.callback_queue = result.method.queue

		self.channel.basic_consume(
			queue=self.callback_queue,
			on_message_callback=self.on_response,
			auto_ack=True)

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body

	def call(self, order):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		order = json.dumps(order)
		self.channel.basic_publish(
			exchange='',
			routing_key='rpc_queue_payment',
			properties=pika.BasicProperties(
				reply_to=self.callback_queue,
				correlation_id=self.corr_id,
			),
			body=order)
		while self.response is None:
			self.connection.process_data_events()
		return self.response

	def payment_return_call(self, payment):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		payment = json.dumps(payment)
		self.channel.basic_publish(
			exchange='',
			routing_key='rpc_queue_payment_return',
			properties=pika.BasicProperties(
				reply_to=self.callback_queue,
				correlation_id=self.corr_id,
			),
			body=payment)
		while self.response is None:
			self.connection.process_data_events()
		return self.response	


class StockRpcClient(object):

	def __init__(self):
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host='localhost'))

		self.channel = self.connection.channel()

		result = self.channel.queue_declare(queue='', exclusive=True)
		self.callback_queue = result.method.queue

		self.channel.basic_consume(
			queue=self.callback_queue,
			on_message_callback=self.on_response,
			auto_ack=True)

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body

	def call(self, stock_response):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		# order = producd_id
		stocks = json.dumps(stock_response)
		self.channel.basic_publish(
			exchange='',
			routing_key='rpc_queue_stock_check',
			properties=pika.BasicProperties(
				reply_to=self.callback_queue,
				correlation_id=self.corr_id,
			),
			body=stocks)
		while self.response is None:
			self.connection.process_data_events()
		return self.response

	def product_remaining_call(self, stock_response):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		# order = producd_id
		stocks = json.dumps(stock_response)
		self.channel.basic_publish(
			exchange='',
			routing_key='rpc_queue_product_remaining',
			properties=pika.BasicProperties(
				reply_to=self.callback_queue,
				correlation_id=self.corr_id,
			),
			body=stocks)
		while self.response is None:
			self.connection.process_data_events()
		return self.response	

@app.route('/orders', methods=['POST', 'GET'])
def handle_product():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			order = OrderModel(product_id=data['product_id'],quantity= data['quantity'] ,total_amount=data['total_amount'],order_status="pending")
			db.session.add(order)
			db.session.commit()
			# here we need to call payment callback
			order_dict = {"order_id":order.id,"product_id":order.product_id,"quantity":order.quantity,"amount":order.total_amount}
			payment_rpc = PaymentRpcClient()
			payments = payment_rpc.call(order_dict)# n
			payments = payments.decode('utf-8')
			# import pdb; pdb.set_trace()
			# payments = json.dumps(payments)


			# check stock is available or not
			stock_rpc = StockRpcClient()
			stocks = stock_rpc.call(order.product_id)# n
			stocks = stocks.decode('utf-8')
			stocks = json.loads(stocks)


			# if stock is available and ready for delivery
			if stocks["total"] >= order.quantity:
				order.order_status = "delivered"
				db.session.commit()
				remaining_product_quantity = stocks["total"] - order.quantity
				# here we need to add product remaining code

				stock_rpc = StockRpcClient()
				product_remaing = stock_rpc.product_remaining_call(order_dict)# n
				product_remaing = product_remaing.decode('utf-8')
				product_remaing = json.loads(product_remaing)
				return {
				"message": f"order {order.product_id} has been created successfully.",
				"payments":json.loads(payments),
				"stocks":stocks,
				"order_status":order.order_status,
				"product_remaing":product_remaing
				}
			# if stock is not available at the delivery time
			else:
				order.order_status = "failed"
				db.session.commit()

				# payment return method call
				#payment_rpc = PaymentRpcClient()
				#payment_retun = payment_rpc.payment_return_call(payments)# n
				#import pdb; pdb.set_trace()
				# payment_retun = payment_retun.decode('utf-8')
				# payment_retun = json.loads(payment_retun)

				return {
				"message": f"order {order.product_id} has been created successfully.",
				"payments":json.loads(payments),
				"payment" : "payment will be return soon",
				"stocks":stocks,
				"order_status":order.order_status,
				"product_remaing":stocks
				}


				




			return {"message": f"order {order.product_id} has been created successfully.","payments":json.loads(payments),"stocks":stocks}
		else:
			return {"error": "The request payload is not in JSON format"}

	elif request.method == 'GET':
		orders = OrderModel.query.all()
		# call Async other service API by 
		# services_rpc = ServicesRpcClient()
		# services = services_rpc.call(10)# n
		# services = services.decode('utf-8')
		# services = json.dumps(services)
		results = [{}]
		for order in orders:
		# 	total_quantity = 0
		# 	stocks = StockModel.query.filter(StockModel.product_id == product.id)
		# 	for stock in stocks:
		# 		total_quantity += stock.quantity
			result = {	
				"product_id": order.product_id,
				"quantity": order.total_amount,
				"order_status": order.order_status

			}
			results.append(result)

		return {"count": len(results), "orders": results}


if __name__ == '__main__':
    app.run(port=5001,debug=True) 		