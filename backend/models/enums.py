from sqlalchemy import Enum
import enum


class GenderTypeEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class class_type_enum(str, enum.Enum):
    ECONOMY = "Economy"
    PREMIUM_ECONOMY = "Premium Economy"
    BUSINESS = "Business"
    FIRST = "First"


SqlGenderTypeEnum = Enum(GenderTypeEnum, name="gender_type_enum")
SqlClassTypeEnum = Enum(class_type_enum, name="class_type_enum")