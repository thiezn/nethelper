#!/bin/bash

echo 'Metric Calculations'
echo '==================='
echo '1024 kbps'
curl -H "Content-Type: application/json" -X POST -d '{"kbps": 1024}' http://10.243.48.5:8081/api/v1/metrics/calculate
echo -e '\n\n1024 kbps non-rounded'
curl -H "Content-Type: application/json" -X POST -d '{"kbps": 1024, "round_to": null}' http://10.243.48.5:8081/api/v1/metrics/calculate
echo -e '\n\nIncorrect payload'
curl -H "Content-Type: application/json" -X POST -d '{"bla": null}' http://10.243.48.5:8081/metrics/calculate


echo -e '\n\nNetwork calculations'
echo '===================='
echo '10.0.0.0 bitmask 24'
curl -H "Content-Type: application/json" -X POST -d '{"network": "10.0.0.0", "bitmask": 24}' http://10.243.48.5:8081/api/v1/networks/calculate
echo -e '\n\n10.0.0.0 netmask 255.255.255.0'
curl -H "Content-Type: application/json" -X POST -d '{"network": "10.0.0.0", "netmask": "255.255.255.0"}' http://10.243.48.5:8081/api/v1/networks/calculate
echo -e '\n\n10.0.0.0/24'
curl -H "Content-Type: application/json" -X POST -d '{"network": "10.0.0.0/24"}' http://10.243.48.5:8081/api/v1/networks/calculate
echo -e '\n\nIncorrect payload'
curl -H "Content-Type: application/json" -X POST -d '{"bla": null}' http://10.243.48.5:8081/api/v1/networks/calculate


echo -e '\n\nMAC Address parsing'
echo '==================='
echo '00.11.22.33.44.55'
curl -H "Content-Type: application/json" -X POST -d '{"mac_address": "00.11.22.33.44.55"}' http://10.243.48.5:8081/api/v1/mac
echo -e '\n\n0011.2233.4455'
curl -H "Content-Type: application/json" -X POST -d '{"mac_address": "0011.2233.4455"}' http://10.243.48.5:8081/api/v1/mac
echo -e '\n\n00-11-22-33-44-55'
curl -H "Content-Type: application/json" -X POST -d '{"mac_address": "00-11-22-33-44-55"}' http://10.243.48.5:8081/api/v1/mac
echo -e '\n\n00:11:22:33:44:55'
curl -H "Content-Type: application/json" -X POST -d '{"mac_address": "00:11:22:33:44:55"}' http://10.243.48.5:8081/api/v1/mac
echo -e '\n\n001122334455'
curl -H "Content-Type: application/json" -X POST -d '{"mac_address": "001122334455"}' http://10.243.48.5:8081/api/v1/mac
echo -e '\n\nIncorrect payload'
curl -H "Content-Type: application/json" -X POST -d '{"bla": null}' http://10.243.48.5:8081/api/v1/mac

echo -e '\n\nPorts'
echo '====='
echo 'tcp/22'
curl -H "Content-Type: application/json" -X POST -d '{"port": 22, "protocol": "tcp"}' http://10.243.48.5:8081/api/v1/ports
echo -e '\n\nudp\21'
curl -H "Content-Type: application/json" -X POST -d '{"port": 21, "protocol": "udp"}' http://10.243.48.5:8081/api/v1/ports
echo -e '\n\nIncorrect payload'
curl -H "Content-Type: application/json" -X POST -d '{"bla": null}' http://10.243.48.5:8081/api/v1/ports

echo ''
