"""
The parent System representation in the ECS model. Takes in a variable number of required Components.
Has a function to test that an Entity has the required Components

author: lou3797
version: 10_13_2018
since:
"""


"""
A System
"""
class System:
    def __init__(self, *required_component_ids):
        self.required_component_ids = required_component_ids

    """
    Checks if the given Entity has the components required by the System.
    Returns True or False depending on the Entity's Components
    """
    def has_required_components(self, entity):
        for component in self.required_component_ids:
            if not entity.get_component(component):
                return False
        return True

"""
An ObservingSystem
"""
class ObserverSystem(System):
    def __init__(self, *required_component_ids):
        super().__init__(*required_component_ids)
        self.subjects = []

    def update_all(self):
        for subject in self.subjects:
            self.update(subject)

    def update(self, subject):
        if not self.has_required_components(subject):
            self.subjects.remove(subject)
            subject.detach(self)

    def attach_one(self, subject):
        if self.has_required_components(subject):
            if subject not in self.subjects:
                self.subjects.append(subject)
                subject.attach(self)
                return True
        return False

    def attach_multiple(self, subjects):
        for subject in subjects:
            self.attach_one(subject)