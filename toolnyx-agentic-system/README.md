# Scalable Agentic Tool System

A prototype agentic architecture designed to avoid exposing hundreds or thousands of tools directly to a reasoning model.

## Flow

User Request -> Domain Detection -> Action Detection -> Tool Registry -> Candidate Scoring -> Top-K Candidates -> Tool Selection -> Parameter Extraction -> Validation -> Execution -> Structured Response

## Tools

- paypal.invoice.create
- paypal.invoice.send
- paypal.report.sales
- paypal.dispute.search
- knowledge.search
- system.capabilities
- system.status

## Run

```bash
python -m venv .venv
pip install -r requirements.txt
python -m uvicorn app.main:app --reload