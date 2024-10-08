#!/bin/bash
# Run python-caldav tests against Xandikos.
set -e

. $(dirname $0)/common.sh

BRANCH=master
PYCALDAV_REF=v1.2.1

if [ ! -d $(dirname $0)/pycaldav ]; then
    git clone --branch $PYCALDAV_REF https://github.com/python-caldav/caldav $(dirname $0)/pycaldav
else
    pushd $(dirname $0)/pycaldav
    git fetch origin
    git reset --hard $PYCALDAV_REF
    popd
fi

cat <<EOF>$(dirname $0)/pycaldav/tests/conf_private.py
# Only run tests against my private caldav servers.
only_private = True

caldav_servers = [
    {'url': 'http://localhost:5233/',
     # Until recurring support is added in xandikos.
     # See https://github.com/jelmer/xandikos/issues/102
     'incompatibilities': ['no_expand', 'no_recurring', 'no_scheduling', 'text_search_not_working'],
    }
]
EOF

run_xandikos 5233 5234 --defaults

pushd $(dirname $0)/pycaldav
${PYTHON:-python3} -m pytest tests "$@"
popd
