def create_invoice(customer_id, amount):
    return {"invoice_id": "INV1001", "customer_id": customer_id, "amount": amount, "currency": "USD", "status": "created", "provider": "paypal_demo"}

def send_invoice(email):
    return {"email": email, "status": "sent", "provider": "paypal_demo"}

def sales_report(period):
    return {"period": period, "total_sales": 12500, "currency": "USD", "provider": "paypal_demo"}

def search_dispute(customer_id):
    return {"customer_id": customer_id, "dispute_found": True, "dispute_id": "DSP1001", "status": "open", "provider": "paypal_demo"}

def knowledge_search(query):
    knowledge = {
        "invoice": "An invoice is a request for payment. It normally contains a customer, amount, currency and status.",
        "payment": "A payment represents money transferred from a customer for a product or service.",
        "dispute": "A dispute is a customer case concerning a payment or transaction.",
    }
    for key, answer in knowledge.items():
        if key in query.lower():
            return {"answer": answer, "source": key}
    return {"answer": "No matching knowledge-base article was found.", "source": None}

def system_capabilities(query):
    return {"type": "capabilities", "query": query, "tools": [t for t in [
        "paypal.invoice.create", "paypal.invoice.send", "paypal.report.sales",
        "paypal.dispute.search", "knowledge.search", "system.capabilities", "system.status"
    ]]}

def system_status(query):
    return {"type": "request_status", "query": query, "status": "completed", "message": "The most recent demo request completed successfully."}

TOOL_FUNCTIONS = {
    "paypal.invoice.create": create_invoice,
    "paypal.invoice.send": send_invoice,
    "paypal.report.sales": sales_report,
    "paypal.dispute.search": search_dispute,
    "knowledge.search": knowledge_search,
    "system.capabilities": system_capabilities,
    "system.status": system_status,
}
