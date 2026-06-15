class Project:
    def __init__(self, project_id, name, user_id):
        self.id = project_id
        self.name = name
        self.user_id = user_id  # owner

    def to_dict(self):
        return {"id": self.id, "name": self.name, "user_id": self.user_id}

    @staticmethod
    def from_dict(data):
        return Project(data["id"], data["name"], data["user_id"])

    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}', user_id={self.user_id})"