# ContosoPay Customer Support Triage Workflow

A Microsoft Foundry workflow project that demonstrates how AI agents, workflow
variables, loops, confidence checks, category routing, and a Python client can
work together to automate customer-support triage.

The workflow processes fictional ContosoPay support tickets, classifies each
ticket as **Billing**, **Technical**, or **General**, evaluates classification
confidence, escalates billing issues to human support, and uses a second AI
agent to draft responses for eligible tickets.

## GitHub Description

> Microsoft Foundry AI workflow for customer-support triage using multiple agents, conditional routing, confidence handling, and Python SDK integration.

## What This Project Demonstrates

- Microsoft Foundry workflow builder
- Multi-agent orchestration
- Structured JSON agent output
- For-each loops
- Workflow variables
- Confidence-based conditional logic
- Category-based routing
- Human escalation for billing issues
- AI-generated support responses
- Azure AI Projects SDK integration
- Streaming workflow execution
- Conversation cleanup

## Architecture

```text
Support Ticket Array
        |
        v
    For Each
        |
        v
   Triage-Agent
        |
        v
Confidence > 0.6?
   /             \
 No               Yes
 |                 |
 v                 v
Ask for        Billing?
more info      /     \
             Yes      No
              |        |
              v        v
          Escalate  Resolution-Agent
          to Human       |
                         v
                 Recommended Response
```

## Repository Structure

```text
azure-foundry-customer-support-workflow/
│
├── workflow.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── docs/
│   └── workflow-configuration.md
│
└── outputs/
    └── screenshots/
        ├── README.md
        ├── 01-workflow-overview.png
        ├── 02-support-tickets-variable.png
        ├── 03-triage-agent.png
        ├── 04-confidence-condition.png
        ├── 05-category-routing.png
        ├── 06-resolution-agent.png
        ├── 07-workflow-preview.png
        └── 08-vscode-terminal-output.png
```

## Prerequisites

- Azure subscription
- Microsoft Foundry access
- Visual Studio Code
- Python 3.13
- Git
- Azure CLI

## 1. Create the Foundry Workflow

In Microsoft Foundry:

1. Open **Build > Agents > Workflows**.
2. Select **Create > Blank workflow**.
3. Save the workflow as:

```text
ContosoPay-Customer-Support-Triage
```

The full node-by-node configuration is in:

```text
docs/workflow-configuration.md
```

## 2. Sample Tickets

```json
[
  "The API returns a 403 error when creating invoices, but our API key hasn't changed.",
  "Is there a way to export all invoices as a CSV?",
  "I was charged twice for the same invoice last Friday and my customer is also seeing two receipts. Can someone fix this?"
]
```

Expected classifications are approximately:

| Ticket | Expected category |
|---|---|
| API 403 during invoice creation | Technical |
| Export invoices as CSV | General |
| Duplicate charge | Billing |

Exact model wording and confidence values can vary.

## 3. Open the Project in VS Code

Extract this repository and open the folder:

```text
azure-foundry-customer-support-workflow
```

## 4. Create a Virtual Environment

PowerShell:

```powershell
python -m venv labenv
.\labenv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\labenv\Scripts\Activate.ps1
```

## 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

Dependencies:

```text
python-dotenv
azure-identity
azure-ai-projects==2.0.0b4
aiohttp
```

## 6. Configure Environment Variables

Create `.env`:

```powershell
Copy-Item .env.example .env
```

Then edit:

```env
PROJECT_ENDPOINT=https://YOUR-FOUNDRY-RESOURCE.services.ai.azure.com/api/projects/YOUR-PROJECT
WORKFLOW_NAME=ContosoPay-Customer-Support-Triage
```

Copy the real project endpoint from the **Code > .env variables** area of your
Microsoft Foundry workflow.

Never commit the real `.env` file.

## 7. Sign In to Azure

```powershell
az login
```

## 8. Run the Client

```powershell
python workflow.py
```

The client:

1. authenticates with Azure
2. connects to the Foundry project
3. creates a conversation
4. invokes the saved workflow
5. streams events
6. retrieves the completed output
7. formats ticket results
8. deletes the temporary conversation

## 9. Output Screenshots

Store GitHub evidence in:

```text
outputs/screenshots/
```

Recommended filenames:

```text
01-workflow-overview.png
02-support-tickets-variable.png
03-triage-agent.png
04-confidence-condition.png
05-category-routing.png
06-resolution-agent.png
07-workflow-preview.png
08-vscode-terminal-output.png
```

### Workflow Overview

![Workflow Overview](outputs/screenshots/01-workflow-overview.png)

### Support Tickets Variable

![Support Tickets Variable](outputs/screenshots/02-support-tickets-variable.png)

### Triage Agent

![Triage Agent](outputs/screenshots/03-triage-agent.png)

### Confidence Condition

![Confidence Condition](outputs/screenshots/04-confidence-condition.png)

### Category Routing

![Category Routing](outputs/screenshots/05-category-routing.png)

### Resolution Agent

![Resolution Agent](outputs/screenshots/06-resolution-agent.png)

### Workflow Preview

![Workflow Preview](outputs/screenshots/07-workflow-preview.png)

### VS Code Terminal Output

![VS Code Terminal Output](outputs/screenshots/08-vscode-terminal-output.png)

GitHub will show broken image placeholders until screenshots with these exact
names are added.

## 10. Push to GitHub

Create an **empty** GitHub repository first.

Then run from the VS Code terminal:

```powershell
git init
git add .
git commit -m "Initial commit: Microsoft Foundry customer support workflow"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

After adding screenshots later:

```powershell
git add outputs/screenshots/
git commit -m "Add workflow output screenshots"
git push
```

## Security

Do not commit:

- `.env`
- API keys
- access tokens
- Azure credentials
- screenshots containing secrets

The included `.gitignore` excludes `.env`.

## Troubleshooting

### `PROJECT_ENDPOINT is missing`

Create `.env` from `.env.example` and add your actual Foundry project endpoint.

### Authentication error

Run:

```powershell
az login
```

and verify that the selected Azure account can access the Foundry project.

### Workflow not found

Make sure the workflow name in `.env` exactly matches the saved workflow name.

### Output formatting looks unusual

Microsoft Foundry workflows are a preview feature. The client falls back to
printing raw workflow output if the response does not match the expected ticket
format.

## What I Learned

This project demonstrates how visual workflow orchestration can combine
specialized AI agents with deterministic application logic. The Triage Agent
handles classification, while workflow conditions control uncertainty and
escalation, and the Resolution Agent generates customer-facing responses.

The Python client shows how a saved Microsoft Foundry workflow can be invoked
programmatically through the Azure AI Projects SDK.

## Technologies

- Microsoft Foundry
- Microsoft Foundry Workflows
- Azure AI Projects SDK
- Azure Identity
- Python
- Visual Studio Code
- Azure CLI
- Git
- GitHub

## Reference

Based on the Microsoft Learn **Develop AI Agents in Azure** exercise:
**Build a workflow in Microsoft Foundry**.

This repository reorganizes the exercise as a standalone portfolio project and
adds a completed Python client, documentation, security configuration, and a
GitHub screenshot structure.
