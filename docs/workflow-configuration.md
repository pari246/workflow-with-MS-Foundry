# Microsoft Foundry Workflow Configuration

## Workflow name

```text
ContosoPay-Customer-Support-Triage
```

## Workflow logic

```text
SupportTickets
    |
    v
For Each CurrentTicket
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
Request        Category = Billing?
more info        /          \
                Yes          No
                 |            |
                 v            v
             Escalate     Resolution-Agent
             to human          |
                               v
                       Draft support response
```

## 1. SupportTickets variable

Create a **Set variable** node.

Variable:

```text
Local.SupportTickets
```

Value:

```json
[
  "The API returns a 403 error when creating invoices, but our API key hasn't changed.",
  "Is there a way to export all invoices as a CSV?",
  "I was charged twice for the same invoice last Friday and my customer is also seeing two receipts. Can someone fix this?"
]
```

## 2. For Each

Items:

```text
Local.SupportTickets
```

Loop value variable:

```text
Local.CurrentTicket
```

## 3. Triage-Agent

Agent name:

```text
Triage-Agent
```

Instructions:

```text
Classify the user's problem description into exactly ONE category from the list below. Provide a confidence score from 0 to 1.

Billing
- Charges, refunds, duplicate payments
- Missing or incorrect payouts
- Subscription pricing or invoices being charged

Technical
- API errors, integrations, webhooks
- Platform bugs or unexpected behavior

General
- How-to questions
- Feature availability
- Data exports, reports, or UI navigation

Important rules
- Questions about exporting, viewing, or downloading invoices are General, not Billing
- Billing ONLY applies when money was charged, refunded, or paid incorrectly
```

Input:

```text
Local.CurrentTicket
```

Save output message as:

```text
Local.TriageOutputText
```

Save JSON output as:

```text
Local.TriageOutputJson
```

JSON Schema:

```json
{
  "name": "category_response",
  "schema": {
    "type": "object",
    "properties": {
      "customer_issue": {"type": "string"},
      "category": {"type": "string"},
      "confidence": {"type": "number"}
    },
    "additionalProperties": false,
    "required": ["customer_issue", "category", "confidence"]
  },
  "strict": true
}
```

## 4. Confidence condition

```text
Local.TriageOutputJson.confidence > 0.6
```

Else branch message:

```text
The support ticket classification has low confidence. Requesting more details about the issue: "{Local.CurrentTicket}"
```

## 5. Billing routing

Condition:

```text
Local.TriageOutputJson.category = "Billing"
```

Billing branch:

```text
Escalate billing issue to human support team.
```

## 6. Resolution-Agent

Agent name:

```text
Resolution-Agent
```

Instructions:

```text
You are a customer support resolution assistant for ContosoPay, a B2B payments and invoicing platform.

Your task is to draft a clear, professional, and friendly support response based on the issue category and customer message.

Guidelines:
If the issue category is Technical:
Suggest 1–2 common troubleshooting steps at a high level.

Avoid asking for logs, credentials, or sensitive data.

Do not imply fault by the customer.
If the issue category is General:
Provide a concise, helpful explanation or guidance.
Keep the response under 5 sentences.

Tone:
Professional, calm, and supportive
Clear and concise
No emojis

Output:
Return only the drafted response text.
Do not include internal reasoning or analysis.
```

Input:

```text
Local.TriageOutputText
```

Save output as:

```text
Local.ResolutionOutputText
```

## 7. Preview

Trigger:

```text
Start processing support tickets.
```
