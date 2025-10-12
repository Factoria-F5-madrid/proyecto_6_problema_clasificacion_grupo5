from sqlalchemy import Enum
import enum


class GenderTypeEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class class_type_enum(str, enum.Enum):
    ECO_PLUS = "Economy Plus"
    ECONOMY = "Eco"
    BUSINESS = "Business"

class class_customer_type(str, enum.Enum):
    Loyal = "Loyal Customer"
    Disloyal = "Disloyal Customer"

class class_type_of_travel(str, enum.Enum):
    Personal = "Personal Travel"
    Business = "Business travel"


SqlGenderTypeEnum = Enum(GenderTypeEnum, name="gender_type_enum")
SqlClassTypeEnum = Enum(class_type_enum, name="class_type_enum")
SqlCustomerType = Enum(class_customer_type, name="class_customer_type")
SqlTypeOfTravel = Enum(class_type_of_travel, name="class_type_of_travel")