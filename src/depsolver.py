import sys
import json

#repositoryInitial
#commands
#constraints
#initial

class Package:
    def __init__(self,name,version,size,depends=[],conflicts=[]):
        self.name = name
        self.version = version
        self.size = size
        self.conflicts = conflicts
        self.dependsList = parseDepends(depends)

    def printFields(self):
        print("Name:" + self.name)

    def parseDepends(self):
        for i in self.depends:

class Dependency:
def __init__(self,dependList):
    
        
        


package_list = []
packages = []
file_object = open(sys.argv[1])
json_root = json.loads(file_object.read())

for i in json_root:
  package_list.append(i)
   
for i in package_list:
    if "depends" in i and "conflicts" in i:
        #print("matches: depends and conflicts")
        #print(list(i.keys()))
        #print("name, version, size, depends, conflicts")
        #print(i["name"] + "\t" + str(i["version"]) + "\t" + str(i["size"]) + "\t" + str(i["conflicts"]) + "\t" + str(i["depends"]))
        packages.append(Package(i["name"], i["version"], i["size"], i["conflicts"], i["depends"]))
    elif "depends" in i:
        #print("matches: depends")
        #print(list(i.keys()))
        #print("name, version, size, depends")
        #print(i["name"] + "\t" + str(i["version"]) + "\t" + str(i["size"]) + "\t" + str(i["depends"]))
        packages.append(Package(i["name"], i["version"], i["size"], i["depends"]))
    elif "conflicts" in i:
        #print("matches: conflicts")
        #print(list(i.keys()))
        #print("name, version, size, conflicts")
        print(i["name"] + "\t" + str(i["version"]) + "\t" + str(i["size"]) + "\t" + str(i["conflicts"]))
        packages.append(Package(i["name"], i["version"], i["size"], i["conflicts"]))
    else:
        #print("didn't match")
        #print(list(i.keys()))
        #print("name, version, size")
        print(i["name"] + "\t" + str(i["version"]) + "\t" + str(i["size"]))
        packages.append(Package(i["name"], i["version"], i["size"]))

for i in packages:
    i.printFields()
    i.printDeps()
