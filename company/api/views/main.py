from flask import Blueprint, request
from api.models import db,Project
from api.models.Company import *
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect
import boto3
main = Blueprint("main", __name__)  # initialize blueprint


# function that is called when you visit /
@main.route("/")
def index():
    # you are now in the current application context with the main.route decorator
    # access the logger with the logger from api.core and uses the standard logging module
    # try using ipdb here :) you can inject yourself
    sqs = boto3.resource('sqs')

    # Create the queue. This returns an SQS.Queue instance
    #queue = sqs.create_queue(QueueName='company_contacts', Attributes={'DelaySeconds': '5'})
    queue = sqs.create_queue(QueueName='company_contacts')
    print("----------------------------")
    # You can now access identifiers and attributes
    print(queue.url)
    print(queue)
    response = queue.send_message(MessageBody='Rishi SQS message')
    # The response is NOT a resource, but gives you a message ID and MD5
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))
    print("----------------------------")
    logger.info("Hello World!")
    return "<h1>Hello World!</h1>"

@main.route("/read_sqs")
def read_sqs():
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='company_contacts')

    # Process messages by printing out body and optional author name
    # for message in queue.receive_messages(MessageAttributeNames=['Author']):
    msg = ""
    for message in queue.receive_messages():
        # Get the custom author message attribute if it was set
        author_text = ''
        if message.message_attributes is not None:
            '''author_name = message.message_attributes.get('Author').get('StringValue')
            if author_name:
                author_text = ' ({0})'.format(author_name)'''

        # Print out the body and author (if set)
        msg += ' SQS message, {0}!'.format(message.body)
        print(msg)

        # Let the queue know that the message is processed
        #message.delete()

    return "<h1>"+msg+"</h1>"

@main.route("/companies", methods=["GET"])
def get_persons():
    companies = Company.query.all()
    return create_response(data={"Companies": serialize_list(companies)})


@main.route("/add_company_type", methods=["POST"])
def create_company_type():
    data = request.get_json()

    logger.info("Data recieved: %s", data)
    if "type" not in data:
        msg = "Please supply a type name."
        logger.info(msg)
        return create_response(status=422, message=msg)

    # create SQLAlchemy Objects
    new_company_type = CompanyType(type=data["type"])
    #email = Email(email=data["email"])
    #new_person.emails.append(email)

    # commit it to database
    db.session.add_all([new_company_type])
    db.session.commit()
    return create_response(
        message=f"Successfully created company type {new_company_type.type} with id: {new_company_type.id}"
    )

@main.route("/add_company", methods=["POST"])
def create_company():
    data = request.get_json()

    logger.info("Data recieved: %s", data)
    if "name" not in data:
        msg = "Please supply a company name."
        logger.info(msg)
        return create_response(status=422, message=msg)

    if "company_type" not in data:
        msg = "Please supply a company_type."
        logger.info(msg)
        return create_response(status=422, message=msg)

    if "description" not in data:
        msg = "Please supply a company description."
        logger.info(msg)
        return create_response(status=422, message=msg)

    if "address" not in data:
        msg = "Please supply a company address."
        logger.info(msg)
        return create_response(status=422, message=msg)
    try:
        # create SQLAlchemy Objects
        new_company = Company(name=data["name"])
        company_type = data["company_type"] #CompanyType(id=data["company_type"])
        print(company_type)
        new_company.company_type = company_type
        new_company.description = data["description"]
        new_company.address = data["address"]
        new_company.phone = data["phone"]
        new_company.MSA = data["MSA"]
        new_company.NDS = data["NDS"]
        new_company.url = data["url"]
        new_company.logo = data["logo"]
        db.session.add_all([new_company])
        db.session.commit()
    except Exception as e:
        print("+++++++++++++++++++++++++++++")
        print(e)
        return create_response(status=422, message=e)
    return create_response(
        message=f"Successfully created company {new_company.name} with id: {new_company.id}"
    )



# function that is called when you visit /persons
'''@main.route("/persons", methods=["GET"])
def get_persons():
    persons = Person.query.all()
    return create_response(data={"persons": serialize_list(persons)})


# POST request for /persons
@main.route("/persons", methods=["POST"])
def create_person():
    data = request.get_json()

    logger.info("Data recieved: %s", data)
    if "name" not in data:
        msg = "No name provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "email" not in data:
        msg = "No email provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)

    # create SQLAlchemy Objects
    new_person = Person(name=data["name"])
    email = Email(email=data["email"])
    new_person.emails.append(email)

    # commit it to database
    db.session.add_all([new_person, email])
    db.session.commit()
    return create_response(
        message=f"Successfully created person {new_person.name} with id: {new_person._id}"
    )
'''
