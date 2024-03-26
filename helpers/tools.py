import functions.create_lead

class Tools:
    registered = []
    registered_callers = {}

    def __init__(self):
        self.register_tools()

    def register_tools(self):
        default = {
            "type": "retrieval"
        }

        self.registered.append(default)

        # Include all functions to register below
        self.register_function(functions.create_lead.create_lead_reference())

    def register_function_tool_reference(self, name, description, parameters, caller_function):
        tool_reference = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }

        self.registered.append(tool_reference)
        self.registered_callers[name] = caller_function


    @staticmethod
    def generate_parameters_by_object(properties: tuple) -> object:
        properties_dict = {}
        required_properties = []

        for property_details in properties:
            properties_dict[property_details[0]] = {
                "type": property_details[1],
                "description": property_details[2]
            }

            if property_details[3] is True:
                required_properties.append(property_details[0])

        parameters = {
            "type": "object",
            "properties": properties_dict,
            "required": required_properties
        }

        return parameters

    # To create a new tool, use the example below and add the call in the __init__ function above
    def register_function(self, function_reference: tuple):
        name, description, properties, caller_function = function_reference

        self.register_function_tool_reference(
            name=name,
            description=description,
            parameters=self.generate_parameters_by_object(properties=properties),
            caller_function=caller_function
        )

        print(f"[TOOL FUNCTION][FUNCTION {name}] Tool function registered and available to be used")
