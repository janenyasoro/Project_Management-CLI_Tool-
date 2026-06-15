from datetime import datetime

class Task:
    def __init__(self, task_id, title, project_id, contributors=None, completed=False):
        self.id = task_id
        self.title = title
        self.project_id = project_id
        self.contributors = contributors if contributors else []  # list of user IDs
        self.completed = completed
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "contributors": self.contributors,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["id"],
            data["title"],
            data["project_id"],
            data.get("contributors", []),
            data.get("completed", False),
        )

    def mark_complete(self):
        self.completed = True

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"