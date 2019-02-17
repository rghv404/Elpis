import uuid


class Case:
    def __init__(self, name="", location="", problem_description=""):
        self.id = uuid.uuid4().__str__()
        self.name = name
        self.location = location
        self.severity_score = 0
        self.problem_description = problem_description
        return None
