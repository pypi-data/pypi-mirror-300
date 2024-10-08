import requests

class UserCreator:
    def __init__(self, first_name: str, last_name: str, age: int):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.base_url = 'https://dummyjson.com/users/add'

    def create_user(self) -> dict:
        """Creates a user by sending a POST request to the API."""
        data = {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "age": self.age
        }
        response = requests.post(self.base_url, json=data)
        response_data = response.json()
        return response_data

    def get_user_info(self) -> str:
        """Fetches and returns the created user's ID, first name, last name, age."""
        response_data = self.create_user()
        user_id = response_data.get('id')
        first_name = response_data.get('firstName')
        last_name = response_data.get('lastName')
        age = response_data.get('age')
        return f"ID: {user_id}\nFirst Name: {first_name}\nLast Name: {last_name}\nAge: {age}"