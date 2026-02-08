from flask import Flask, request, jsonify
import heapq

app = Flask(__name__)

# In-memory storage for sales transactions
sales_transactions = []

# Dictionary to store precomputed total sales per product
product_sales = {}

# Update product sales when a transaction is added, updated, or deleted
def update_product_sales(transaction, operation):
    product = transaction['product']
    amount = transaction['amount']

    if operation == 'add':
        product_sales[product] = product_sales.get(product, 0) + amount
    elif operation == 'update':
        old_amount = transaction['old_amount']
        product_sales[product] = product_sales.get(product, 0) - old_amount + amount
    elif operation == 'delete':
        product_sales[product] -= amount
        if product_sales[product] <= 0:
            del product_sales[product]

# Refactored helper function to validate transaction data
def validate_transaction_data(data, required_fields):
    if not data:
        return False, "Request body must be JSON"
    for field in required_fields:
        if field not in data:
            return False, f"{field} is required"
    return True, None

# Endpoint 1: CRUD operations for transactions
@app.route('/transactions', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_transactions():
    if request.method == 'POST':
        data = request.get_json()
        is_valid, error_message = validate_transaction_data(data, ['product', 'amount'])
        if not is_valid:
            return jsonify({"message": error_message}), 400
        sales_transactions.append(data)
        update_product_sales(data, 'add')
        return jsonify({"message": "Transaction added", "transaction": data}), 201

    elif request.method == 'GET':
        return jsonify(sales_transactions), 200

    elif request.method == 'PUT':
        data = request.get_json()
        is_valid, error_message = validate_transaction_data(data, ['id', 'product', 'amount'])
        if not is_valid:
            return jsonify({"message": error_message}), 400
        for transaction in sales_transactions:
            if transaction['id'] == data['id']:
                old_amount = transaction['amount']
                transaction.update(data)
                transaction['old_amount'] = old_amount
                update_product_sales(transaction, 'update')
                return jsonify({"message": "Transaction updated", "transaction": transaction}), 200
        return jsonify({"message": "Transaction not found"}), 404

    elif request.method == 'DELETE':
        data = request.get_json()
        is_valid, error_message = validate_transaction_data(data, ['id'])
        if not is_valid:
            return jsonify({"message": error_message}), 400
        for transaction in sales_transactions:
            if transaction['id'] == data['id']:
                sales_transactions.remove(transaction)
                update_product_sales(transaction, 'delete')
                return jsonify({"message": "Transaction deleted"}), 200
        return jsonify({"message": "Transaction not found"}), 404

# Endpoint 2: Calculate total sales per product
@app.route('/sales/total', methods=['GET'])
def calculate_total_sales():
    return jsonify(product_sales), 200

# Endpoint 3: Calculate top customers
@app.route('/customers/top', methods=['GET'])
def calculate_top_customers():
    customer_sales = {}
    for transaction in sales_transactions:
        customer = transaction.get('customer', 'Unknown')
        amount = transaction['amount']
        customer_sales[customer] = customer_sales.get(customer, 0) + amount

    # Use a heap to find the top 5 customers by sales
    top_customers = heapq.nlargest(5, customer_sales.items(), key=lambda x: x[1])
    return jsonify(top_customers), 200

# Endpoint 4: Return filtered results
@app.route('/transactions/filter', methods=['GET'])
def filter_transactions():
    product = request.args.get('product')
    filtered_transactions = [t for t in sales_transactions if t['product'] == product]
    return jsonify(filtered_transactions), 200

if __name__ == '__main__':
    app.run(debug=True)