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

class PaymentModel(db.Model):
	__tablename__ = 'payments'

	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer)
	order_id = db.Column(db.Integer)
	payment_status = db.Column(db.String())
	
	def __init__(self,order_id, amount, payment_status):
		self.order_id = order_id
		self.amount = amount
		self.payment_status = payment_status
		
	def __repr__(self):
		return f"<Payments {self.order_id}>"

import pika
import uuid


# @app.route('/payment/update', methods=['POST', 'GET'])
# def handle_product_update():
# 	if request.method == 'POST':
# 		if request.is_json:
# 			data = request.get_json()
# 			data = json.loads(data)
# 			import pdb; pdb.set_trace()
# 			payment = PaymentModel.query.get(data['payment_id'])
# 			payment.payment_status = "refund"
# 			db.session.commit()
# 			return {"message":"payment successfully refund","payment_id":payment.id,"product_status":"Refund"}

@app.route('/payments', methods=['POST', 'GET'])
def handle_product():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			try:
				payment = PaymentModel(order_id=data['order_id'],amount=data['amount'],payment_status="success")
				db.session.add(payment)
				db.session.commit()
				# check stock is available or not
				# stock_rpc = StockRpcClient()
				# stocks = stock_rpc.call(str(data['product_id']))# n
				# stocks = stocks.decode('utf-8')
				# stocks = json.dumps(stocks)
				return {"message":"payment successfully done","product_id":data['product_id'],"payment_id":payment.id }
				# return {"message": f"payment {payment.id} has been created successfully."}

			except Exception as e:
				payment = PaymentModel(order_id=data['order_id'],amount=data['amount'],payment_status="Failed")
				raise e
			
			# payment Async call
			# call Async other service API by 
			# services_rpc = ServicesRpcClient()
			# services = services_rpc.call(10)# n
			# services = services.decode('utf-8')
			# services = json.dumps(services)

			
		else:
			return {"error": "The request payload is not in JSON format"}

	elif request.method == 'GET':
		orders = PaymentModel.query.all()
		# call Async other service API by 
		# services_rpc = ServicesRpcClient()
		# services = services_rpc.call(10)# n
		# services = services.decode('utf-8')
		# services = json.dumps(services)
		results = []
		# for order in orders:
		# # 	total_quantity = 0
		# # 	stocks = StockModel.query.filter(StockModel.product_id == product.id)
		# # 	for stock in stocks:
		# # 		total_quantity += stock.quantity
		# 	result = {	
		# 		"product_id": order.product_id,
		# 		"quantity": order.total_amount,
		# 		"order_status": order.order_status

		# 	}
		# 	results.append(result)

		return {"count": len(results), "orders": results}


if __name__ == '__main__':
    app.run(port=5002,debug=True) 		