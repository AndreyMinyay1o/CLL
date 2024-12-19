import re
import json


class Client:


    def __init__(self, surname, name, patronymic, address, phone):
        self.surname = self.validate_value(surname, "Surname", is_required=True, only_letters=True)
        self.name = self.validate_value(name, "Name", is_required=True, only_letters=True)
        self.patronymic = self.validate_value(patronymic, "Patronymic", is_required=False, only_letters=True)
        self.address = self.validate_value(address, "Address", is_required=True)
        self.phone = self.validate_value(phone, "Phone", is_required=True, regex=r'^\+\d{1,3}-\d{3}-\d{3}-\d{4}$')

    @staticmethod
    def validate_value(value, field_name, is_required=True, only_letters=False, regex=None):

        if is_required and not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

        if only_letters and not value.replace(' ', '').isalpha():
            raise ValueError(f"{field_name} must contain only letters.")

        if regex and not re.match(regex, value):
            raise ValueError(f"{field_name} is invalid. Expected format: {regex}")

        return value

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

    @classmethod
    def from_json(cls, json_string):

        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

        required_keys = [
            ("surname", "Surname", {"is_required": True, "only_letters": True}),
            ("name", "Name", {"is_required": True, "only_letters": True}),
            ("patronymic", "Patronymic", {"is_required": False, "only_letters": True}),
            ("address", "Address", {"is_required": True}),
            ("phone", "Phone", {"is_required": True, "regex": r'^\+\d{1,3}-\d{3}-\d{3}-\d{4}$'}),
        ]

        validated_data = {
            key: cls.validate_value(data.get(key, "").strip(), field_name, **validation_rules)
            for key, field_name, validation_rules in required_keys
        }

        return cls(
            surname=validated_data["surname"],
            name=validated_data["name"],
            patronymic=validated_data["patronymic"],
            address=validated_data["address"],
            phone=validated_data["phone"]
        )

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

    def __eq__(self, other):

        if not isinstance(other, Client):
            return NotImplemented
        return (
                self.surname == other.surname and
                self.name == other.name and
                self.patronymic == other.patronymic and
                self.address == other.address and
                self.phone == other.phone
        )

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        self.__surname = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def patronymic(self):
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, value):
        self.__patronymic = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value


class ShortClient:
    def __init__(self, base_client):
        if not isinstance(base_client, Client):
            raise ValueError("Expected an instance of Client.")
        self._base = base_client

    @property
    def surname(self):
        return self._base.surname

    @property
    def name(self):
        return self._base.name

    def __str__(self):
        return f"{self.name} {self.surname}"

    def __repr__(self):
        return f"ShortClient({self.name} {self.surname})"


if __name__ == "__main__":
    client = Client.from_string("Minyaylo, Andrey, Andreevich, stavropskaya 149, +7-900-000-5150")
    print(client)

    short_client = ShortClient(client)
    print(short_client)
