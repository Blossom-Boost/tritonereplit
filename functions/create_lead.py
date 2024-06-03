import logging

import modules.agendor_module

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


def create_lead_reference():
    tool_name = "create_lead"
    tool_description = "After collecting the data, save using this function"

    # Example of properties ((name of property, type, description, required True or False))
    properties = (("name", "string", "Full name of the lead user",
                   True), ("phone", "string",
                           "Lead phone number, including the local code (Phone has to be an Brazilian Phone with local code, between 10 to 11 digits (2 for local code)) and only digits", True),
                  ("email", "string", "Email address of the lead user", True))

    return tool_name, tool_description, properties, create_lead


def create_lead(tool_request):
    logger.info("Saving new client on Agendor...")
    logger.info(tool_request)

    agendor_client = modules.agendor_module.AgendorModule()
    agendor_client.save_new_client(tool_request.get("name"), tool_request.get("email"), tool_request.get("phone"))

    return True, "Daora"
