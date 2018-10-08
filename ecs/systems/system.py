# The parent System representation in the ECS model. Takes in a variable number of required Components.
# Has a function to test that an Entity has the required Components
class System:
    def __init__(self, *required_components):
        self.required_components = required_components

    def has_required_components(self, entity):
        for component in self.required_components:
            if not entity.get_component(component):
                return False
        return True
