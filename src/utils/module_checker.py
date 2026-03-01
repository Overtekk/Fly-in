# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  module_checker.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/01 18:03:34 by roandrie        #+#    #+#               #
#  Updated: 2026/03/01 18:11:51 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
"""Runtime dependency verification utility.

This module provides a mechanism to check for the existence of required
third-party libraries before the main application attempts to import them,
ensuring a clean error message instead of an import crash.
"""

import importlib.util


def module_checker() -> None:
    """Verifies that all required third-party dependencies are installed.

    Iterates through a strict list of required packages and attempts to
    locate their specifications using `importlib`. This prevents the
    application from crashing with a standard ImportError later on.

    Raises:
        ModuleNotFoundError: If a required package is not found in the current
                             environment.
    """

    required = ['pydantic']
    missing = []

    for module_name in required:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            missing.append(spec)

    if missing:
        raise ModuleNotFoundError(f"missing dependencies {len(missing)}.\nUse "
                                  "'uv run python3 run.py <map>' instead.")
