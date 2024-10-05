from typing import List

import pydantic_yaml
from node_hermes_core.loader import load_modules
from pydantic import BaseModel, Field


class HermesDependencies(BaseModel):
    """
    Provides a way to specify dependencies for the configuration file.
    This is a subset of the configuration file that is loaded before the main configuration file.
    """

    modules: List[str] = Field(description="List of modules to import before loading the configuration")

    @classmethod
    def from_yaml(cls, file_path: str):
        with open(file_path, "r") as file:
            return pydantic_yaml.parse_yaml_raw_as(cls, file)

    @staticmethod
    def import_from_yaml(file_path: str):
        config = HermesDependencies.from_yaml(file_path)
        return load_modules(config.modules)
