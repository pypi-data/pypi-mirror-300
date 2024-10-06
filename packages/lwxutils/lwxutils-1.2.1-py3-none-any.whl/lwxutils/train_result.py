import json
import os


class TrainingResultItem:
    def __init__(self, key, value, description):
        self.key = key
        self.value = value
        self.description = description

    def __repr__(self):
        return f"Item(key={self.key}, value='{self.value}', description={self.description})"


class TrainingResult:

    def __init__(self, rootPath=".", fileName="results.json"):
        self.objects = []
        self.resultPath = os.path.join(rootPath, fileName)

    def add(self, obj: TrainingResultItem):
        self.objects.append(obj)

    def save(self):
        object_list = [
            {"key": obj.key, "value": obj.value, "description": obj.description}
            for obj in self.objects
        ]

        with open(self.resultPath, "w") as file:
            json.dump(object_list, file)  # , ensure_ascii=False, indent=4
