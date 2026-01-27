class Perception:
    def extract_features(self, data: dict):
        return [
            data["study_hours"],
            data["attendance"]
        ]
