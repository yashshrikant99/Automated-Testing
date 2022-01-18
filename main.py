import requests
import json
import pandas as pd
dict1={'Method Name':[],'Verb':[],'URL':[],'Mandatory params':[]}
dict2={'Method Name':[],'Verb':[],'Response':[],'Status code':[],'Test':[],'Test status':[]}
df_final=pd.DataFrame(dict2)
def pretty_print(s):
    s = json.dumps(s)
    parsed = json.loads(s)
    pretty=json.dumps(parsed, indent=4)
    return pretty

#given the spec file generate the list of methods,verb, url and mandatory params
def generate_list():
    f = open('spec.json')
    data = json.load(f)
    url = ''
    meth_verb = dict()
    for i in data:
        if i == 'servers':
            url = data[i][0]['url']
    print("basepath url is", url)
    lst1 = []
    for i in data['paths']:
        print(i)
        # dict1['Method Name'].append(i)
        # dict1['URL'].append(url+i)
        mc = 0
        verb = 0
        for j in data['paths'][i]:
            print("\t", j)
            if j != 'parameters':
                # # if(mc==0):
                # #     # print("the verb for method=",i,"is",j)
                # #     meth_verb[url+i]=j.upper()
                # #     dict1['Verb'].append(j.upper())
                lst = []
                paramc = 0
                for k in data['paths'][i][j]:
                    print('\t\t', k, type(k))
                    if (type(k) != dict and k == 'parameters' and paramc == 0):
                        for l in data['paths'][i][j][k]:
                            # print("\t\t",l)
                            if 'required' in l and l['required'] == True:
                                print("\t\t\tmandatory query param for method", i, "is", l['name'], "in", l['in'])
                                lst.append(l['name'])
                        paramc += 1
                dict1['Mandatory params'].append(lst)
                dict1['Method Name'].append(i)
                dict1['URL'].append(i)
                meth_verb[url + i] = j.upper()
                dict1['Verb'].append(j.upper())
                print("\t\t", lst)
                print(dict1)
                mc += 1
                verb += 1
        print("\tnumber of verbs for method", i, "is", verb)
    f1 = open('url.json')
    data1 = json.load(f1)
    # for i in data1:
    #     dt_04(i,data1[i])
    #     print("\n")
    df = pd.DataFrame(dict1)
    df.to_csv("list.csv", index=False)
    print(dict1)
    print(lst1, len(lst1))
    print(len(dict1['Method Name']), len(dict1['Verb']), len(dict1['URL']), len(dict1['Mandatory params']))
    f.close()

def dt_01(method,url,verb,head,qparam,body):
    if(verb=="GET"):
        if(pd.isna(qparam)==True):
            response=requests.request(verb,url,headers=head)
        else:
            response=requests.request(verb,url,headers=head,params=json.loads(qparam))
    elif(verb=='PUT' or verb=='POST' or verb=='DELETE' or verb=='PATCH'):
        if (pd.isna(qparam) == True): #params absent
            if(pd.isna(body) == True):
                print("please provide body")
                response = requests.request(verb, url, headers=head)
            else:
                response=requests.request(verb,url,headers=head,data=json.loads(body))
        else: #params present
            if(pd.isna(body)==True):
                response = requests.request(verb, url, headers=head,params=json.loads(qparam))
            else:
                response = requests.request(verb, url,headers=head,params=json.loads(qparam), data=json.loads(body))
    s=json.dumps(response.json())
    parsed = json.loads(s)
    # print(json.dumps(parsed, indent=4))
    if response.status_code==200:
        print("DT-01-200 ok positive response=passed")
        #'Method Name':[],'Verb':[],'Response':[],'Status code':[],'Test status':[]
        df_final.loc[len(df_final.index)]=[method,verb,response.json(),response.status_code,"DT-A-01","passed"]
    else:
        print("DT-01-200 ok positive response=failed")
        df_final.loc[len(df_final.index)]=[method,verb,response.json(),response.status_code,"DT-A-01","failed"]

#mandatory field check
def dt_02(url,verb,head,body):
    return

#time check
def dt_03(method,url,verb,head):
    response = requests.request(verb,url)
    t=response.elapsed.total_seconds()
    # print(response.json())
    if t<=55:
        print("DT-03 response time check=passed")
        df_final.loc[len(df_final.index)] = [method, verb, response.json(), response.status_code,"DT-A-03","passed"]
    else:
        print("DT-03 response time check=failed")
        df_final.loc[len(df_final.index)] = [method, verb, response.json(), response.status_code,"DT-A-03" ,"failed"]

#mandatory header check
def dt_04(method,url,verb):
    response = requests.request(verb, url)
    if response.status_code == 401:
        print("DT-04-401 ok positive response=passed")
        df_final.loc[len(df_final.index)] = [method, verb, response.json(), response.status_code, "DT-A-04" ,"passed"]
    else:
        print("DT-04-401 ok positive response=failed")
        df_final.loc[len(df_final.index)] = [method, verb, response.json(), response.status_code, "DT-A-04" ,"failed"]


# url='https://api.dev.se.com/v1/customer-order/system/flexset-assembly-compliance/issues/6b04fafc-b7a0-412d-8260-4327ca4d6157'
head={'Authorization':'Bearer jSNtXzscyMj5JBYV3xXrKrCO6WQx',
    'X-IDMS-Authorization':'00Dg0000006I0pD!AR4AQN8w2lOeeGBAnm358ia.BEXit0iM7Aa196wRwOuh5Nqrj1Kd2p9.p2re5Brr71cgPtXysBAPgigSdzsFmvJE2gEAH9FD'}
# ut1(url,'GET',head)
f = open('spec.json')
data = json.load(f)
url = ''
for i in data:
    if i == 'servers':
        url = data[i][0]['url']
url=url.replace("qa","dev")
print("basepath url is", url)
df1=pd.read_csv("input.csv")
for i in range(0,len(df1)):
    # print(df1.iloc[i],'\n')
    # print(url+df1.iloc[i]['URL'])
    url1=url+df1.iloc[i]['URL']
    verb=df1.iloc[i]['Verb']
    head1=json.loads(df1.iloc[i]['Headers'])
    query = df1.iloc[i]['Query params']
    body = df1.iloc[i]['Body']
    method=df1.iloc[i]['Method Name']
    # print(query,pd.isna(query))
    print("Testing for method",method)
    dt_04(method,url1,verb)
    dt_03(method,url1,verb,head)
    # print("passing param and body",query,"\n",body)
    try:
        dt_01(method,url1,verb,head1,query,body)
    except Exception as e:
        print(e)
        continue
    print("\n")
#
# df_final.to_csv("test results.csv",index=False)
# len()
# generate_list()