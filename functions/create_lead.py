import logging

import modules.airtable_module

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


def create_lead_reference():
    tool_name = "create_lead"
    tool_description = "Capture lead details of the user."

    # Example of properties ((name of property, type, description, required True or False))
    properties = (("name", "string", "Full name of the lead user",
                   True), ("phone", "string",
                           "Lead phone number, including country code", True),
                  ("email", "string", "Email address of the lead user", True))

    return tool_name, tool_description, properties, create_lead


def create_lead(tool_request):
    logger.info(tool_request)

    airtableClient = modules.airtable_module.AirtableModule()
    airtableClient.create_record("Leads", tool_request)

    return True, "Daora"
