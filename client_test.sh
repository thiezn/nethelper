#!/bin/bash

echo 'Metric Calculations'
echo '==================='
echo '1024 kbps'
curl -H "Content-Type: application/json" -X POST -d '{"kbps": 1024}' http://10.243.48.5:8081/metrics/calculate
echo -e '\n\n1024 kbps non-rounded'
curl -H "Content-Type: application/json" -X POST -d '{"kbps": 1024, "round_to": null}' http://10.243.48.5:8081/metrics/calculate
echo -e '\n\nNetwork calculations'
echo '===================='
echo '10.0.0.0 bitmask 24'
curl -H "Content-Type: application/json" -X POST -d '{"network": "10.0.0.0", "bitmask": 24}' http://10.243.48.5:8081/networks/calculate
echo -e '\n\n10.0.0.0 netmask 255.255.255.0'
curl -H "Content-Type: application/json" -X POST -d '{"network": "10.0.0.0", "netmask": "255.255.255.0"}' http://10.243.48.5:8081/networks/calculate
echo -e '\n\n10.0.0.0/24'
curl -H "Content-Type: application/json" -X POST -d '{"network": "10.0.0.0/24"}' http://10.243.48.5:8081/networks/calculate
echo ''
