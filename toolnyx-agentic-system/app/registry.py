from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class ToolDefinition:
    name: str
    domain: str
    action: str
    description: str
    keywords: List[str]
    risk: str = "low"

TOOL_CATALOG = [
    ToolDefinition("paypal.invoice.create", "paypal.invoice", "create", "Create an invoice for a customer.", ["create", "invoice", "bill", "billing", "charge"], "medium"),
    ToolDefinition("paypal.invoice.send", "paypal.invoice", "send", "Send an existing invoice to a customer.", ["send", "invoice", "email", "deliver"], "medium"),
    ToolDefinition("paypal.report.sales", "paypal.report", "sales", "Retrieve sales volume for a requested period.", ["sales", "revenue", "volume", "report", "sold"]),
    ToolDefinition("paypal.dispute.search", "paypal.dispute", "search", "Search disputes associated with a customer.", ["dispute", "complaint", "case", "customer"]),
    ToolDefinition("knowledge.search", "knowledge", "search", "Search the product and process knowledge base.", ["how", "what", "explain", "documentation", "knowledge"]),
    ToolDefinition("system.capabilities", "system", "capabilities", "Find available system capabilities and tools.", ["tools", "capabilities", "available", "system"]),
    ToolDefinition("system.status", "system", "status", "Check the status of the most recent request.", ["status", "request", "last", "recent"]),
]

class ToolRegistry:
    def __init__(self, catalog=None):
        self.catalog = catalog or TOOL_CATALOG

    def all(self):
        return self.catalog

    def find(self, name):
        return next((tool for tool in self.catalog if tool.name == name), None)

    def search(self, text, limit=4):
        lower = text.lower()
        words = set(lower.split())
        scored = []
        for tool in self.catalog:
            score = sum(2 for keyword in tool.keywords if keyword in lower)
            score += sum(1 for word in words if word in tool.description.lower())
            if score:
                scored.append((score, tool))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [tool for _, tool in scored[:limit]]
