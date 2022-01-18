import jsonref
import json
from Automation_final import read_json,json_parser
def json_extract(obj, key):
    arr = []
    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values
spec=input('Enter the name of the spec file:')
spec=read_json(spec)
spec=json_parser(spec)
spec=json.loads(json.dumps(spec))
with open("spec.json", "w") as outfile:
    outfile.write(json_object)
