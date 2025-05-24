def get_info(element):
    # Basic element information
    tag_name = element.tag_name
    element_id = element.get_attribute("id")
    element_class = element.get_attribute("class")
    element_type = element.get_attribute("type")
    element_text = element.text
    element_location = element.location
    element_size = element.size
    element_attributes = {}

    # Collect all attributes (this is an extra step to capture all possible attributes)
    attributes_to_check = ["href", "src", "alt", "title", "placeholder", "value", "name", "aria-label", "role"]
    for attribute in attributes_to_check:
        value = element.get_attribute(attribute)
        if value:
            element_attributes[attribute] = value

    # Prepare the info string
    info = (
        f"Tag: {tag_name}, ID: {element_id}, Class: {element_class}, Type: {element_type}, "
        f"Text: {element_text}, Location: {element_location}, Size: {element_size}, "
        f"Attributes: {element_attributes}"
    )
    
    return info

def log (action, element, *args):
    # Get all the info
    info = get_info(element)
    
    # Print the executed action with additional arguments (if any)
    if args:
        print(f"{action} on {info} with {args}")
    else:
        print(f"{action} on {info}")
