# IPv4FileCompare
Simple script which compare two files one with networks, second with ip addresses. 
Return grouped subnets based on ip addresses. 

## Authors
	Ireneusz Wolny
	Wojciech Wolny
		


# FLAGS:
    -h --help: print help
    
	--not-match: return list of not matched ip addresses 
	OUTPUT
		*-*-*-* Not matched *-*-*-*
            1 : 182.123.123.32/32
            2 : 55.54.53.0/30

	--match: return grouped addresses
	OUTPUT: 
		*-*-*-* 10.0.0.0/24 *-*-*-*
            1 : 10.0.0.1/32
            2 : 10.0.0.6/32
            3 : 10.0.0.8/32
            4 : 10.0.0.9/32
            5 : 10.0.0.4/30
		*-*-*-* 192.168.2.0/24 *-*-*-*
  
	--not-empty: skip empty group networks  
	
	--json: return json representation of results
	
	--file={file_name}: print results to file with given name, don't overwrite file if exists
  
# EXAMPLE OF USE: 
Networsk file contain only list of networks and masks, separated by new line. 
Ipaddresses file contain only list of networks and masks or ip addresses, separated by new line.

	./network_recognision.py networks ipaddresses

## OUTPUT: 
	*-*-*-* Not matched *-*-*-*
	1 : 182.123.123.32/32
	*-*-*-* 10.0.0.0/24 *-*-*-*
    1 : 10.0.0.1/32
    2 : 10.0.0.6/32
    3 : 10.0.0.8/32
    4 : 10.0.0.9/32
    5 : 10.0.0.4/30
	*-*-*-* 192.168.2.0/24 *-*-*-*
