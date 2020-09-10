#!/usr/bin/env python
import pika
import requests
import json
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()


channel.queue_declare(queue='rpc_queue_product_remaining')
channel.queue_declare(queue='rpc_queue_stock_check')
channel.queue_declare(queue='rpc_queue_payment')
# channel.queue_declare(queue='rpc_queue_payment_return')
channel.queue_declare(queue='rpc_queue2')



def product_remainging_method_call(product):
    print("Stock method call")
    URL = "http://127.0.0.1:5000/product/update"
    PARAMS = product
    response = requests.post(url = URL, params = PARAMS,json=PARAMS)
    return response.json()

def on_request_product_remaining(ch, method, props, body):
    product = json.loads(body)
    res = product_remainging_method_call(product)
    response = json.dumps(res)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def stock_check_method_call(product_id):
    print("Stock method call")
    URL = "http://127.0.0.1:5000/get_product_stock"
    PARAMS = {"product_id":product_id}
    response = requests.post(url = URL, params = PARAMS,json=PARAMS)
    return response.json()

def on_request_stock_check(ch, method, props, body):
    product_id = int(json.loads(body))
    res = stock_check_method_call(product_id)
    response = json.dumps(res)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)



# def payment_return_method_call(payment):
#     print("get payment return method call")
#     URL = "http://127.0.0.1:5002/payment/update"
#     PARAMS = payment
#     response = requests.post(url = URL, params = PARAMS,json=PARAMS)
#     import pdb; pdb.set_trace()
#     return response.json()

# def on_request_payment_return(ch, method, props, body):
#     payment = json.loads(body)
#     res = payment_return_method_call(payment)
#     response = json.dumps(res)
#     ch.basic_publish(exchange='',
#                      routing_key=props.reply_to,
#                      properties=pika.BasicProperties(correlation_id = \
#                                                          props.correlation_id),
#                      body=response)
#     ch.basic_ack(delivery_tag=method.delivery_tag)


def payment_method_call(order):
    print("get servies method call")
    URL = "http://127.0.0.1:5002/payments"
    PARAMS = order
    response = requests.post(url = URL, params = PARAMS,json=PARAMS)
    return response.json()

def on_request_payment(ch, method, props, body):
    order = json.loads(body)
    res = payment_method_call(order)
    response = json.dumps(res)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# this method get all servies
def get_services(n):
    print("get servies method call")
    URL = "http://127.0.0.1:5001/services"
    PARAMS = {}
    response = requests.get(url = URL, params = PARAMS)
    return response.json()

def on_request2(ch, method, props, body):
    n = int(body)
    res = get_services(n)
    response = res
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)


channel.basic_consume(queue='rpc_queue_product_remaining', on_message_callback=on_request_product_remaining)
channel.basic_consume(queue='rpc_queue_stock_check', on_message_callback=on_request_stock_check)
channel.basic_consume(queue='rpc_queue_payment', on_message_callback=on_request_payment)
#channel.basic_consume(queue='rpc_queue_payment_return', on_message_callback=on_request_payment_return)
channel.basic_consume(queue='rpc_queue2', on_message_callback=on_request2)
print(" [x] Awaiting RPC requests")
channel.start_consuming()