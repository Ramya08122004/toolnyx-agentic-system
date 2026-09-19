def validate_parameters(tool_name, parameters):
    if tool_name == "paypal.invoice.create":
        if not parameters.get("customer_id"):
            return False, "customer_id is required"
        if parameters.get("amount") is None:
            return False, "amount is required"
        if parameters["amount"] <= 0:
            return False, "amount must be greater than zero"
    elif tool_name == "paypal.invoice.send":
        if not parameters.get("email"):
            return False, "email is required"
    elif tool_name == "paypal.dispute.search":
        if not parameters.get("customer_id"):
            return False, "customer_id is required"
    elif tool_name == "paypal.report.sales":
        if not parameters.get("period"):
            return False, "period is required"
    elif tool_name in {"knowledge.search", "system.capabilities", "system.status"}:
        if not parameters.get("query"):
            return False, "query is required"
    return True, None
