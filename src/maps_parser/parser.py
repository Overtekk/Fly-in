# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parser.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/24 17:33:05 by roandrie        #+#    #+#               #
#  Updated: 2026/03/02 22:02:39 by roandrie        ###   ########.fr        #
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
from typing import Any, Dict, List, Self, Set

from pydantic import BaseModel, Field, ValidationError, model_validator

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
        self.invalid_maps_dict: dict[str, list[tuple[str, str]]] = {}

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
        for category, invalid_maps in self.invalid_maps_dict.items():
            print(f"{category}: {invalid_maps}")


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

        valid_map_key: Set[str] = {
            "nb_drones", "start_hub", "end_hub", "hub", "connection"
        }
        list_key: Set[str] = {"hub", "connection"}

        valid_zones = []
        existing_connection: List[str] = []

        raw_config: Dict[str, Any] = {}

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
                            errors_list.append(f"Line {i}: First parameter"
                                               f" must be 'nb_drones'. "
                                               f"Found '{key}'.")
                        is_first_param = False
                    elif key == "nb_drones":
                        errors_list.append(f"Line {i}: 'nb_drones' must be at "
                                           "the first line.")

                    # Check zones data
                    if key in ["start_hub", "hub", "end_hub"]:
                        zone_data = re.findall(r"\[[^\]]*\]|\S+", value)
                        if len(zone_data) in [3, 4]:
                            if cls._check_valid_zones(zone_data[0]) is False:
                                errors_list.append(f"Line {i}: error in zone "
                                                   f"name ('{zone_data[0]}'). "
                                                   "Check that is a valid "
                                                   "string, with no space and "
                                                   "'-'.")
                            else:
                                if zone_data[0] in valid_zones:
                                    errors_list.append(f"Line {i}: Duplicated"
                                                       " zone name: "
                                                       f"{zone_data[0]}")
                                valid_zones.append(zone_data[0])

                            if cls._check_zone_coords(zone_data[1]) is False:
                                errors_list.append(f"Line {i}: error in zone "
                                                   "coordinates ('"
                                                   f"{zone_data[1]}). Check "
                                                   "that is a valid int.")

                            if cls._check_zone_coords(zone_data[2]) is False:
                                errors_list.append(f"Line {i}: error in zone "
                                                   "coordinates ('"
                                                   f"{zone_data[2]}). Check "
                                                   "that is a valid int.")

                            if len(zone_data) == 4:
                                tmp_error = cls._check_metada(zone_data[3],
                                                              "zone")
                                if tmp_error:
                                    for e in tmp_error:
                                        errors_list.append(f"Line {i}: {e}")
                        else:
                            if len(zone_data) < 3:
                                errors_list.append(f"Line {i}: Missing datas "
                                                   "for zone. Valid syntax: "
                                                   "<name>(str) <x>(int) <y>"
                                                   "(int) <metadata> (metadata"
                                                   " is optional).")
                            else:
                                errors_list.append(f"Line {i}: Too much datas "
                                                   "for zone. Valid syntax: "
                                                   "<name>(str) <x>(int) <y>"
                                                   "(int) <metadata> (metadata"
                                                   " is optional).")
                    # Check connections data
                    elif key == "connection":
                        zone_data = re.findall(r"\[[^\]]*\]|\S+", value)
                        if len(zone_data) in [1, 2]:
                            tmp_error = cls._check_connection(
                                zone_data[0], existing_connection, valid_zones)
                            if tmp_error:
                                for e in tmp_error:
                                    errors_list.append(f"Line {i}: {e}")
                            else:
                                existing_connection.append(zone_data[0])
                                zone1, zone2 = zone_data[0].split("-", 1)
                                inversed = f"{zone2}-{zone1}"
                                existing_connection.append(inversed)

                            if len(zone_data) == 2:
                                tmp_error = cls._check_metada(zone_data[1],
                                                              "connection")
                                if tmp_error:
                                    for e in tmp_error:
                                        errors_list.append(f"Line {i}: {e}")
                        else:
                            if len(zone_data) < 1:
                                errors_list.append(f"Line {i}: Missing data "
                                                   "for connection. Valid "
                                                   "syntax: <zone1>-<zone2> "
                                                   "<metadata> (metadata is "
                                                   "optional).")
                            else:
                                errors_list.append(f"Line {i}: Too much data "
                                                   "for connection. Valid "
                                                   "syntax: <zone1>-<zone2> "
                                                   "<metadata> (metadata is "
                                                   "optional).")

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

        try:
            map = cls(**raw_config)
        except ValidationError as e:
            for error in e.errors():
                if not error['loc']:
                    errors_list.append(error['msg'])
                    continue

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

    @model_validator(mode='after')
    def validate_coords(self) -> Self:
        seen_coords: set[tuple[int, int]] = set()

        all_zones = [self.start_hub, self.end_hub] + self.hub

        for zone in all_zones:
            parts = zone.split()

            if len(parts) < 3:
                continue

            try:
                x = int(parts[1])
                y = int(parts[2])
                curr_coords = (x, y)
            except ValueError:
                continue

            if curr_coords in seen_coords:
                raise ValueError(f"Duplicate coordinates: {curr_coords} "
                                 f"for zone '{parts[0]}'")
            seen_coords.add(curr_coords)

        return self

    @staticmethod
    def _check_valid_zones(valid_zones: str) -> bool:
        if (" " in valid_zones or "-" in valid_zones or
                not isinstance(valid_zones, str)):
            return False
        return True

    @staticmethod
    def _check_zone_coords(coords: str) -> bool:
        try:
            int(coords)
            return True
        except ValueError:
            return False

    @staticmethod
    def _check_metada(metada: str, definition: str) -> List:
        error_list = []
        valid_zone_metadata = {"zone", "color", "max_drones"}
        valid_zone_type = {"normal", "blocked", "restricted", "priority"}
        duplicate_data: List[str] = []

        if not metada.startswith("["):
            error_list.append("Missing '[' at the start.")
        if not metada.endswith("]"):
            error_list.append("Missing ']' at the end.")

        metada = metada.strip("[]")
        metada_list = re.findall(r"\S+", metada)

        for m in metada_list:
            if "=" not in m:
                error_list.append(f"Missing '=' separator in {m}")
                continue

            key, value = m.split("=", 1)

            if definition == "zone":
                if key not in valid_zone_metadata:
                    error_list.append(f"{key} is not a valid tag.")
                    continue
            elif definition == "connection":
                if key != "max_link_capacity":
                    error_list.append(f"{key} is not a valid tag.")
                    continue

            if key == "zone":
                if value not in valid_zone_type:
                    error_list.append(f"'{key}={value}' is not a valid zone "
                                      "type. Use: 'normal', 'blocked', "
                                      "'restricted', 'priority'.")

            elif key in ["max_drones", "max_link_capacity"]:
                try:
                    n = int(value)
                    if n <= 0:
                        raise ValueError
                except ValueError:
                    error_list.append(f"'{key}={value}' need to be a positive "
                                      "valid int.")

            elif key == "color":
                if not isinstance(value, str):
                    error_list.append(f"'{key}={value}' is not a valid color.")

            if len(duplicate_data) > 0:
                if key in duplicate_data:
                    error_list.append(f"'duplicated key: {key}")
            duplicate_data.append(key)

        return error_list

    @staticmethod
    def _check_connection(connection_name: str, existing_connection: List[str],
                          valid_zones: List[str]) -> List:
        error_list = []

        if "-" not in connection_name:
            error_list.append("Missing '-' between zones name.")
            return error_list

        zone1, zone2 = connection_name.split("-", 1)

        if len(valid_zones) == 0:
            error_list.append("Define zones first.")
            return error_list

        if zone1 not in valid_zones:
            error_list.append(f"{zone1} not a valid zone name.")
        if zone2 not in valid_zones:
            error_list.append(f"{zone2} not a valid zone name.")

        if error_list:
            return error_list

        if connection_name in existing_connection:
            error_list.append(f"Duplicated connection: {connection_name}")

        return error_list
