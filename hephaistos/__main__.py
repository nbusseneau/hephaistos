#!/usr/bin/env python3
"""Hephaistos

CLI tool for patching any resolution in Supergiant Games' Hades, primarily
targeting ultrawide monitors (21:9, 32:9) and multi-monitors (48:9).

Hephaistos can bypass both pillarboxing and letterboxing, which are the default
on non-16:9 resolutions for Hades, and allows using custom resolutions (useful
for custom window sizes and multi-monitor without Eyefinity / Surround).

See README for usage examples or run:

- `python -m hephaistos` directly to enter interactive mode.
- `python -m hephaistos --help` for more information about the CLI commands.
"""
import logging

from hephaistos.cli import Hephaistos


logging.basicConfig()
Hephaistos()
