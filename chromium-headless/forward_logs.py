#!/usr/bin/env python3
"""Run Chromium and forward logs to Sentry.

This script executes Chromium with provided command line arguments and
forwards its stdout and stderr streams into Python logging so they are
shipped to Sentry when DSN is configured.
"""
import os
import sys
import subprocess
import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

DSN = os.getenv("SENTRY_DSN")
ENV = os.getenv("SENTRY_ENV", "development")

if DSN:
    sentry_sdk.init(
        dsn=DSN,
        environment=ENV,
        integrations=[LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)],
    )

LOGGER = logging.getLogger("chromium")
LOGGER.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter("%(message)s"))
LOGGER.addHandler(handler)

# Start chromium and relay its output line by line.
process = subprocess.Popen(
    sys.argv[1:],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)

for line in process.stdout:
    LOGGER.info(line.rstrip())

process.wait()
sys.exit(process.returncode)
