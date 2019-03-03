# IPv4FileCompare
Simple script which compare two files with ip addresses or networks. Return grouped addresses or subnets.<br/>
Script required two files with ips or networks. Support only IPv4. <br/>
<br/>
# FLAGS:
	--not-match: return list of not matched ip addresses 
	OUTPUT
		*-*-*-* Not matched *-*-*-*
		1 : 182.123.123.32 is host address
		2 : 55.54.53.0/30 is subnet

	--match: return grouped addresses
	OUTPUT: 
		*-*-*-* 10.0.0.0/24 *-*-*-*
		1 : 10.0.0.1 is host address
		2 : 10.0.0.6 is host address
		3 : 10.0.0.8 is host address
		4 : 10.0.0.9 is host address
		5 : 10.0.0.4/30 is subnet
		*-*-*-* 192.168.2.0/24 *-*-*-*
  
	--not-empty: skip empty group networks
  
# EXAMPLE OF USE: 
Networsk file contain only list of networks and masks, separated by new line. 
Ipaddresses file contain only list of networks and masks or ip addresses, separated by new line.

	./network_recognision.py networks ipaddresses

## OUTPUT: 
	*-*-*-* Not matched *-*-*-*
	1 : 182.123.123.32 is host address
	*-*-*-* 10.0.0.0/24 *-*-*-*
	1 : 10.0.0.1 is host address
	2 : 10.0.0.6 is host address
	3 : 10.0.0.8 is host address
	4 : 10.0.0.9 is host address
	5 : 10.0.0.4/30 is subnet
	*-*-*-* 192.168.2.0/24 *-*-*-*
