#!/bin/bash -e

PORTS = "4001 4002 4003"

for port in ${PORTS}; do
    systemctl stop hello_env@${port}
done

exit 0
