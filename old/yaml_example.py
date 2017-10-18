import yaml
f = open("./../prefs.yaml","r")
Mystring = f.read()
MyYaml= yaml.load(Mystring)


print MyYaml['waze_users']

for key in MyYaml['waze_users']:
    print key
