from hubmap_sdk.entity import Entity


class Collection(Entity):
    def __init__(self, instance):
        super().__init__(instance)
        for key in instance:
            setattr(self, key, instance[key])