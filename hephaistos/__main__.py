#!/usr/bin/env python3
"""Hephaistos

CLI tool for patching any resolution in Supergiant Games' Hades, initially
intended as an ultrawide support mod.
It can bypass both pillarboxing and letterboxing, which are the default on
non-16:9 resolutions for Hades.

See README for usage examples or run `hephaistos --help` for more information
about the available commands.
"""
import logging

from hephaistos.cli import Hephaistos

logging.basicConfig()
Hephaistos()
