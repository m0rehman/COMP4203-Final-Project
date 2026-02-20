# COMP4203 Final Project

### Paper 1:
Authentication Flooding DOS Attack Detection and Prevention in 802.11
https://ieeexplore.ieee.org/abstract/document/9023344/

The Problem:
// This would benefit from recreating or using Figure 2 from the paper
Problems happen when an attacker continuously sends fake authentication request packets to an Access Point (AP). The AP responds to all authentication request packets by sending an auth response, and puts the auth request into the unassociated buffer, which is the memory space for clients that haven't completed the full handshake after sending an auth request. In the buffer, an association request is awaited to complete the handshake. Because the 802.11 standard requires the AP to reserve memory for a client right after receiving the first auth request, the attacker uses this to his advantage by never finishing the handshake, thereby leaving entries in the memory pool that blocks legitimate users.

Attackers use MAC spoofing in DOS attacks because by generating numerous randomized and faked MAC addresses, they are able to bypass simple firewall blacklists which creates a need for a Filter that is dynamic and able to address large quantities of data effectively, which this paper provides

Attempts to Address DOS Attacks: (This can be expanded using Section 2, Related Work)
Several algorithms have been proposed to detected and prevent DOS attacks in WLANs:
- the three security protocols set out by 802.11 for the protection of wireless infrastructure network, are Wired Equivalent Privacy (WEP), Wi-Fi protected access(WPA), and Wi-Fi Protected Access2 (WPA2) all suffer from DOS attacks
- 802.11 focuses mainly on ensuring integrity and privacy and doesn't focus on availability

This paper proposes an algorithm for the detection and prevention of authentication request flood attacks, using a MAC filter buffer for the maintenance and filtering of MAC as well as buffer monitoring
Results show 98.4% improved detection performance

Main Idea:
- Introduce a new MAC filtering buffer for receiving authentication packets while using the counter to maintain the filtering buffer
- Additionally introduce a thread to monitor the filter MAC

The Solution is in Three Components:

1) Adding a Filter MAC Buffer: The aim is to add a new check for the received auth packets which drops packets that if the sender's MAC is already present in the buffer

2) Maintaining Filter Mac: Once an auth request is received, it is verified in the filter MAC, 
	1) if the sender is not in the filter MAC, an auth response gets sent, then the MAC address is added to the MAC buffer
	2) If the address is present in the buffer, the counter is incremented instead

1) Monitoring Thread: A new thread is introduced to monitor the filter MAC and the MAC buffer
	1) every 3 seconds, it decrements the count of the MAC Buffer
	2) If it finds any MAC in the MAC Buffer with a count greater than 5, this means it has received more than 5 auth requests in 3 sec
	3) This is unusual behaviour and the sender MAC is added to the filter MAC

// More detail can be added to compare to the DRDA algorithm as the paper presents.


Mohammad Rehman  
Devanjali Das  
Yacine Saoudi  
