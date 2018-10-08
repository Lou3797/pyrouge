class Entity:
    def __init__(self, name, components):
        self.name = name
        self.components = components # A dictionary of components, {Component.AI: AI()}
        self.set_components_owner()

    def set_components_owner(self):
        for id, comp in self.components.items():
            comp.owner = self

    def get_component(self, component_id):
        return self.components.get(component_id)

    def add_component(self, component_id, component):
        self.components[component_id] = component

    def remove_component(self, component_id):
        return self.components.pop(component_id, None)

