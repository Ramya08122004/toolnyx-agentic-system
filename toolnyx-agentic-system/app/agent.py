import re

from .registry import ToolRegistry
from .tools import TOOL_FUNCTIONS
from .validators import validate_parameters


class Agent:
    def __init__(self):
        self.registry = ToolRegistry()
        self.history = []

    def _detect_domain(self, text):
        text = text.lower()

        # Knowledge questions should be checked first
        # so phrases like "Explain how invoices work"
        # go to the knowledge tool instead of PayPal invoice tools.
        if any(w in text for w in [
            "explain", "how does", "how do", "documentation",
            "what is", "what are", "knowledge"
        ]):
            return "knowledge"

        if any(w in text for w in ["invoice", "bill", "billing"]):
            return "paypal.invoice"

        if any(w in text for w in ["sales", "revenue", "volume"]):
            return "paypal.report"

        if any(w in text for w in ["dispute", "complaint", "case"]):
            return "paypal.dispute"

        if any(w in text for w in [
            "tools", "capabilities", "available", "system"
        ]):
            return "system"

        if any(w in text for w in [
            "status", "last request", "recent request"
        ]):
            return "system"

        return "unknown"

    def _detect_action(self, text, domain):
        text = text.lower()

        if domain == "paypal.invoice":
            if any(w in text for w in ["send", "email", "deliver"]):
                return "send"
            if any(w in text for w in ["create", "bill", "billing", "charge"]):
                return "create"

        if domain == "paypal.report":
            return "sales"

        if domain == "paypal.dispute":
            return "search"

        if domain == "knowledge":
            return "search"

        if domain == "system":
            return (
                "status"
                if any(w in text for w in ["status", "last request", "recent"])
                else "capabilities"
            )

        return None

    def _customer(self, text):
        m = re.search(r"\buser[_ -]?(\d+)\b", text, re.I)
        return f"user_{m.group(1)}" if m else None

    def _amount(self, text):
        m = re.search(
            r"\$\s*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)\s*(?:dollars|usd)",
            text,
            re.I,
        )
        return float(m.group(1) or m.group(2)) if m else None

    def _email(self, text):
        m = re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text,
        )
        return m.group(0) if m else None

    def _period(self, text):
        lower = text.lower()

        if "last month" in lower:
            return "last_month"

        if "this month" in lower:
            return "this_month"

        if "last week" in lower:
            return "last_week"

        return "requested_period"

    def _parameters(self, tool, text):
        if tool == "paypal.invoice.create":
            return {
                "customer_id": self._customer(text),
                "amount": self._amount(text),
            }

        if tool == "paypal.invoice.send":
            return {
                "email": self._email(text),
            }

        if tool == "paypal.report.sales":
            return {
                "period": self._period(text),
            }

        if tool == "paypal.dispute.search":
            return {
                "customer_id": self._customer(text),
            }

        return {
            "query": text
        }

    def _select(self, text):
        domain = self._detect_domain(text)
        action = self._detect_action(text, domain)

        candidates = self.registry.search(text)

        exact = [
            t for t in candidates
            if t.domain == domain and t.action == action
        ]

        if exact:
            return exact[0], candidates

        domain_matches = [
            t for t in self.registry.all()
            if t.domain == domain
        ]

        return (
            domain_matches[0] if domain_matches else None
        ), candidates

    def run(self, message):
        if not message or not message.strip():
            return {
                "status": "error",
                "message": "Request message cannot be empty.",
            }

        text = message.strip()

        tool, candidates = self._select(text)

        if not tool:
            return {
                "status": "error",
                "message": "No suitable tool found.",
                "candidates": [t.name for t in candidates],
            }

        params = self._parameters(tool.name, text)

        valid, error = validate_parameters(tool.name, params)

        if not valid:
            return {
                "status": "error",
                "tool": tool.name,
                "parameters": params,
                "message": error,
            }

        try:
            result = TOOL_FUNCTIONS[tool.name](**params)

            response = {
                "status": "success",
                "tool": tool.name,
                "domain": tool.domain,
                "action": tool.action,
                "parameters": params,
                "candidates": [t.name for t in candidates],
                "result": result,
            }

            self.history.append(response)

            return response

        except Exception as exc:
            return {
                "status": "error",
                "tool": tool.name,
                "message": str(exc),
            }