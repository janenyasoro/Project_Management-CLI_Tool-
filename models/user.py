class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    @staticmethod
    def from_dict(data):
        return User(data["id"], data["name"])

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}')"