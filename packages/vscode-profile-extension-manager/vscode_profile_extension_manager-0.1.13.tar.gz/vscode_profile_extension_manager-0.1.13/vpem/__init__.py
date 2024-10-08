# Copyright (c) 2024 JP Hutchins
# SPDX-License-Identifier: Apache-2.0

from appdirs import user_config_dir
import os

CONFIG_DIR = user_config_dir("vpem")
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

ALL_EXTENSION_DETAILS = os.path.join(CONFIG_DIR, "vscode-extensions-with-desc.json")
EXTENSION_GROUPS = os.path.join(CONFIG_DIR, "vscode-extensions-groups.json")

__version__ = '0.1.13'
