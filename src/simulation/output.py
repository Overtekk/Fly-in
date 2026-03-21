# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  output.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 14:35:34 by roandrie        #+#    #+#               #
#  Updated: 2026/03/21 16:10:28 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import os

from typing import Dict, List
from pathlib import Path

from src.utils.ui import Display


class LogOutput():
    def __init__(self, map_name: str, logs: Dict[int, List[str]]) -> None:
        self.logs = logs
        self.root = Path("output")
        self.map_name = map_name

        self._create_folder()

    def write_log(self) -> None:
        try:
            with open(f"{self.root}/{self.map_name}", "w") as f:
                for log_list in self.logs.values():
                    log_line = ""
                    for log in log_list:
                        log_line += f"{log} "
                        f.write(f"{log_line}")
                    f.write("\n")
        except PermissionError:
            Display.error("Can't write logs. Permissions denied to write in "
                          "the 'output' folder")

    def _create_folder(self) -> None:
        if not self.root.exists() or not self.root.is_dir():
            os.makedirs("output")
