import re
import os
import json
import yaml

class Client:
    def __init__(self, surname, name, patronymic, address, phone, client_id=None):
        self.surname = self.validate_value(surname, "Surname", is_required=True, only_letters=True)
        self.name = self.validate_value(name, "Name", is_required=True, only_letters=True)
        self.patronymic = self.validate_value(patronymic, "Patronymic", is_required=False, only_letters=True)
        self.address = self.validate_value(address, "Address", is_required=True)
        self.phone = self.validate_value(phone, "Phone", is_required=True, regex=r'^\+\d{1,3}-\d{3}-\d{3}-\d{4}$')

        if client_id is None:
            self.client_id = None
        else:
            self.client_id = client_id

    @staticmethod
    def validate_value(value, field_name, is_required=True, only_letters=False, regex=None):
        if is_required and not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        if only_letters and not value.replace(' ', '').isalpha():
            raise ValueError(f"{field_name} must contain only letters.")
        if regex and not re.match(regex, value):
            raise ValueError(f"{field_name} is invalid. Expected format: {regex}")
        return value

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        if value is None:
            self.__client_id = value
        else:
            self.__client_id = value

    def get_client_id(self):
        return self.client_id

    def to_dict(self):
        return {
            "surname": self.surname,
            "name": self.name,
            "patronymic": self.patronymic,
            "address": self.address,
            "phone": self.phone,
            "client_id": self.client_id
        }

    @classmethod
    def from_string(cls, data_string, delimiter=","):
        fields = data_string.split(delimiter)
        if len(fields) != 5:
            raise ValueError("Data string must contain exactly 5 fields separated by the delimiter.")
        validated_fields = [
            cls.validate_value(field.strip(), field_name, **validation_rules)
            for field, (field_name, validation_rules) in zip(fields, [
                ("Surname", {"is_required": True, "only_letters": True}),
                ("Name", {"is_required": True, "only_letters": True}),
                ("Patronymic", {"is_required": False, "only_letters": True}),
                ("Address", {"is_required": True}),
                ("Phone", {"is_required": True, "regex": r'^\+\d{1,3}-\d{3}-\d{3}-\d{4}$'}),
            ])
        ]
        return cls(*validated_fields)

    def __str__(self):
        return (
            f"Full Details:\n"
            f"Surname: {self.surname}\n"
            f"Name: {self.name}\n"
            f"Patronymic: {self.patronymic}\n"
            f"Address: {self.address}\n"
            f"Phone: {self.phone}"
        )

    def __repr__(self):
        return f"Client({self.name} {self.surname})"


class ClientRepJson:
    def __init__(self, file_name):
        self.file_name = file_name
        self.clients = self.read_all()

    def read_all(self):
        try:
            with open(self.file_name, 'r') as file:
                data = json.load(file)
                clients = []
                for client_data in data:
                    client_id = client_data.get("client_id", None)
                    client = Client(
                        surname=client_data["surname"],
                        name=client_data["name"],
                        patronymic=client_data.get("patronymic", ""),
                        address=client_data["address"],
                        phone=client_data["phone"],
                        client_id=client_id
                    )
                    clients.append(client)
                return clients
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Error: The file '{self.file_name}' is not a valid JSON.")
            return []

    def save_all(self):
        data = []
        for client in self.clients:
            client_data = client.to_dict()
            if client_data["client_id"] is None:
                client_data["client_id"] = self.get_new_client_id()
            data.append(client_data)
        with open(self.file_name, 'w') as file:
            json.dump(data, file, indent=4)

    def get_by_id(self, client_id):
        for client in self.clients:
            if client.get_client_id() == client_id:
                return client
        raise ValueError(f"Client with ID {client_id} not found")

    def get_k_n_short_list(self, k, n):
        start = (k - 1) * n
        end = start + n
        return self.clients[start:end]

    def sort_by_field(self, field="client_id"):
        self.clients.sort(key=lambda client: getattr(client, field))

    def add_client(self, surname, name, patronymic, address, phone):
        new_id = self.get_new_client_id()
        new_client = Client(surname, name, patronymic, address, phone, new_id)
        self.clients.append(new_client)
        self.save_all()

    def replace_by_id(self, client_id, new_client):
        for i, client in enumerate(self.clients):
            if client.get_client_id() == client_id:
                self.clients[i] = new_client
                self.save_all()
                return True
        return False

    def delete_by_id(self, client_id):
        self.clients = [client for client in self.clients if client.get_client_id() != client_id]
        self.save_all()

    def get_count(self):
        return len(self.clients)

    def get_new_client_id(self):
        max_id = max([client.get_client_id() for client in self.clients if client.get_client_id() is not None],
                     default=0)
        return max_id + 1

f __name__ == "__main__":
    client_rep_json = ClientRepJson('clients.json')

    client_rep_json.add_client("Minyaylo", "Andrey", "Andreevich", "stavropskaya 149", "+7-900-000-5150")

    try:
        client = client_rep_json.get_by_id(1)
        print(client)
    except ValueError as e:
        print(e)

