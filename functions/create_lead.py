import os

from modules.airtable_module import AirtableModule


def create_lead_reference():
    tool_name = "create_lead"
    tool_description = "Capture lead details of the user."

    # Example of properties ((name of property, type, description, required True or False))
    properties = (
        ("name", "string", "Full name of the lead user", True),
        ("phone", "string", "Lead phone number, including country code", True),
        ("email", "string", "Email address of the lead user", True)
    )

    return (
        tool_name,
        tool_description,
        properties,
        create_lead
    )


# {"name": string, "phone": string, "email": string}
def create_lead(tool_request):
    client = AirtableModule()

    response = client.create_record("Leads", tool_request);

    return True, response
