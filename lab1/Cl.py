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
        """
        Создает экземпляр из строки, где значения разделены заданным разделителем.
        """
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
        """
        Создает экземпляр из JSON-строки.
        """
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
