import json
import os
class Employee:

    def __init__(self,name, id, title,department) -> None:
        self.name=name
        self.id=id
        self.title=title
        self.department=department

    def dispaly_details(self):
        print("Employee Name: ",self.name)
        print("Employee ID :  ",self.id)
        print("Title    :",self.title)
        print("Department :",self.department)
    
    def __str__(self) -> str:
        return f"Employee's name is {self.name} and id is {self.id}.\n"

class Department:

    def __init__(self,name) -> None:
        self.department_name=name
        self.employee=list()
    
    def add_employee(self,name,id,title):
        e=Employee(name,id,title,self.department_name)
        self.employee.append(e)
        print(f"{e.name} added to {self.department_name}\n")
    
    def remove_employee(self,e):
        if e in self.employee:
            self.employee.remove(e)
            print(f"{e.name} removed from {self.department_name}\n")
        else:
            print(f"{e.name} not present in {self.department_name}\n")

    def list_employee(self):
        for i in self.employee:
            print(i)

class Company:

    def __init__(self) -> None:
        self.company=dict()

    def add_department(self,d):
        if d not in self.company:
            self.company[d]=Department(d)
            print(f"{d} added to company\n")
        else:
            print(f"{d} already in company\n")
    
    def remove_department(self,d):
        if d in self.company:
            del self.company[d]
            print(f"{d} removed from company\n")
        else:
            print(f"{d} not present in company\n")

    def list_department(self):
        for i in self.company.keys():
            print(f"Department Name: {i}")
            self.company[i].list_employee()

class DepartmentEncoder(json.JSONEncoder):
    def default(self, obj):
        d=[]
        for j in obj.employee:
                d.append([j.name,j.id,j.title,j.department])
        return {"department_name":obj.department_name,"employees":d}
        
class DepartmentDecoder(json.JSONDecoder):
    def decode(self, json_string):
        decoded_data = super().decode(json_string)
        m=dict()
        for i in decoded_data:
            department = Department(i)
            d=[]
            for name,id,title,dept in decoded_data[i]["employees"]:
                    d.append(department.add_employee(name,id,title))
            department.employees = d
            m[i]=department
        return m
    
def save_company_data(filename,c):
            with open(filename, 'w') as file:
                json.dump(c.company,file,cls=DepartmentEncoder,indent=5)
            print("Company data has been saved successfully.\n")
        

def load_company_data(filename,c):
        if os.path.exists(filename):
            if os.path.getsize(filename) == 0:
                print(f"The file '{filename}' is empty.\n")
            else:
                with open(filename, 'r') as file:
                    c.company = json.load(file,cls=DepartmentDecoder)
                print("Company data has been loaded successfully.\n")
        else:
            print("File Doesn't exist\n")

def menu():
    print("\nEmployee management System: \n")
    print("1.Add Department")
    print("2.Remove Department")
    print("3.Display Department")
    print("4.Add Employee to a Department")
    print("5.Remove Employee from Department")
    print("6.Display Employees in a Department")
    print("7.Exit")

if __name__=="__main__":
    c=Company()
    load_company_data("Company_details_.txt",c)
    print(c.company)
    while True:
        menu()
        i=input("\nEnter your requirement: \n")
        if i=='1':
            dep=input("Enter Department Name:")
            c.add_department(dep)
        elif i=='2':
            dep=input("Enter Department Name:")
            c.remove_department(dep)
        elif i=='3':
            c.list_department()
        elif i=="4":
            dep=input("Enter department:")
            name=input("Enter the name of Employee:")
            id=int(input("Enter the id of employee:"))
            title=input("Enter the title of Employee:")
            if dep  not in c.company.keys():
                print(f"{dep} not in company\n")
                c.add_department(dep)
            d=c.company[dep]
            d.add_employee(name,id,title)
        elif i=="5":
            dep=input("Enter department:")
            name=input("Enter the Employee name:")
            if dep in c.company.keys():
                d=c.company[dep]
                for e in d.employee:
                    if e.name==name:
                        d.remove_employee(e)
                        break
                else:
                    print(f"{name} Employee doesn't exist in {dep}\n")
            else:
                print(f"{dep} doesn't exist\n")
        elif i=="6":
            dep=input("Enter departmenr:")
            if dep in c.company.keys():
                c.company[dep].list_employee()
            else:
                print(f"{dep} doesn't exist")
        elif i=="7":
            print("Thankyou for using our Service!!!!\n")
            break
        else:
            print("Wrong Input.Try again!\n")
    save_company_data("Company_details_.txt",c)






    
