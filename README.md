# Scalable Agentic Tool Routing System

## Purpose

This project demonstrates a scalable agentic architecture for understanding user requests, identifying the required domain and action, selecting the appropriate tool, validating parameters, and executing the selected operation.

The architecture is designed so additional tools can be registered without requiring the agent to directly reason over the complete tool catalog.

## Architecture

User Request -> Domain Detection -> Action Detection -> Tool Registry -> Candidate Scoring -> Tool Selection -> Parameter Extraction -> Validation -> Tool Execution -> Structured Result

## Main Components

### Agent

Processes the user request and coordinates the complete routing workflow.

It identifies the relevant domain, determines the requested action, selects the appropriate tool, extracts parameters, validates them, and executes the operation.

### Tool Registry

Maintains the available tools along with their metadata.

The registry provides a centralized mechanism for discovering and selecting tools based on the user's request.

### Domain Detection

Identifies the general area of the request.

Examples include:

- PayPal Invoice
- PayPal Reports
- PayPal Disputes
- Knowledge
- System

### Action Detection

Identifies the operation requested by the user.

Examples include:

- Create
- Send
- Search
- Retrieve
- Explain
- Check

### Candidate Scoring

Scores registered tools based on the detected domain, requested action, keywords, and tool metadata.

This reduces the number of tools that need to be considered for the final selection.

### Parameter Extraction

Extracts relevant parameters from the user request before executing the selected tool.

### Validation

Validates the extracted parameters before allowing tool execution.

This prevents invalid or incomplete requests from being directly passed to the execution layer.

### Tool Execution

Executes the selected registered tool and returns a structured result.

### PayPal Tools

Provides mock PayPal-style operations for demonstration purposes.

Available operations include:

- Invoice creation
- Invoice sending
- Sales report retrieval
- Dispute search

### Knowledge Search

Provides a small local knowledge-search capability for requests such as explaining concepts or retrieving knowledge.

### System Tools

Provides system-related operations such as:

- System capabilities
- System status

## Available Tools

The current prototype includes:

- `paypal.invoice.create`
- `paypal.invoice.send`
- `paypal.report.sales`
- `paypal.dispute.search`
- `knowledge.search`
- `system.capabilities`
- `system.status`

The architecture is designed so additional tools can be added to the registry without changing the overall agent workflow.

## Scalability Strategy

The system separates request understanding, tool discovery, candidate selection, validation, and execution.

For a larger tool catalog, the architecture can follow a flow such as:

1000 tools -> domain detection -> action detection -> candidate scoring -> top candidates -> parameter extraction -> validation -> selected tool

This prevents the complete tool catalog from being directly exposed to every routing decision.

The current prototype uses rule-based detection and candidate scoring. In a production system, the selection layer can later be extended with semantic embeddings, vector search, or LLM-based routing.

## Running

### Create the Environment

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
python -m pytest
```

Expected result:

```text
8 passed
```

### Run API

```bash
python -m uvicorn app.main:app --reload
```

### Swagger

```text
http://127.0.0.1:8000/docs
```

## Example Requests

```text
Create an invoice for user_123 for 50 dollars

Send invoice INV001

What was my total sales volume last month?

Is there a dispute open from user_123?

Explain how invoices work

What tools are available?

What is the current system status?
```

## Example Routing

Example request:

```text
Create an invoice for user_123 for 50 dollars
```

Processing flow:

```text
User Request
     |
     v
Domain Detection
     |
     v
PayPal Invoice
     |
     v
Action Detection
     |
     v
Create
     |
     v
Tool Registry
     |
     v
paypal.invoice.create
     |
     v
Parameter Extraction
     |
     v
Validation
     |
     v
Tool Execution
     |
     v
Structured Result
```

## Production Evolution

The prototype can later be extended with:

- Real PayPal APIs
- Embedding-based tool retrieval
- Vector database
- LLM-based structured routing
- Semantic search
- Redis or PostgreSQL state
- Authentication
- Authorization
- Rate limiting
- Audit logging
- OpenTelemetry
- Distributed tool execution
- Tool versioning
- Human approval for sensitive operations
- Retry and timeout policies

The current implementation is intentionally local and uses mock tool operations for demonstration purposes. It does not require external AI API credits or real payment credentials.

## Technology Stack

- Python
- FastAPI
- Pydantic
- Pytest
- REST API
- Tool Registry
- Rule-based Agent Routing
- Parameter Validation

## Project Structure

```text
toolnyx-agentic-system/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── agent.py
│   ├── registry.py
│   ├── tools.py
│   └── validators.py
│
├── tests/
│   ├── __init__.py
│   └── test_agent.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Project Scope

This repository is a representative prototype demonstrating scalable agentic tool-routing concepts.

The PayPal operations are mock implementations and do not perform real financial transactions.

The architecture demonstrates how a tool catalog can be organized, discovered, scored, validated, and executed through a centralized agent workflow.

## Releases

No releases published.

## Packages

No packages published.
