"""
A wrapper of Components. Takes in a dictionary of components in the form of {Component.TYPE: Type(srgs)}
Has functions for adding, removing, and accessing components.
"""
class Entity:
    def __init__(self, name, components):
        self.name = name
        self.components = components # A dictionary of components, {Component.AI: AI()}
        self.observers = []
        # self.set_components_owner()

    def set_components_owner(self):
        for id, comp in self.components.items():
            comp.owner = self

    def get_component(self, component_id):
        return self.components.get(component_id)

    def add_component(self, component_id, component):
        self.components[component_id] = component

    def remove_component(self, component_id):
        return self.components.pop(component_id, None)

    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        print("Can't detach observers from entities yet")

    def update(self):
        for observer in self.observers:
            observer.update(self)
