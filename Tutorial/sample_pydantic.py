from pydantic import BaseModel
import os
import json

class User(BaseModel):
    name:str
    age:int
    email:str

if __name__ == "__main__":
    user=User(name="Srinivas", age=38, email="srinivasreddy@gmail.com")
    print(user.model_dump_json(indent=2))

