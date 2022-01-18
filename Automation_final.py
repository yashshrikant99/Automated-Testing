import requests
import json
from pprint import pprint
import jsonref
import yaml
import sys 
import copy
import jsonpickle
from json import JSONEncoder
import yaml

def event(n):
    file='Unit Tests Sample.postman_collection.json'
    f = open(file)
    data = json.load(f)
    return data['item'][n]['event']

def get_first_response(data,method_name): #to get the first response code and description from spec
    for i in data['paths']:
        for j in data['paths'][i]:
            if j=='parameters':
                continue
            if data['paths'][i][j]['summary']==method_name:
                for k in data['paths'][i][j]['responses']:
                    lst=list(data['paths'][i][j]['responses'][k].keys())[0]
                    if lst=='description':
                        lst1=list(data['paths'][i][j]['responses'][k].values())[0]
                        return k,lst1
            
                
def replace_schema(schema,name,verb,spec):
    test2=event(1)
    code,desc=get_first_response(spec,name)
    test2[1]['script']['exec'][0]=test2[1]['script']['exec'][0].replace('200',code) #replace status code
    test2[1]['script']['exec'][16]=test2[1]['script']['exec'][16].replace('pm.response.to.be.ok',"pm.response.to.have.status('"+desc+"')")
    test=test2[1]['script']['exec'][31]# this gets var schema
    final_schema=schema[name]
    final_schema=final_schema.replace('"type": "string"','"type":["string","null"]')
    final_schema=final_schema.replace('"type": "integer"','"type":["integer","null"]')
    final=test[:12]+final_schema+test[12:] #populates var schema with schema
    test2[1]['script']['exec'][31]=final
    if(verb=='GET'):
        del test2[1]['script']['exec'][48:61] #removes request header check for GET methods
    return test2
def replace_status_code(schema,method_name,method_verb,spec):
    test2=event(0)
    code,desc=get_first_response(spec,method_name)
    test2[1]['script']['exec'][0]=test2[1]['script']['exec'][0].replace('200',code)
    return test2
def modify_json2(schema,data,spec):
    dict1=[]
    ch=65
    for i in data['item']:
        lst=[]
        method_name=i['name']
        method_verb=i['request']['method']
        i['response']=[]
        for j in range(0,5):
            dict2={}
            dict2=copy.deepcopy(i)
            dict2['name']='DT-'+chr(ch)+'-0'+str(j+1)
            if j==0:
                tests=replace_status_code(schema,method_name,method_verb,spec)
            elif j==1:
                tests=replace_schema(schema,method_name,method_verb,spec)
            else:
                tests=event(j)
            dict2['event']=tests
            lst.append(dict2) 
        ch+=1
        for k in lst:
            dict1.append(k)
    return dict1
def read_json(path):
    f = open(path,)
    if(path.endswith(".yaml")):
        data=yaml.load(f,Loader=yaml.FullLoader)
    else:
        data = json.load(f)
    f.close()
    return data

def get_mandatory(data):
    data=json_parser(data)
    for i in data['paths']: #this is per method
        print('for method',i)
        for j in data['paths'][i]: #this is per verb
            if j=='parameters' :# this is to get path params
                params=data['paths'][i][j]
                for m in params:
                    if 'required' in m:
#                         print(m)
                        print('\t\tmandatory param is',m['name'],'which is',m['in'],'param')
            for k in data['paths'][i][j]: #this is for all variables within the method/verb
                if(k=='parameters'):  
                    print('\tfor verb',j)
                    for l in data['paths'][i][j][k]: #this is to iterate through all 
                        if 'required' in l:
                            print('\t\tmandatory param is',l['name'],'which is',l['in'],'param')
                        if l['name']=='body':
                            if('required' in l['schema']):
                                get_required(l['schema'])
def get_required(d):
    for k, v in d.items():
        if isinstance(v, dict):
            get_required(v)
        else:
            if(k=='required' or v=='required'):
                print("\t\tmandatory fields in body are",v)
def get_schema(data):
    data=json_parser(data)
    final_schema={}
    schema_file={}
    open("schema.json", "w").close()
    file = open("schema.json", "a")
    for i in data['paths']:#this is for each method
        for j in data['paths'][i]: #this is for verbs in that method
            if j!='parameters':
                for k in data['paths'][i][j]['responses']: #this gives the status code
                    method_name=data['paths'][i][j]['summary']
                    if str(k).startswith('2'):
                        if('swagger' in data):
                            version='swagger'
                        elif('openapi' in data):
                            version='openapi'
                        if data[version].startswith("3"):
                            schema=data['paths'][i][j]['responses'][k]['content']['application/json']['schema']
                        elif data[version].startswith("2"):
                            schema=data['paths'][i][j]['responses'][k]['schema']
                        print("-->>>the schema for method",j,i,k,"response is-->>>",file=file)
                        print(json.dumps(schema,indent=1),file=file)
                        print("\n",file=file)
                        final_schema[method_name]=json.dumps(schema,indent=1)
                        schema_file[j+" "+i+" "+k+" response"]=json.dumps(schema,indent=1)
    # with open("schema.json", "w") as write_file:
    #     print(schema_file, file=write_file)
    return final_schema
def json_parser(schema):
    schema=json.dumps(schema) #converts json dict to string
    data = jsonref.loads(schema) #converts string to json object
    return data
def first_collection(name):
    f = open(name,)
    data = json.load(f)
    data=json_parser(data)
    f.close()
    for i in data['item']:
        print(i['name'])
    return pprint(data)
def output_txt(filename,s): #saves only json body as txt file
    jsonString = json.dumps(s)
    jsonFile = open(filename+".txt", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
def main():
    spec=input('Enter the full spec file name with extension:')
    # spec='spec.json'
    spec=read_json(spec)
#     get_mandatory(spec)
    schema=get_schema(spec)
    data=read_json("postman_collection.json")
    mod=modify_json2(schema,data,spec)
    data['item']=mod
    data['info']['name']=data['info']['name']+' processed'
    name=data['info']['name']
    try:
        with open(name+".json", "w") as outfile:
            json.dump(data, outfile,indent=4)
        print("success-output saved as",name+".json")
    except Exception as e:
        print(e)
        print("failed")
if __name__=='__main__':
    main()
