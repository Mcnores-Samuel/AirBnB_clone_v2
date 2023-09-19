#!/usr/bin/python3
"""Entry point for the command interpreter and is used
manage the objects of the application.

operations that can be performed or be done with the command
interpreter are as follows:
- Create a new object (ex: a new User or a new Place)
- Retrieve an object from a file, a database etc…
- Do operations on objects (count, compute stats, etc…)
- Update attributes of an object
- Destroy an object
"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review

class_list = {
    "BaseModel": BaseModel, "User": User,
    "State": State, "City": City, "Review": Review,
    "Place": Place, "Amenity": Amenity
}


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_create(self, line):
        """Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id

        args:
            line: inputline containing the create command followed by
            the name of the class (BaseModel)
        """
        if not line:
            print("** class name missing **")
            return False
        if line in class_list:
            class_obj = class_list[line]()
            class_obj.save()
            print(class_obj.id)
        else:
            print("** class doesn't exist **")
            return False

    def do_show(self, line):
        """Prints the string representation of an instance based
        on the class name and id

        args:
            line: input line  format (show className instanceid)
        """
        if not line:
            print("** class name missing **")
            return False
        else:
            args = line.split(" ")
            if args[0] in class_list:
                if len(args) != 2:
                    print("** instance id missing **")
                    return False
                data = storage.all()
                obj = ""
                for obj_id in data.keys():
                    instance_id = obj_id.split(".")[1]
                    if args[1] == instance_id:
                        obj = data[obj_id]
                        break
                if obj:
                    print(obj)
                else:
                    print("** no instance found **")
                    return False
            else:
                print("** class doesn't exist **")
                return False

    def do_destroy(self, line):
        """ Deletes an instance based on the class name and id
        (save the change into the JSON file).
        """
        if not line:
            print("** class name missing **")
            return False
        else:
            args = line.split(" ")
            if args[0] in class_list:
                if len(args) != 2:
                    print("** instance id missing **")
                    return False
                data = storage.all()
                is_deleted = False
                for obj_id in data.keys():
                    instance_id = obj_id.split(".")[1]
                    if args[1] == instance_id:
                        del data[obj_id]
                        storage.save()
                        is_deleted = True
                        break
                if not is_deleted:
                    print("** no instance found **")
                    return False
            else:
                print("** class doesn't exist **")
                return False

    def do_all(self, line):
        """Prints all string representation of all instances based
        or not on the class name. Ex: $ all BaseModel or $ all.
        """
        args = line.split(" ")
        data = storage.all()
        result = []
        if line:
            if args[0] in class_list:
                pass
            else:
                print("** class doesn't exist **")
                return False
        for obj in data.keys():
            instance_type = obj.split(".")[0]
            if args[0] and args[0] == instance_type:
                result.append(str(data[obj]))
            if not line:
                result.append(str(data[obj]))
        print(result)

    def do_update(self, line):
        """ Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file)
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        Only one attribute can be updated at the time
        """
        if not line:
            print("** class name missing **")
            return False
        else:
            args = line.split(" ")
            if args[0] in class_list:
                if len(args) < 2:
                    print("** instance id missing **")
                    return False
                if len(args) < 3:
                    print("** attribute name missing **")
                    return False
                elif len(args) < 4:
                    print("** value missing **")
                    return False
                data = storage.all()
                is_found = False
                for obj_id in data.keys():
                    instance_id = obj_id.split(".")
                    if args[1] == instance_id[1] and args[0] == instance_id[0]:
                        if "\"" in args[3] or "'" in args[3]:
                            args[3] = args[3].strip("\"")
                            args[3] = args[3].strip("'")
                        try:
                            if int(args[3]):
                                args[3] = int(args[3])
                        except ValueError:
                            try:
                                if float(args[3]):
                                    args[3] = float(args[3])
                            except ValueError:
                                pass
                        setattr(data[obj_id], args[2], args[3])
                        data[obj_id].save()
                        is_found = True
                        break
                if not is_found:
                    print("** no instance found **")
                    return False
            else:
                print("** class doesn't exist **")
                return False

    def do_count(self, line):
        """Counts number of instances of a given class"""
        args = line.split(" ")
        data = storage.all()
        count = 0
        if line:
            if args[0] in class_list:
                pass
            else:
                print("** class doesn't exist **")
                return False
        for obj in data.keys():
            instance_type = obj.split(".")[0]
            if args[0] and args[0] == instance_type:
                count += 1
        print(count)

    def do_quit(self, line):
        """quit the console"""
        return True

    def do_EOF(self, line):
        """ quit the console"""
        print("")
        return True

    def emptyline(self):
        """ does not excute anything """
        pass

    def help_quit(self):
        """ Quit command to exit the program """
        print("Quit command to exit the program")

    def default(self, line):
        """Retrieves all instances of a class by using: <class name>.all()
        Retrieves the number of instances of a class: <class name>.count()
        Retrieves an instance based on its ID: <class name>.show(<id>)
        Destroys an instance based on his ID: <class name>.destroy(<id>)
        Updates an instance based on his ID:
            <class name>.update(<id>, <attribute name>, <attribute value>
        Update an instance based on his ID with a dictionary:
            <class name>.update(<id>, <dictionary representation>)
        """
        inputline = line.split(".")
        try:
            if inputline and "(" in inputline[1] and ")" in inputline[1]:
                args = inputline[1].strip("\"(\")").split("(\"")
                inputline.pop()
                my_list = inputline + args
                parsed = []
                for n in my_list:
                    value = n.split("\",")
                    for v in value:
                        parsed.append(v)
                if len(parsed) >= 2:
                    if parsed[1] == "all":
                        self.do_all(parsed[0])
                    elif parsed[1] == "count":
                        self.do_count(parsed[0])
                    elif parsed[1] == "show":
                        self.do_show(parsed[0] + " " + parsed[2])
                    elif parsed[1] == "destroy":
                        self.do_destroy(parsed[0] + " " + parsed[2])
                    elif parsed[1] == "update":
                        statement = parsed[0] + " " + parsed[2]
                        attr_value = []
                        for pos in range(len(parsed)):
                            if pos >= 3:
                                if "{" in parsed[pos] or "}" in parsed[pos]:
                                    strip_off = [' ', '{', "'", '"', '}']
                                    new = ""
                                    for c in list(parsed[pos]):
                                        if c not in strip_off:
                                            new += c
                                    attr_value.append(new.split(":"))
                                else:
                                    attr_value.append(parsed[pos].strip(" \""))
                        if attr_value and type(attr_value[0]) == list:
                            for item in attr_value:
                                n = statement + " " + item[0] + " " + item[1]
                                self.do_update(n)
                        else:
                            n = statement
                            if attr_value:
                                n += " " + attr_value[0] + " " + attr_value[1]
                            self.do_update(n)
                else:
                    return cmd.Cmd.default(self, line)
            else:
                return cmd.Cmd.default(self, line)
        except IndexError:
            return cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
