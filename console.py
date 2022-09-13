#!/usr/bin/python3
"""cmd script"""

import cmd
from curses.ascii import isdigit
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """child class of cmd class"""

    prompt = "(hbnb) "
    model_list = [
            "BaseModel",
            "User",
            "Place",
            "State",
            "City",
            "Amenity",
            "Review"
            ]

    def emptyline(self) -> bool:
        """empty line does nothing"""
        return False

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        return True

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def precmd(self, line: str) -> str:
        """Used this function to handle precommand"""

        if line.startswith('"') or line.startswith("'"):
            line = line[1:]
        if line.endswith('"') or line.endswith("'"):
            line = line[:-1]
        line = " ".join(line.split())
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2).replace("'", "")
        args = match.group(3)
        line = " ".join([method, classname, args])
        return super().precmd(line)

    def do_create(self, line):
        """Creates a new instance, saves it
        (to the JSON file) and prints the id.
        """

        line = self.parse(line)
        if HBNBCommand.error_handler(line, command="Create"):
            obj = eval(line[0])()
            obj.save()
            print(obj.id)

    def do_show(self, line):
        """Prints the string representation of an instance"""
        line = self.parse(line)
        if HBNBCommand.error_handler(line, command="Show"):
            obj = storage.all().get(f"{line[0]}.{line[1]}")
            print(obj if obj else "** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class
        name and id (save the change into the JSON file)
        """

        line = self.parse(line)
        if HBNBCommand.error_handler(line, command="Destroy"):
            if storage.all().get(f"{line[0]}.{line[1]}"):
                del storage.all()[f"{line[0]}.{line[1]}"]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        """Prints all string representation
        of all instances based or not on the class name"""
        if (not line) or line == "":
            print([str(value) for value in storage.all().values()])
        elif line not in HBNBCommand.model_list:
            print("** class doesn't exist **")
        else:
            print(
                [
                    str(value)
                    for value in storage.all().values()
                    if value.__class__.__name__ == line
                ]
            )

    def do_update(self, line):
        """Updates an instance by adding or updating attribute."""

        update_dict = re.search(r"{[^\}]*}", line)
        if update_dict:
            update_dict = eval(update_dict.group(0))
        line = self.parse(line)

        if HBNBCommand.error_handler(line, command="Update"):
            key = f"{line[0]}.{line[1]}"
            if update_dict and len(update_dict) != 0:
                opp = storage.all().get(key)
                if opp:
                    for key, val in update_dict.items():
                        setattr(opp, key, val)
                    opp.save()
                else:
                    print("** no instance found **")
            else:
                line[3] = eval(line[3]) if line[3].isdigit()\
                        or "." in line[3] else line[3]
                if storage.all().get(f"{key}"):
                    obj_to_update = storage.all()[f"{key}"]
                    setattr(obj_to_update, line[2], line[3])
                    obj_to_update.save()
                else:
                    print("** no instance found **")

    def do_count(self, line):
        """Prints out the total number of instance(in a class if specified)"""

        line = self.parse(line)
        if HBNBCommand.error_handler(line, command="Count"):
            print(
                len(
                    [
                        value
                        for value in storage.all().values()
                        if value.__class__.__name__ == line[0]
                    ]
                )
            )

    @classmethod
    def error_handler(cls, line, command=None):
        """Handles all error before passed to the command"""
        if (not line) or line[0] == "":
            print("** class name missing **")
        elif line[0] not in cls.model_list:
            print("** class doesn't exist **")
        elif command and command in ["Create", "Count"]:
            return True
        elif len(line) < 2 or line[1] == "":
            print("** instance id missing **")
        elif command and command in ["Show", "Destroy"]:
            return True
        elif len(line) < 3 or line[2] == "":
            print("** attribute name missing **")
        elif len(line) < 4 or line[3] == "":
            print("** value missing **")
        elif command and command == "Update":
            return True
        else:
            return False

    def parse(self, line):
        """splits commands"""
        line = line.replace("'", " ").replace('"', " ").replace(",", " ")
        return line.split()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
