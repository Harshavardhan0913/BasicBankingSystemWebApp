from flask import *
from DataBase import DataBase

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return render_template("home.html")

@app.route('/all_customers')
def view_customers():
    db = DataBase()
    data = db.get_data()
    #print(data)
    final_data = []

    # for d in data:
    #     f_data = dict()
    #     f_data['customerId'] = d['customerId']
    #     f_data['Customer'] = d['customerName']
    #     f_data['Balance'] = d['balance']
    #     final_data.append(f_data)
    # print(final_data)
    # l = len(final_data)
    return render_template("AllCustomers.html", data=data, l=10)


@app.route("/view_customer")
def view_customer():
    customerId = request.args.get('customerId')
    db = DataBase()
    data = db.get_customer(customerId)
    customerDetails = data[0]
    return render_template("ViewCustomer.html",customerId=customerId,data=customerDetails)


@app.route('/transfer')
def transfer():
    customerId = int(request.args.get('customerId'))
    status = request.args.get('status')


    #print(customerId)
    db = DataBase()
    otherCustomers = db.get_other_customers(customerId)
    # for d in otherCustomers:
    #     print(d['customerName'])
    # print(otherCustomers)
    currentCustomer = db.get_customer(customerId)
    #print(otherCustomers.rowcount)
    return render_template('TransferMoney.html', currentCustomer=currentCustomer[0], otherCustomers=otherCustomers,status=status)


@app.route("/validate_transfer",methods=['POST'])
def validate_transfer():
    fromCustomerId = request.args.get('customerId')
    toCustomerId = request.form.get('TransferTo')
    transferAmount = request.form.get('transferAmount')
    # print(fromCustomerId)
    # print(transferTo)
    # print(transferAmount)
    db = DataBase()
    status = db.transfer(fromCustomerId, toCustomerId, float(transferAmount))
    #print(status)
    return redirect("/transfer?customerId="+fromCustomerId+"&status="+str(status)+"")


if __name__ == '__main__':
    app.run()
