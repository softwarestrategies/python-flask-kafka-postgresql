class ChangeProjectStatusMessage(object):
    def __init__(self, id: int):
        self.id = id

    @property
    def serialize(self):
        return {
            'id': self.id,
        }
