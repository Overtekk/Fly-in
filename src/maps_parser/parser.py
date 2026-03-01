# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parser.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/24 17:33:05 by roandrie        #+#    #+#               #
#  Updated: 2026/03/01 19:06:26 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""
This function does two things at a time.
Every map in the "maps" folder will be scanned and added to two dictionnaries.
If a map is valid, meaning all data are clean, it will be stored in the main
dictionnary used by the program. Otherwise, invalid maps are stored elsewhere
but all data errors are stocked to fix it later.
"""

import re

from pathlib import Path
from typing import Any, Dict, List, Set

from pydantic import BaseModel, Field, ValidationError

from src.utils.ui import COLORS
from src.utils.custom_errors import MapError


class Maps():
    """
    Class validating and stocking maps for the program.
    """
    def __init__(self) -> None:
        """
        Initialize "maps" folders and extension for maps, dictionnary for valid
        and invalids maps and launch the process of validation.
        """
        self.root = Path("maps")
        self.extension = "*.txt"
        self.maps_dict: dict[str, list[str]] = {}
        self.invalid_maps_dict: dict[str, list[str]] = {}

        self._add_maps_to_list()

    def _process_map(self, file_path: Path, category: str) -> None:
        """ Internal helper to validate a map and add it to the correct
            dictionary.

        Args:
            file_path (Path): path of the file to validate.
            category (str): category of the map.
        """

        if category not in self.maps_dict:
            self.maps_dict[category] = []
        if category not in self.invalid_maps_dict:
            self.invalid_maps_dict[category] = []

        # If the map is valid, we add it to "maps_dict"
        try:
            MapModel.is_map_valid(file_path)
            self.maps_dict[category].append(file_path.stem)
        # If map is invalid, we add it to the "invalid_maps_dict" with
        # errors list
        except MapError as e:
            self.invalid_maps_dict[category].append((file_path.stem, str(e)))
        # Catch weird errors
        # except Exception as e:
        #     raise MapError(f"Error processing {file_path}: {e}")

    def _cleanup_dictionaries(self) -> None:
        """
        Removes categories that don't contain any maps (valid or invalid) to
        keep the UI menu clean.
        """
        all_categories = (set(list(self.maps_dict.keys()) +
                              list(self.invalid_maps_dict.keys())))

        for category in all_categories:
            # Valid maps
            if category in self.maps_dict and not self.maps_dict[category]:
                del self.maps_dict[category]

            # Invalid maps
            if (category in self.invalid_maps_dict
                    and not self.invalid_maps_dict[category]):
                del self.invalid_maps_dict[category]

    def _add_maps_to_list(self) -> None:
        """Add all maps found in the "maps" folder into a dictionnary. Valid
           maps goes to the main dictionnary used by the program, invalids
           goes to an other dictionnary to know errors.

        Raises:
            MapError: "maps" folder is not found.
            MapError: "maps" folder can't be read (permission error).
        """
        if not self.root.exists() or not self.root.is_dir():
            raise MapError(f"The maps directory '{self.root}' was not found. "
                           "Create it first and place your maps inside.")

        try:
            for item in self.root.iterdir():

                # Directory
                if item.is_dir():
                    for map_file in item.glob(self.extension):
                        self._process_map(map_file, item.name)

                    if item.name in self.maps_dict:
                        self.maps_dict[item.name].sort()

                # Map file
                elif item.match(self.extension):
                    self._process_map(item, "other")

            if "other" in self.maps_dict:
                self.maps_dict["other"].sort()

            # Clean empty folders
            self._cleanup_dictionaries()

            if self.invalid_maps_dict:
                for category in self.invalid_maps_dict:
                    self.invalid_maps_dict[category].sort()

        except PermissionError:
            raise MapError("Permission denied: Cannot read directory "
                           f"'{self.root}'. Check your permission.")
        # except Exception as e:
        #     raise MapError(f"Unexpected error of type {e}")

    def get_maps_list(self) -> None:
        """
        Prints the current state of valid and invalid maps.
        """
        print(f"{COLORS.GREEN}Valid maps:{COLORS.END}")
        for category, maps in self.maps_dict.items():
            print(f"{category}: {maps}")

        print(f"{COLORS.RED}Invalid maps:{COLORS.END}")
        for category, maps in self.invalid_maps_dict.items():
            print(f"{category}: {maps}")


class MapModel(BaseModel):
    nb_drones: int = Field(ge=1)
    start_hub: str
    end_hub: str
    hub: List[str] = Field(default_factory=list)
    connection: List[str] = Field(default_factory=list)

    @classmethod
    def is_map_valid(cls, file: Path) -> "MapModel":
        # Check if file extension is '.txt' if user manually launch the script.
        if file.suffix != ".txt":
            raise MapError(f"Invalid file extension '{file.suffix}'. Map must "
                           "be a '.txt' file.")

        # Valid first key
        valid_map_key: Set[str] = {
            "nb_drones", "start_hub", "end_hub", "hub", "connection"
        }
        # Valid first key and can be duplicate
        list_key: Set[str] = {"hub", "connection"}
        # Valid metadata for connection
        valid_connection_metadata = {"max_link_capacity"}
        # Raw config with all maps informations
        raw_config: Dict[str, Any] = {}
        # List of errors of a map
        errors_list: List[str] = []

        key_line_map: Dict[str, int] = {}
        is_first_param = True

        try:
            with open(file, "r") as f:
                for i, line in enumerate(f, 1):
                    line = line.split("#", 1)[0].strip()

                    # Ignore empty line and comment
                    if line.startswith("#") or not line:
                        continue

                    # Check if separator exist
                    if ":" not in line:
                        errors_list.append(f"Line {i}: Invalid format "
                                           "(missing ':').")
                        continue

                    # Split key and value
                    key, value = line.split(":", 1)
                    key = key.strip()

                    # Check if key is valid
                    if key not in valid_map_key:
                        errors_list.append(f"Line {i}: key '{key}' doesn't "
                                           "exist.")
                        continue

                    # Check if first key is "nb_drones"
                    if is_first_param:
                        if key != "nb_drones":
                            errors_list.append(f"Line {i}: First parameter must"
                                               f" be 'nb_drones'. "
                                               f"Found '{key}'.")
                        is_first_param = False
                    elif key == "nb_drones":
                        errors_list.append(f"Line {i}: 'nb_drones' must be at "
                                           "the first line.")

                    if key in ["start_hub", "hub", "end_hub"]:
                        zone_data = re.findall(r"\[[^\]]*\]|\S+", value)
                        if len(zone_data) in [3, 4]:
                            if cls._check_zone_name(zone_data[0]) is False:
                                errors_list.append(f"Line {i}: error in zone name ('{zone_data[0]}'). Check that is a valid string, with no space and '-'.")
                            if cls._check_zone_coords(zone_data[1]) is False:
                                errors_list.append(f"Line {i}: error in zone coordinates ('{zone_data[1]}). Check that is a valid positive int.")
                            if cls._check_zone_coords(zone_data[2]) is False:
                                errors_list.append(f"Line {i}: error in zone coordinates ('{zone_data[2]}). Check that is a valid positive int.")
                            if len(zone_data) == 4:
                                if cls._check_zone_metada(zone_data[3]) is False:
                                    errors_list.append(f"Line {i}: error in zone metadata.")
                        else:
                            if len(zone_data) < 3:
                                errors_list.append(f"Line {i}: Missing datas for zone. Valid syntax: <name>(str) <x>(int) <y>(int) <metadata> (metadata is optional).")
                            else:
                                errors_list.append(f"Line {i}: Too much datas for zone. Valid syntax: <name>(str) <x>(int) <y>(int) <metadata> (metadata is optional).")

                    # Constructing data
                    if key in list_key:
                        if key not in raw_config:
                            raw_config[key] = []
                        raw_config[key].append(value)
                        if key not in key_line_map:
                            key_line_map[key] = i
                    else:
                        if key in raw_config:
                            errors_list.append(f"Line {i}: Duplicate key: "
                                               f"'{key}' must be unique.")
                        raw_config[key] = value
                        key_line_map[key] = i

        except FileNotFoundError:
            raise MapError(f"File not found: {file}")
        except PermissionError:
            raise MapError(f"Can't read file, check permissions: {file}")
        # except Exception as e:
        #     raise MapError(f"Critical error reading file {file.name}: {e}")

        print(raw_config)

        try:
            map = cls(**raw_config)
        except ValidationError as e:
            for error in e.errors():
                field_name = str(error['loc'][0])
                msg = error['msg']

                if error['type'] == "greater_than_equal":
                    msg = (f"Value too small. Must be at least "
                           f"{error['ctx']['ge']}")
                elif error['type'] == "int_parsing":
                    msg = "Value must be an integer"

                line_num = key_line_map.get(field_name, "Unknown")

                if error['type'] == 'missing':
                    errors_list.append(f"Missing required key "
                                       f"'{field_name}'.")
                else:
                    errors_list.append(f"Line {line_num}: Key '{field_name}': "
                                       f"{msg}")

        if errors_list:
            errors_list.sort(key=lambda x: int(x.split()[1].strip(":"))
                             if x.startswith("Line ") else float("inf"))
            raise MapError("\n".join(errors_list))

        return map

    @staticmethod
    def _check_zone_name(zone_name: str) -> bool:
        if " " in zone_name or "-" in zone_name or not isinstance(zone_name, str):
            return False
        return True

    @staticmethod
    def _check_zone_coords(coords: int) -> bool:
        try:
            int(coords)
            return True
        except ValueError:
            return False

    @staticmethod
    def _check_zone_metada(metada: str) -> bool:
        # Valid metadata for zone
        valid_zone_metadata = {"zone", "color", "max_drones"}
        # Valid zone type
        valid_zone_type = {"normal", "blocked", "restricted", "priority"}


