from pydantic import BaseModel, ValidationError
from typing import List, ClassVar


from pydantic import BaseModel,ValidationError
class Employee(BaseModel):
    name: str
    age: int
    salary: float

employees = [
        {"name": "John", "age": 30, "salary": 50000},
        {"name": "Jane", "age": 28, "salary": 60000},
        {"name": "Bob", "age": 35, "salary": 75000},
        ]
    
try:
    emp_obj= [  Employee(**emp) for emp in employees]
    for emp in emp_obj:
        print(f"Name: {emp.name}, Age: {emp.age}, Salary: {emp.salary}")
        print(emp.model_dump_json(indent=2) )
except ValidationError as e:
    print(f"Validation error: {e}")
