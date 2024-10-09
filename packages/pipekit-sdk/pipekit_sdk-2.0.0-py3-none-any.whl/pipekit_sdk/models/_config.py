from pydantic.v1 import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        """General config for generated models."""

        allow_population_by_field_name = True
        """support populating object by Field alias"""

        allow_mutation = True
        """allow mutation of objects post instantiation"""

        use_enum_values = True
        """supports using enums, which are then unpacked to obtain the actual `.value`"""
