from pydantic import BaseModel, Field
from typing import List, Optional

"""
Example of creating structured output with Pydantic models.

This module demonstrates how to use Pydantic for data validation
and structured output in Python applications.
"""



class Person(BaseModel):
    """
    Represents a person with validated fields.
    
    Attributes:
        name: The person's full name (must be a non-empty string)
        age: The person's age (must be between 0 and 150)
        email: The person's email address (optional)
        phone: The person's phone number (optional)
    """
    name: str = Field(..., min_length=1, description="Full name")
    age: int = Field(..., ge=0, le=150, description="Age in years")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")


class Company(BaseModel):
    """
    Represents a company with employees.
    
    Attributes:
        name: The company name
        employees: List of Person objects working at the company
        founded_year: The year the company was founded
    """
    name: str = Field(..., min_length=1, description="Company name")
    employees: List[Person] = Field(default_factory=list, description="List of employees")
    founded_year: int = Field(..., ge=1800, description="Year founded")


# Example usage
if __name__ == "__main__":
    # Create individual persons
    person1 = Person(name="Alice", age=30, email="alice@example.com")
    person2 = Person(name="Bob", age=25, phone="555-1234")
    
    # Create a company with employees
    company = Company(
        name="Tech Corp",
        employees=[person1, person2],
        founded_year=2010
    )
    
    # Print structured output
    print(company.model_dump_json(indent=2))