# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  run.py                                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/24 17:45:51 by roandrie        #+#    #+#               #
#  Updated: 2026/02/24 23:32:16 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
"""
Simple function to run the main script without using 'make run' and/or with
a custom map.
"""

import sys

from src.__main__ import main
from src.utils.ui import Display

if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        Display.error("\nProgram interrupted by user.")
        sys.exit(130)

    except Exception as e:
        Display.error(f"{e}")
        sys.exit(1)
