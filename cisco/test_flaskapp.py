import pytest
from cisco.sales_analytics import app, sales_transactions, product_sales

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset state before each test
        sales_transactions.clear()
        product_sales.clear()
        yield client
#copilot
def test_add_transaction(client):
    response = client.post('/transactions', json={"product": "Product A", "amount": 100})
    assert response.status_code == 201
    assert response.get_json()["message"] == "Transaction added"

def test_add_transaction_invalid_data(client):
    response = client.post('/transactions', json={"product": "Product A"})
    assert response.status_code == 400
    assert response.get_json()["message"] == "amount is required"

def test_get_transactions(client):
    client.post('/transactions', json={"product": "Product A", "amount": 100})
    response = client.get('/transactions')
    assert response.status_code == 200
    assert len(response.get_json()) > 0

def test_calculate_total_sales(client):
    client.post('/transactions', json={"product": "Product A", "amount": 100})
    client.post('/transactions', json={"product": "Product B", "amount": 200})
    response = client.get('/sales/total')
    assert response.status_code == 200
    assert response.get_json()["Product A"] == 100
    assert response.get_json()["Product B"] == 200

def test_calculate_top_customers(client):
    client.post('/transactions', json={"product": "Product A", "amount": 100, "customer": "Customer 1"})
    client.post('/transactions', json={"product": "Product B", "amount": 200, "customer": "Customer 2"})
    client.post('/transactions', json={"product": "Product C", "amount": 300, "customer": "Customer 1"})
    response = client.get('/customers/top')
    assert response.status_code == 200
    top_customers = response.get_json()
    assert len(top_customers) == 2
    assert top_customers[0][0] == "Customer 1"
    assert top_customers[0][1] == 400
    assert top_customers[1][0] == "Customer 2"
    assert top_customers[1][1] == 200

def test_filter_transactions(client):
    client.post('/transactions', json={"product": "Product A", "amount": 100})
    client.post('/transactions', json={"product": "Product B", "amount": 200})
    response = client.get('/transactions/filter?product=Product A')
    assert response.status_code == 200
    filtered_transactions = response.get_json()
    assert len(filtered_transactions) == 1
    assert filtered_transactions[0]["product"] == "Product A"