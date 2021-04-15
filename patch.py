#!/usr/bin/env python3

from pathlib import Path
import re

regex = re.compile(b'(\xc7\x05.{4})\x80\x07\x00\x00')
data = Path('x64/EngineWin64s.dll').read_bytes()
patched = regex.sub(b'\g<1>\x20\x0a\x00\x00', data)
Path('x64/EngineWin64s.dll.patch').write_bytes(patched)
