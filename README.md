## Getting started
To install the packages just go to the directory where the above text file and script are present and open a new command prompt terminal by replacing the path in file explorer ,for ex: ‘C:\Users\SESA612288\Desktop\Automation’ with ‘cmd’

And then type 
>pip install -r requirements.txt

The same can also be done on a terminal in VS Code.

## Updated Testing Strategy
![image](https://user-images.githubusercontent.com/41529190/149934689-bb2ef8da-c481-455a-b72e-44f301094070.png)

- Sample test logs can be found [here](https://github.com/yashshrikant99/Automated-Testing/blob/master/Sample%20Test%20Logs%20-%20New.xlsx)
## Process
### A.	For New APIs which are being tested:

1.	Save the spec file with the proper extension , for ex: ‘spec.json’ or ‘spec.yaml’. The spec files should have no errors as such.
2.	Open postman and import the spec file. 
-![image](https://user-images.githubusercontent.com/41529190/149932000-54f54802-7376-4a0e-baef-f21aa30ca489.png)
3.	This creates a collection with the default values and responses which are present in the spec file.
-![image](https://user-images.githubusercontent.com/41529190/149932156-7da7445c-305c-49cf-b7a5-c72c7eb72de1.png)
4.	***For some APIs the requests might be nested inside a folder. These need to be un-nested and need to be placed sequentially without any folder structure present. The empty folders then need to be deleted before proceeding to the next step.***
5.	Replace these values with the accurate values which upon sending should return 200 ok.
6.	Export the modified collection with correct values as ‘postman_collection.json’ and save it to the same directory where the spec and the script are present.
7.	Run the script by clicking ‘Cntrl+F5’ and then enter the name of the spec file as: spec.json or spec.yaml accordingly. 
-![image](https://user-images.githubusercontent.com/41529190/149932452-195b1e3a-ca7a-47f4-8e29-aa989d881894.png) 
8.	Example of a success response:
-![image](https://user-images.githubusercontent.com/41529190/149932474-0e5c8eab-1cc1-4252-8ec6-ce85ca3ccfcb.png)
9.	Import the processed collection which will have the following format : <API Name> processed.json back into postman and verify the requests.Example of a successful creation:
- ![image](https://user-images.githubusercontent.com/41529190/149932498-b2136900-0b48-477f-bad9-f4eb1948770a.png)

### B.	For APIs with already existing collections:

1.	If an API already has a collection present then we keep only one request per method which gives 200 ok.
2.	Save the spec file as: spec.json or spec.yaml in the same directory as the script
3.	The name of the methods need to be renamed as per the description of the method present in the spec file, for ex:
-![image](https://user-images.githubusercontent.com/41529190/149932574-bb20b2d5-bb6b-48ac-8d50-8867025e6d5e.png)
4.	Once this is done we export the collection and follow the same steps as above from 4-9.

## Troubleshooting:
•	In some cases the script might throw an error , the most common ones being ‘None type not iterable’ or ‘Key error: key not found ’. In such cases the following steps need to be taken:
1.	Check if spec has no issues- usual ones are ‘application/jsin’ or ‘application/Json’ instead of ‘application/json’
2.	Check if the description for each method match the ones present in the collection- sometimes methods may not have any summary present , in those cases a manual summary may need to be added. For ex:-
- Before adding:![image](https://user-images.githubusercontent.com/41529190/149933155-e1e61617-a9ec-4ba2-b8fb-9cbe9026128b.png)

- After adding:![image](https://user-images.githubusercontent.com/41529190/149933256-445079a1-98b0-43a8-9a6c-5435b7d4e840.png)

The script is very dependent on the validity of the spec file. If there are any issues kindly reach me out at yash.shrikant@se.com .
  
# To-Do
- [ ] In case of errors create a collection for the rest of the methods which dont have error 
- [ ] Automatic testing for mandatory parameters

