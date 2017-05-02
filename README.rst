NetHelper
~~~~~~~~~

REST API for retrieving information on ip and mac addresses

Information retrieval
=====================

IPv6 bitmask to netmask conversion (Some vendors *cough*F5*cough* want you to use the netmask notation!!)
MAC address vendor lookup
private/public/multicast/anycast network checks
Azure networks per region
Special ip addresses like OSPF, HSRP, BGP multicast stuff
Golden networks
Well known blacklists
Well known whitelists
TOR exit node IP lists?
information on TCP/UDP/ICMP headers perhaps? not sure what I would want but would be cool if we can use scapy! :D
Known vpn adress lists(or perhaps using a portscan, fingerprinting something to detect)
Common port lists through API


Function calls
==============
- Summarization of given list of networks
- Convert Mbps/kbps/bps/kBps/etc
- simple postscan (Dangerous waters here...?)


Brain dump of all kinds of stuff I want to do but probably will never get around to
===================================================================================
- REST API rate limiting to avoid DDOS attacks and make some money from heavy users
- Deployment to cloud provider utilising CDN network and different regions for resiliency
- Nice web frontend for some of the common features of the Api
- Api authentication for instance using tokens
- Database for maintaining users of the Api, amount of calls per day, etc. use https://github.com/magicstack/asyncpg
- Extensive documentation using sphinx
- unit tests
- coverage.py
