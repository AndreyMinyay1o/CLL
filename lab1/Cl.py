import re

class Client:

    def __init__(self, surname, name, patronymic, address, phone):
        self.surname = self.validate_surname(surname)
        self.name = self.validate_name(name)
        self.patronymic = self.validate_patronymic(patronymic)
        self.phone = self.validate_phone(phone)
        self.address = self.validate_address(address)

    @staticmethod
    def validate_surname(value):
        if not value.strip():
            raise ValueError("surname cannot be empty.")
        if not value.isalpha():
            raise ValueError("surname must contain only letters.")
        return value
        
    @staticmethod
    def validate_name(value):
        if not value.strip():
            raise ValueError("name cannot be empty.")
        if not value.isalpha():
            raise ValueError("name must contain only letters.")
        return value

    @staticmethod
    def validate_patronymic(value):
        if value.strip() and not value.isalpha():
            raise ValueError("patronymic must contain only letters if provided.")
        return value

    @staticmethod
    def validate_phone(value):
        if not value.strip():
            raise ValueError("Phone number cannot be empty.")
        if not re.match(r'^\+\d{1,3}-\d{3}-\d{3}-\d{4}$', value):
            raise ValueError("Phone number must be in the format +XXX-XXX-XXX-XXXX.")
        return value
    
    @staticmethod
    def validate_address(value):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        return value

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
