import logging

import modules.agendor_module

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
    logger.info("Saving new client on Agendor...");
    logger.info(tool_request)

    agendor_client = modules.agendor_module.AgendorModule()
    agendor_client.save_new_client(tool_request.get("name"), tool_request.get("email"), tool_request.get("phone"))

    return True, "Daora"
