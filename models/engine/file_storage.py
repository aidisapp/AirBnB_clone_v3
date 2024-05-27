#!/usr/bin/python3
"""
Handles I/O, writing, and reading of
JSON for storage of all class instances.
"""
import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """Manages long-term storage of all class instances using JSON format."""

    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    __file_path = './dev/file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects or all objects
        of a specific class.
        :param cls: (Optional) Class name as a string
        :return: Dictionary of objects with keys formatted as
        <class name>.<object id>
        """
        if cls:
            objects_dict = {}
            for class_id, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    objects_dict[class_id] = obj
            return objects_dict
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds or updates an object in the storage dictionary.
        :param obj: The object to be added or updated in the storage
        """
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def get(self, cls, id):
        """
        Retrieves a specific object by class name and ID.
        :param cls: Class name as a string
        :param id: Object ID as a string
        :return: The found object or None if not found
        """
        all_class = self.all(cls)
        for obj in all_class.values():
            if id == str(obj.id):
                return obj
        return None

    def count(self, cls=None):
        """
        Counts the number of instances of a specified class.
        If no class is specified, counts instances of all classes.
        :param cls: (Optional) Class name as a string
        :return: Number of instances of the specified class
        """
        return len(self.all(cls))

    def save(self):
        """
        Serializes the storage dictionary to a JSON file.
        :param __file_path: Path to the JSON file
        """
        fname = FileStorage.__file_path
        d = {}
        for bm_id, bm_obj in FileStorage.__objects.items():
            d[bm_id] = bm_obj.to_json()
        with open(fname, mode='w+', encoding='utf-8') as f_io:
            json.dump(d, f_io)

    def reload(self):
        """
        Deserializes the JSON file to the storage dictionary,
        if the file exists.
        """
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except FileNotFoundError:
            return
        for o_id, d in new_objs.items():
            k_cls = d['__class__']
            d.pop("__class__", None)
            d["created_at"] = datetime.strptime(
                d["created_at"], "%Y-%m-%d %H:%M:%S.%f")
            d["updated_at"] = datetime.strptime(
                d["updated_at"], "%Y-%m-%d %H:%M:%S.%f")
            FileStorage.__objects[o_id] = FileStorage.CNC[k_cls](**d)

    def delete(self, obj=None):
        """
        Deletes an object from the storage dictionary if it is not None.
        :param obj: The object to be deleted
        """
        if obj is None:
            return
        for k in list(FileStorage.__objects.keys()):
            if obj.id == k.split(".")[1] and k.split(".")[0] in str(obj):
                FileStorage.__objects.pop(k, None)
                self.save()

    def close(self):
        """
        Calls the reload() method for deserialization from JSON to objects.
        """
        self.reload()
