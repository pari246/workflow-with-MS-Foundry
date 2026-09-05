import json
import os
import re

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def print_workflow_output(output_text: str) -> None:
    """Format workflow output into readable ticket sections."""
    tickets = re.findall(r"(\{.*?\})(.*?)(?=\{|$)", output_text, re.DOTALL)

    if not tickets:
        print(output_text)
        return

    for ticket_number, (ticket_json, response_text) in enumerate(tickets, start=1):
        try:
            ticket = json.loads(ticket_json)
            print("\n" + "=" * 80)
            print(
                f"Ticket {ticket_number}: "
                f"{ticket.get('category', 'Unknown')} "
                f"({ticket.get('confidence', 0):.0%} confidence)"
            )
            print("-" * 80)
            print(f"Issue: {ticket.get('customer_issue', 'Not provided')}")
            print("\nResponse:")
            print(response_text.strip() or "No additional response text returned.")
            print("=" * 80 + "\n")
        except (json.JSONDecodeError, TypeError, ValueError):
            print("\n" + "=" * 80)
            print(f"Ticket {ticket_number}")
            print("-" * 80)
            print(ticket_json)
            print(response_text.strip())
            print("=" * 80 + "\n")


def main() -> None:
    """Connect to Microsoft Foundry and invoke the saved workflow."""
    load_dotenv()

    endpoint = os.getenv("PROJECT_ENDPOINT")
    workflow_name = os.getenv(
        "WORKFLOW_NAME",
        "ContosoPay-Customer-Support-Triage",
    )

    if not endpoint:
        raise ValueError(
            "PROJECT_ENDPOINT is missing. Copy .env.example to .env and "
            "replace the placeholder with your Microsoft Foundry project endpoint."
        )

    print("Microsoft Foundry Customer Support Workflow")
    print(f"Workflow: {workflow_name}")
    print(f"Project endpoint: {endpoint}\n")

    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
        workflow = {"name": workflow_name}

        conversation = openai_client.conversations.create()
        print(f"Created conversation (id: {conversation.id})")
        print("Starting workflow...\n")

        try:
            stream = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={
                    "agent_reference": {
                        "name": workflow["name"],
                        "type": "agent_reference",
                    }
                },
                input="Start",
                stream=True,
            )

            completed = False

            for event in stream:
                event_type = getattr(event, "type", "")

                if event_type == "response.completed":
                    completed = True
                    print("\nResponse completed:")
                    response = openai_client.responses.retrieve(event.response.id)
                    print_workflow_output(response.output_text or "")

            if not completed:
                print(
                    "\nThe stream ended without a response.completed event. "
                    "Check the workflow run in Microsoft Foundry for details."
                )

        finally:
            openai_client.conversations.delete(
                conversation_id=conversation.id
            )
            print("\nConversation deleted")


if __name__ == "__main__":
    main()
