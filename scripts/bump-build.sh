#!/bin/sh
# Bump the local test number: MAJOR.MINOR.BUILD → BUILD + 1.
# The first two numbers stay unchanged.
# Called once each time caldbg-ag runs.
# Packaging uses Cursor /build and does not call this script.
# Release bumps go through /upgrade-version and keep this number.
set -eu
root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
exec python3 - "$root" << 'PY'
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
version_path = root / 'version.py'
init_path = root / '__init__.py'
setup_path = root / 'setup.py'

version_src = version_path.read_text(encoding='utf-8')
match = re.search(r'^VERSION = \(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', version_src, re.M)
if match is None:
    sys.exit('VERSION not found in version.py')
major, minor, build = (int(part) for part in match.groups())
build += 1
tuple_text = '(%d, %d, %d)' % (major, minor, build)
new = '%d.%d.%d' % (major, minor, build)

version_src, count = re.subn(
    r'^VERSION = \(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)',
    'VERSION = %s' % tuple_text,
    version_src,
    count=1,
    flags=re.M,
)
if count != 1:
    sys.exit('VERSION not found in version.py')
version_path.write_text(version_src, encoding='utf-8')

init_src = init_path.read_text(encoding='utf-8')
init_src, count = re.subn(
    r'^VERSION = \(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)',
    'VERSION = %s' % tuple_text,
    init_src,
    count=1,
    flags=re.M,
)
init_src, plugin_count = re.subn(
    r'^(    version\s*=\s*)\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)',
    r'\g<1>%s' % tuple_text,
    init_src,
    count=1,
    flags=re.M,
)
if count != 1 or plugin_count != 1:
    sys.exit('VERSION or AskAIPlugin.version not found in __init__.py')
init_path.write_text(init_src, encoding='utf-8')

setup_src = setup_path.read_text(encoding='utf-8')
setup_src, count = re.subn(
    r"version='\d+\.\d+\.\d+'",
    "version='%s'" % new,
    setup_src,
    count=1,
)
if count != 1:
    sys.exit("version='X.Y.Z' not found in setup.py")
setup_path.write_text(setup_src, encoding='utf-8')
print(new)
PY
