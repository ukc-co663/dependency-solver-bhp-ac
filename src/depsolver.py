import sys
import json
import re
from enum import Enum
from collections import defaultdict


class Operator(Enum):
    LESS_THAN = "<"
    LESS_THAN_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL = ">="
    EQUALS = "="
    ANY = "*"

    def __str__(self):
        return self.value


class Operation(Enum):
    INSTALL = "+"
    REMOVE = "-"

    def __str__(self):
        return self.value


class Dependency:
    def __init__(self, raw_dep, opt=False):
        self.opt = opt
        if "<=" in raw_dep:
            split_vals = raw_dep.split("<=")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.LESS_THAN_EQUAL
        elif ">=" in raw_dep:
            split_vals = raw_dep.split(">=")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.GREATER_THAN_EQUAL
        elif "<" in raw_dep:
            split_vals = raw_dep.split("<")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.LESS_THAN
        elif ">" in raw_dep:
            split_vals = raw_dep.split(">")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.GREATER_THAN
        elif "=" in raw_dep:
            split_vals = raw_dep.split("=")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.EQUALS
        else:
            self.name = raw_dep
            self.constraint = Operator.ANY

    def __str__(self):
        if self.constraint != Operator.ANY:
            return self.name + str(self.constraint) + str(self.version)
        else:
            return self.name


class Conflict:
    def __init__(self, raw_conflict):
        if "<=" in raw_conflict:
            split_vals = raw_conflict.split("<=")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.LESS_THAN_EQUAL
        elif ">=" in raw_conflict:
            split_vals = raw_conflict.split(">=")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.GREATER_THAN_EQUAL
        elif "<" in raw_conflict:
            split_vals = raw_conflict.split("<")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.LESS_THAN
        elif ">" in raw_conflict:
            split_vals = raw_conflict.split(">")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.GREATER_THAN
        elif "=" in raw_conflict:
            split_vals = raw_conflict.split("=")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.EQUALS
        else:
            self.name = raw_conflict
            self.constraint = Operator.ANY

    def __str__(self):
        if self.constraint != Operator.ANY:
            return self.name + str(self.constraint) + str(self.version)
        else:
            return self.name


class Constraint:
    def __init__(self, raw_constraint):
        if "+" in raw_constraint:
            temp = raw_constraint.split("+")
            raw_constraint = str(temp[1])
            self.operation = Operation.INSTALL
        elif "-":
            temp = raw_constraint.split("-")
            raw_constraint = str(temp[1])
            self.operation = Operation.REMOVE

        if "<=" in raw_constraint:
            split_vals = raw_constraint.split("<=")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.LESS_THAN_EQUAL
        elif ">=" in raw_constraint:
            split_vals = raw_constraint.split(">=")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.GREATER_THAN_EQUAL
        elif "<" in raw_constraint:
            split_vals = raw_constraint.split("<")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.LESS_THAN
        elif ">" in raw_constraint:
            split_vals = raw_constraint.split(">")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.GREATER
        elif "=" in raw_constraint:
            split_vals = raw_constraint.split("=")
            self.name = split_vals[0]
            self.version = split_vals[1]
            self.constraint = Operator.EQUALS
        else:
            self.name = raw_constraint
            self.constraint = Operator.ANY

    def __str__(self):
        if self.constraint != Operator.ANY:
            return self.name + str(self.constraint) + str(self.version)
        else:
            return self.name


def parse(package_list):
    dep_list = []
    for i in package_list:
        if isinstance(i, list):
            if len(i) > 1:
                for j in i:
                    dep_list.append(Dependency(j, True))
            else:
                dep_list.append(Dependency(i[0]))
        else:
            dep_list.append(Dependency(i))
    return dep_list


class Package:

    def print_dependencies(self):
        for i in self.dependecies:
            print(i)

    def __init__(self, raw_package):

        self.dependecies = []
        self.conflicts = []

        if 'name' in raw_package:
            self.name = raw_package['name']
        if 'version' in raw_package:
            self.version = raw_package['version']
        if 'size' in raw_package:
            self.size = raw_package['size']
        if 'conflicts' in raw_package:
            l = []
            for i in raw_package['conflicts']:
                l.append(Conflict(i))
            self.conflicts = l
        if 'depends' in raw_package:
            self.dependecies = self.parse_depends(raw_package['depends'])

    def __str__(self):
        return self.name + "=" + self.version

    def parse_depends(self, depends_list):
        l = []
        for i in depends_list:
            if isinstance(i, list):
                if len(i) > 1:
                    for j in i:
                        l.append(Dependency(j, True))
                else:
                    l.append(Dependency(i[0]))
            else:
                l.append(Dependency(i))
        return l


class Command:
    def __init__(self, raw_command):
        if "+" in raw_command:
            self.command = Operation.INSTALL
        elif "-" in raw_command:
            self.command = Operation.REMOVE

        raw_command = raw_command[1:]
        com = raw_command.split("=")
        self.name = com[0]
        self.version = com[1]

    def __str__(self):
        return str(self.command) + self.name + "=" + str(self.version)


class Installed:
    def __init__(self, name, version):
        self.name = name
        self.version = version


def get_json_array(arg):
    file_object = open(arg)
    json_object = json.loads(file_object.read())
    return json_object


def build_init(json):
    init_list = []
    for i in json:
        item = i.split("=")
        init_list.append(Installed(item[0], item[1]))
    return init_list


def build_repo(json):
    pkg_list = []
    for i in json:
        pkg_list.append(Package(i))
    return pkg_list


def build_comms(json):
    com_list = []
    for i in json:
        com_list.append(Command(i))
    return com_list


def build_cons(json):
    com_list = []
    for i in json:
        com_list.append(Constraint(i))
    return com_list


def build_dict(raw):
    list = []
    for i in raw:
        list.append(i)
    return list


def build(x):
    l = []
    for i in x:
        l.append(i)
    return l


class System:
    def __init__(self, constraints, packages, initial=[]):
        self.state = self.initalise(initial)
        self.commands = []
        self.constraints = constraints
        self.packages = self.initalise(packages)
        a = self.search_package("B", "3.0", Operator.EQUALS)
        print("done")

    def initalise(self, item_list):
        item_dict = defaultdict(list)
        for i in item_list:
            item_dict[str(i.name)].append(i)
        return item_dict

    def search_package(self, name, version, operator=Operator.ANY):
        pkg_set = self.packages[name]

        if operator == Operator.ANY:
            return pkg_set
        else:
            results = []
            if operator == Operator.LESS_THAN_EQUAL:
                for i in pkg_set:
                    if i.version <= version:
                        results.append(i)
            elif operator == Operator.GREATER_THAN_EQUAL:
                for i in pkg_set:
                    if i.version >= version:
                        results.append(i)
            elif operator == Operator.LESS_THAN:
                for i in pkg_set:
                    if i.version < version:
                        results.append(i)
            elif operator == Operator.GREATER_THAN:
                for i in pkg_set:
                    if i.version > version:
                        results.append(i)
            elif operator == Operator.EQUALS:
                for i in pkg_set:
                    if i.version == version:
                        results.append(i)
            return results

def main():
    # sys.argv[1]
    repo_object = open("/mnt/file/programming/git/depsolver/src/repository.json")
    repo_root = json.loads(repo_object.read())

    commands_object = open("/mnt/file/programming/git/depsolver/src/commands.json")
    commands_root = json.loads(commands_object.read())

    initial_object = open("/mnt/file/programming/git/depsolver/src/initial.json")
    initial_root = json.loads(initial_object.read())

    constraints_object = open("/mnt/file/programming/git/depsolver/src/constraints.json")
    constraints_root = json.loads(constraints_object.read())

    packages = build_repo(build(repo_root))
    # commands = build_comms(build(commands_root))
    constraints = build_cons(build(constraints_root))
    initial_root = build(initial_root)

    if len(initial_root) > 0:
        initial = build_init(initial_root)
        commands = System(constraints, packages, initial)
    else:
        commands = System(constraints, packages)

    # return state
    print("packages:")
    for i in packages:
        print(i)
    print("commands:")
    for i in commands:
        print(i)
    print("constraints:")
    for i in constraints:
        print(i)


if __name__ == "__main__":
    main()
