from app.agent import Agent

def test_create_invoice():
    r = Agent().run("Create an invoice for user_123 for 50 dollars")
    assert r["status"] == "success"
    assert r["tool"] == "paypal.invoice.create"
    assert r["parameters"]["customer_id"] == "user_123"
    assert r["parameters"]["amount"] == 50.0

def test_send_invoice():
    r = Agent().run("Send the invoice to customer@example.com")
    assert r["status"] == "success"
    assert r["tool"] == "paypal.invoice.send"

def test_sales_report():
    r = Agent().run("What was my total sales volume last month?")
    assert r["status"] == "success"
    assert r["tool"] == "paypal.report.sales"

def test_dispute():
    r = Agent().run("Is there a dispute open from user_123?")
    assert r["status"] == "success"
    assert r["tool"] == "paypal.dispute.search"

def test_knowledge():
    r = Agent().run("Explain how invoices work")
    assert r["status"] == "success"
    assert r["tool"] == "knowledge.search"

def test_system():
    r = Agent().run("What tools are available?")
    assert r["status"] == "success"
    assert r["tool"] == "system.capabilities"

def test_invalid_invoice():
    r = Agent().run("Create an invoice for user_123")
    assert r["status"] == "error"
    assert "amount" in r["message"]

def test_empty_request():
    r = Agent().run("")
    assert r["status"] == "error"
