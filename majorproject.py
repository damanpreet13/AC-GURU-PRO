from flask import *
import datetime
from session2 import MongoDBHelper
import hashlib
from bson.objectid import ObjectId

web_app = Flask("Ac service")

@web_app.route('/About-Us')
def about_us_info():
    return render_template('about-us.html')

@web_app.route('/about-Us')
def about_us_1():
    return render_template('about-us2.html')

@web_app.route('/Contact-Us')
def contact_us_info():
    return render_template('contact us.html')

@web_app.route('/contact-Us')
def contact_us_1():
    return render_template('contact us2.html')

@web_app.route('/back')
def back_from_about_us():
    return render_template('index2.html')

@web_app.route('/Back')
def back_from_contact_us():
    return render_template('home2.html')

@web_app.route('/Terms')
def terms_cond():
    return render_template('terms.html')

@web_app.route('/terms')
def terms_cond_1():
    return render_template('terms2.html')


@web_app.route("/")
def index():
    return render_template('index2.html')

@web_app.route("/register")
def register():
    return render_template('register.html')

@web_app.route("/home2")
def home():
    return render_template('home2.html')

"""login register starts"""

@web_app.route("/register-mechanic", methods=['POST'])
def register_mechanic():
    mechanic_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
        'createdon': datetime.datetime.today()
    }
    if len(mechanic_data['name']) == 0 or len(mechanic_data['email']) == 0 or len(mechanic_data['password']) == 0:
        return render_template('error1.html', message="Something is missing...")

    print(mechanic_data)
    db = MongoDBHelper(collection="servicer")
    result = db.insert(mechanic_data)
    mechanic_id = result.inserted_id
    session['mechanic_id'] = str(mechanic_id)
    session['mechanic_name'] = mechanic_data['name']
    session['mechanic_email'] = mechanic_data['email']
    return render_template('home2.html', name=session['mechanic_name'], email=session['mechanic_email'])

@web_app.route("/login-mechanic", methods=['POST'])
def login_mechanic():
    mechanic_data = {
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
    }
    if len(mechanic_data['email']) == 0 or len(mechanic_data['password']) == 0:
        return render_template('error1.html', message="Something is missing...")

    print(mechanic_data)
    db = MongoDBHelper(collection="servicer")
    documents = list(db.fetch({'email': mechanic_data['email']}))
    #documents = list(db.fetch(mechanic_data))
    print(documents, type(documents))
    if len(documents) == 1:
       if documents[0]['password'] == mechanic_data['password']:
        session['mechanic_id'] = str(documents[0]['_id'])
        session['mechanic_email'] = (documents[0]['email'])
        session['mechanic_name'] = (documents[0]['name'])
        return render_template('home2.html', email=session['mechanic_email'], name=session['mechanic_name'])

    return render_template('error1.html', message="Invalid email or password")

    #else:
       # return render_template('error2.html', message="Invalid Login!!")

@web_app.route("/logout")
def logout():
    session['mechanic_id'] = ""
    session['mechanic_email'] = ""
    return redirect("/")

"""login register end -------- """


"""# customer start----------------------#"""

@web_app.route("/add-customer",methods=['POST'])
def add_patient():
    customer_data = {
        'name': request.form['name'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'address': request.form['address'],
        'mechanic_name': session['mechanic_name'],
        'mechanic_id': session['mechanic_id'],
        'mechanic_email': session['mechanic_email'],
        'createdon': datetime.datetime.today()
    }
    if len(customer_data['name']) == 0 or len(customer_data['phone']) == 0 or len(customer_data['email']) == 0:
        return render_template('error2.html', message="Name, Phone and Email cannot be Empty")

    print(customer_data)
    db = MongoDBHelper(collection="customer")
    db.insert(customer_data)
    return render_template('success2.html', message="{} Added Successfully".format(customer_data['name']))

@web_app.route("/fetch-customer")
def fetch_customer_by_mechanic():
    db = MongoDBHelper(collection="customer")
    query = {'mechanic_id': session['mechanic_id']}
    documents = list(db.fetch(query))
    print(documents,type(documents))
    return render_template('customer2.html', email=session['mechanic_email'], name=session['mechanic_name'], documents=documents)

@web_app.route("/delete-customer/<id>")
def delete_patient(id):
    db = MongoDBHelper(collection="customer")
    query = {'_id': ObjectId(id)}
    customer = db.fetch(query)[0]
    db.delete(query)
    return render_template('success2.html', message="customer {} deleted".format(customer['name']))

@web_app.route("/update-customer/<id>")
def update_customer(id):
    db = MongoDBHelper(collection="customer")
    query = {'_id': ObjectId(id)}
    customer = db.fetch(query)[0]
    return render_template('update-customer.html', email=session['mechanic_email'],
                           name=session['mechanic_name'], customer=customer)

@web_app.route("/update-customer-db", methods=['POST'])
def update_customer_in_db():
    customer_data_to_update = {
        'name': request.form['name'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'address': request.form['address'],
    }
    if len(customer_data_to_update['name']) == 0 or len(customer_data_to_update['phone']) == 0 or len(customer_data_to_update['email']) == 0 or len(customer_data_to_update['address']) == 0 :
        return render_template('error.html', message="Name, Phone and Email cannot be Empty")
    print(customer_data_to_update)
    db = MongoDBHelper(collection="customer")
    query = {'_id': ObjectId(request.form['cid'])}
    db.update(customer_data_to_update, query)
    return render_template('success2.html', message="{} updated successfully".format(customer_data_to_update['name']))

"""customer ends----------------#"""

"""#search for customer-----------------#"""
@web_app.route("/search")
def search():
    return render_template('search2.html', email=session['mechanic_email'],
                           name=session['mechanic_name'])
@web_app.route("/search-customer",methods=['POST'])
def search_customer():
    db = MongoDBHelper(collection="customer")
    query = {'email': request.form['email'], 'mechanic_id': session['mechanic_id']}
    customer = db.fetch(query)
    if len(customer) == 1:
        customer = customer[0]
        return render_template('customer-profile2.html', customer= customer,
                               email=session['mechanic_email'],
                               name=session['mechanic_name'])
    else:
        return render_template('error2.html', message="Customer Not Found...")

"""#search ended------------------------#"""

"""# appliances start---------------------#"""
@web_app.route("/add-ac/<id>")
def add_ac(id):
    db = MongoDBHelper(collection="customer")
    # To fetch customer where email and vet id will match
    query = {'_id': ObjectId(id)}
    customers = db.fetch(query)
    customer = customers[0]
    return render_template("add-ac2.html",
                           mechanic_id=session['mechanic_id'],
                           email=session['mechanic_email'],
                           name=session['mechanic_name'],
                           customer=customer)

@web_app.route("/save-ac", methods=["POST"])
def save_ac():

    ac_data = {
        'ac category': request.form['ac category'],
        'ac brand': request.form['ac brand'],
        'customer_id': request.form['customer_id'],
        'customer_email': request.form['customer_email'],
        'mechanic_id': session['mechanic_id'],
        'createdon': datetime.datetime.today()
    }
    if len(ac_data['ac category']) == 0 or len(ac_data['ac brand']) == 0:
        return render_template('error2.html', message="Category and Brand cannot be Empty")

    print(ac_data)
    db = MongoDBHelper(collection="acs")
    db.insert(ac_data)

    return render_template('success2.html', message="Ac added for customer {} successfully.."
                               .format( ac_data['customer_email']))

@web_app.route("/fetch-ac/<id>")
def fetch_acs_of_customer(id):
    db = MongoDBHelper(collection="customer")
    query = {'_id': ObjectId(id)}
    customer = db.fetch(query)[0]

    db = MongoDBHelper(collection="acs")
    query = {'mechanic_id': session['mechanic_id'],'customer_id':id}
    documents = list(db.fetch(query))
    print(documents,type(documents))
    #return "Customers Fetched For The ac{}".format(session['mechanic_name'])
    return render_template('ac2.html',
                           email=session['mechanic_email'],
                           name=session['mechanic_name'],
                           customer=customer,
                           documents=documents)

@web_app.route("/delete-ac/<id>")
def delete_ac(id):
    db = MongoDBHelper(collection="acs")
    query = {'_id': ObjectId(id)}
    ac = db.fetch(query)[0]
    db.delete(query)
    return render_template('success2.html', message="AC deleted")

"""#appliances ended-----------------#"""

"""# services start-------------------#"""
@web_app.route("/add-service/")
def add_service():
    cid = request.args.get("cid")
    acid = request.args.get("acid")
    print("ID:", cid)
    db = MongoDBHelper(collection="customer")
    # To fetch customer where email and vet id will match
    query = {'_id': ObjectId(cid)}
    customers = db.fetch(query)
    customer = customers[0]
    print("customers:", customers)
    print("customer:", customer)

    db = MongoDBHelper(collection="acs")
    # To fetch customer where email and vet id will match
    query = {'_id': ObjectId(acid)}
    acs = db.fetch(query)
    ac = acs[0]
    return render_template("add-service.html",
                           mechanic_id=session['mechanic_id'],
                           email=session['mechanic_email'],
                           name=session['mechanic_name'],
                           ac=ac,
                           customer=customer)


@web_app.route("/save-service", methods=["POST"])
def save_service():
    service_data = {
        'service-type': request.form['service-type'],
        'repair-required': request.form['repair-required'],
        'repairing-note': request.form['repairing-note'],
        'repairing-cost': request.form['repairing-cost'],
        'gas-filling': request.form['gas-filling'],
        'gas-filling-cost': request.form['gas-filling-cost'],
        'service-cost': request.form['service-cost'],
        'total-cost': request.form['total-cost'],
        'createdon': datetime.datetime.today(),
        'customer_name': request.form['customer_name'],
        'customer_email': request.form['customer_email'],
        'next-service': request.form['next-service'],
        'ac_id': request.form['ac_id'],
        'ac category': request.form['ac category'],
        'ac brand': request.form['ac brand'],
        'customer_id': request.form['customer_id'],
        'mechanic_id': session['mechanic_id']
    }

    if len(service_data['service-type']) == 0 or len(service_data['repair-required']) == 0:
        return render_template('error2.html', message=" Form Fields Cannot Be Empty")

    print(service_data)
    db = MongoDBHelper(collection="services")
    db.insert(service_data)

    return render_template('success2.html', message=" Service for AC {} added successfully.."
                           .format(service_data['ac brand']))


@web_app.route("/view-services/<id>")
def fetch_services_of_customer_acs(id):
    db = MongoDBHelper(collection="acs")
    query = {'_id': ObjectId(id)}
    ac = db.fetch(query)[0]

    db = MongoDBHelper(collection="services")
    query = {'mechanic_id': session['mechanic_id'], 'customer_id': ac['customer_id'], 'ac_id': str(ac['_id'])}
    print("[DEBUG] QUERY:", query)
    documents = db.fetch(query)
    print(documents, type(documents))
    # return "Customers Fetched for the Vet {}".format(session['vet_name'])
    return render_template('services-ac.html',
                           email=session['mechanic_email'],
                           name=session['mechanic_name'],
                           ac=ac,
                           documents=documents)


@web_app.route("/delete-service/<id>")
def delete_service(id):
    db = MongoDBHelper(collection="services")
    query = {'_id': ObjectId(id)}
    service = db.fetch(query)[0]
    db.delete(query)
    return render_template('success2.html', message="Service {} Deleted".format(service['_id']))


@web_app.route("/update-services/<id>")
def update_services(id):
    db = MongoDBHelper(collection="services")
    query = {'_id': ObjectId(id)}
    service = db.fetch(query)[0]
    return render_template('update-service.html', email=session['mechanic_email'],
                           name=session['mechanic_name'], service=service)


@web_app.route("/update-service-db", methods=['POST'])
def update_service_in_db():
    service_data_to_update = {
        'service-type': request.form['service-type'],
        'repair-required': request.form['repair-required'],
        'repairing-note': request.form['repairing-note'],
        'repairing-cost': request.form['repairing-cost'],
        'gas-filling': request.form['gas-filling'],
        'gas-filling-cost': request.form['gas-filling-cost'],
        'service-cost': request.form['service-cost'],
        'total-cost': request.form['total-cost'],
        'createdon': datetime.datetime.today(),
        'next-service': request.form['next-service'],
    }

    if len(service_data_to_update['service-type']) == 0 or len(service_data_to_update['next-service']) == 0:
        return render_template('error2.html', message="Form Fields Cannot Be Empty")

    print(service_data_to_update)
    db = MongoDBHelper(collection="services")
    query = {'_id': ObjectId(request.form['sid'])}
    db.update(service_data_to_update, query)
    return render_template('success2.html',
                           message="Service {} updated successfully ".format(service_data_to_update['service-type']))

""""#service ends------------------------"""

"""#start fetch all info-----------------"""

@web_app.route("/fetch-all-information")
def fetch_all_information():
    customer_db = MongoDBHelper(collection="customer")
    acs_db = MongoDBHelper(collection="acs")
    services_db = MongoDBHelper(collection="services")

    customer_query = {'mechanic_id': session['mechanic_id']}
    acs_query = {'mechanic_id': session['mechanic_id']}
    services_query = {'mechanic_id': session['mechanic_id']}

    customer_documents = customer_db.fetch(customer_query)
    acs_documents = acs_db.fetch(acs_query)
    services_documents = list(services_db.fetch(services_query))

    # Create a dictionary to store the ACs and services for each customer
    customer_info = {}

    # Iterate through customer documents
    for customer in customer_documents:
        customer_id = str(customer['_id'])
        # Filter ACs for the current customer
        customer_acs = [ac for ac in acs_documents if ac['customer_id'] == customer_id]
        acs_info = []

        # Iterate through ACs for the current customer
        for ac in customer_acs:
            ac_id = str(ac['_id'])
            # Filter services for the current AC
            ac_services = [service for service in services_documents if service['ac_id'] == ac_id]
            ac_info = {
                'ac_details': {
                    'ac category': ac['ac category'],
                    'ac brand': ac['ac brand'],

                },
                'services': [
                    {
                        'service-type': service['service-type'],
                        'repair-required': service['repair-required'],
                        'repairing-note': service['repairing-note'],
                        'repairing-cost': service['repairing-cost'],
                        'gas-filling': service['gas-filling'],
                        'gas-filling-cost': service['gas-filling-cost'],
                        'service-cost': service['service-cost'],
                        'total-cost': service['total-cost'],
                        'createdon': service['createdon'],
                        'next-service': service['next-service'],
                    }
                    for service in ac_services
                ]
            }
            acs_info.append(ac_info)

        # Store customer information
        customer_info[customer_id] = {
            'customer_details': {
                'name': customer['name'],
                'phone': customer['phone'],
                'email': customer['email'],
                'address': customer['address'],

            },
            'acs_info': acs_info
        }

    return render_template('all_information2.html',
                           email=session['mechanic_email'],
                           name=session['mechanic_name'],
                           customer_info=customer_info)

"""ends all info----------------------"""

"""customer login and info start---------"""

@web_app.route("/customer-login")
def customer_login():
    return render_template('loginn.html')

@web_app.route("/home3")
def home1():
    return render_template('home3.html')

@web_app.route("/login-customer", methods=['POST'])
def login_customer():
    customer_data = {
        'email': request.form['email']
    }
    if len(customer_data['email']) == 0:
        return render_template('error.html', message="Email is missing...")

    db = MongoDBHelper(collection="customer")
    documents = list(db.fetch({'email': customer_data['email']}))

    if len(documents) == 1:
        # Assuming the login is successful if the email exists in the database
        session['customer_id'] = str(documents[0]['_id'])
        session['customer_email'] = documents[0]['email']
        session['customer_name'] = documents[0]['name']
        return render_template('home3.html', email=session['customer_email'], name=session['customer_name'])

        # Fetch and display service records for the customer
        #return fetch_services_of_customer(session['customer_id'])

    return render_template('error1.html', message="Invalid email")


@web_app.route("/view-ac-and-services/<customer_id>")
def fetch_services_of_customer(customer_id):
    db_acs = MongoDBHelper(collection="acs")
    acs_query = {'customer_id': customer_id}
    acs_documents = list(db_acs.fetch(acs_query))

    db_services = MongoDBHelper(collection="services")
    services_query = {'customer_id': customer_id}
    services_documents = list(db_services.fetch(services_query))

    customer_data = {
        'name': session.get('customer_name'),
        'documents': acs_documents + services_documents
    }

    return render_template('customer_services.html', customer=customer_data)

"""customer login and info ends---------"""

"""search by date starts------------"""

@web_app.route("/search-by-single-date")
def search_by_single_date():
    return render_template('service-date.html')

@web_app.route("/search-services-by-single-date", methods=['POST'])
def search_services_by_single_date():
    try:
        search_date = request.form['next-service']
        # Validate date format
        datetime.datetime.strptime(search_date, '%Y-%m-%d')

    except ValueError:
        return render_template('error2.html', message="Invalid date format. Use YYYY-MM-DD.")

    db = MongoDBHelper(collection="services")
    query = {
        'createdon': datetime.datetime.strptime(search_date, '%Y-%m-%d'),
        'mechanic_id': session.get('mechanic_id')
    }
    services = list(db.fetch(query))

    if services:
        return render_template('service-date.html', services=services)
    else:
        return render_template('error2.html', message="No services found for the provided date.")

"""search by date ends------------"""

"""rate application starts----------"""
@web_app.route('/rate')
def index1():
    # Render the HTML file
    return render_template('ratings.html')
def rate_application(application_info):
    # Calculate the total score based on weighted average
    total_score = (int(application_info.get('Functionality', 0)) * 0.2 +
                   int(application_info.get('Performance', 0)) * 0.15 +
                   int(application_info.get('Compatibility', 0)) * 0.1 +
                   int(application_info.get('Security', 0)) * 0.1 +
                   int(application_info.get('Updates_and_Support', 0)) * 0.1 +
                   int(application_info.get('User_Feedback', 0)) * 0.1 +
                   int(application_info.get('Innovation_and_Uniqueness', 0)) * 0.1 +
                   int(application_info.get('Value_for_Money', 0)) * 0.1 +
                   int(application_info.get('Community_and_Social_Proof', 0)) * 0.05 +
                   int(application_info.get('Longevity_and_Sustainability', 0)) * 0.05)

    # Determine rating label based on total score
    if total_score >= 8:
        rating_label = "Excellent"
    elif total_score >= 6:
        rating_label = "Good"
    else:
        rating_label = "Average"

    return total_score, rating_label

@web_app.route('/rate_application', methods=['POST'])
def rate_application_route():
    # Receive application information from the request form
    application_info = request.form

    # Rate the application
    total_score, rating_label = rate_application(application_info)

    # Return the total score and rating label as JSON response
    return jsonify({'total_score': total_score, 'rating_label': rating_label})

"""rate application ends----------"""



def main():
    # In order to use session object in flask, we need to set some key as secret_key in app
    web_app.secret_key = 'Ac-key-1'
    web_app.run()
    # web_app.run(port=5001)


if __name__ == "__main__":
    main()


