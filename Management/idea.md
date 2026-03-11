# Project Idea - Wireless Traffic Anomaly Detection

## The Idea

Simulate a wifi network and passively monitor the traffic. No packet injection, just observe. Detect when something abnormal is happening, like a node flooding the network, collisions caused by the hidden terminal problem, or a node suddenly sending way more traffic than usual.

Passive monitoring works here because it doesn't disturb the network, so behaviour stays natural. Anomalies get flagged in real time and shown visually in Python — network topology, packet flows, nodes highlighted when something gets detected.

All three anomaly types are wireless-specific. The hidden terminal problem doesn't exist in wired networks, and flooding attacks behave differently over wifi because of how CSMA/CA works at the MAC layer.

## Papers

### Paper 1

Unsupervised Wireless Spectrum Anomaly Detection With Interpretable Features
https://ieeexplore.ieee.org/document/8692627

Uses adversarial autoencoders to detect anomalies in wireless spectrum without needing labeled data. Can also localize where the anomaly is happening. Need to check the year.

### Paper 2

Machine Learning Approach for Detection of Flooding DoS Attacks in 802.11 Networks and Attacker Localization
https://link.springer.com/article/10.1007/s13042-014-0309-2

About flooding DoS in wifi, a node sends spoofed frames at an access point until it gets overwhelmed. Proposes an ML-based detection system. Directly relevant to the flooding scenario.

### Paper 3

Recognition and Countermeasure to Hidden Terminal Problem by Packet Analysis in Wireless LAN
https://ieeexplore.ieee.org/abstract/document/9023344/

Detects the hidden terminal problem through passive packet analysis. When two nodes can't hear each other and both transmit to the same receiver, collisions show up in the packet data. Also proposes a fix but we only really need the detection side of it.

### Paper 4

Authentication Flooding DoS Attack Detection and Prevention in 802.11
https://ieeexplore.ieee.org/document/9250990/

Background on flooding attacks at the MAC layer. Uses a filter buffer to detect authentication request floods.

## What we're simulating

Three scenarios:

1. Packet flooding — a node sends spoofed frames at the access point, legitimate nodes see higher delay and packet loss. Detect it by watching transmission rate and flagging when it goes well above the baseline.

2. Hidden terminal collisions — node A and node C are out of range of each other but both transmit to node B. B receives corrupted data. Detect it passively by monitoring retransmission rates and ACK failures, the pattern is distinct from normal packet loss.

3. Bursty traffic — a node suddenly sends much more data than usual. Use a change point detection algorithm to catch when the traffic distribution shifts.

## Metrics

Measure before and after injecting each anomaly:

- throughput
- packet loss rate
- end to end delay
- channel utilization
- collision rate
- detection latency (how long until the detector catches it)
- false positive rate

Compare our results against what the papers reported.

## Simulation plan

- nodes are objects with a position, transmission range, and packet queue
- before transmitting, a node checks if anyone in range is already transmitting and backs off if so (CSMA/CA approximation)
- hidden terminal scenario is created by placing nodes far enough apart that sensing ranges don't overlap, but they share a receiver
- passive monitor node sees all traffic and runs detection on the stream
- visualize with matplotlib and networkx — draw nodes, show packet flows, highlight anomalous nodes


### Paper 1 - Authentication Flooding DOS Attack Detection and Prevention in 802.11
https://ieeexplore.ieee.org/abstract/document/9023344/

### Problem Context:
// This would benefit from recreating or using Figure 2 from the paper
- Vulnerability: Problems happen when an attacker continuously sends fake authentication request packets to an Access Point (AP). The AP responds to all authentication request packets by sending an auth response, and puts the auth request into the unassociated buffer, which is the memory space for clients that haven't completed the full handshake after sending an auth request. In the buffer, an association request is awaited to complete the handshake. 
- The Attack: Because the 802.11 standard requires the AP to reserve memory for a client right after receiving the first auth request, the attacker uses this to his advantage by never finishing the handshake, thereby leaving entries in the memory pool that blocks legitimate users.
- Mac Spoofing: Attackers use MAC spoofing in DOS attacks because by generating numerous randomized and faked MAC addresses, they are able to bypass simple firewall blacklists which creates a need for a Filter that is dynamic and able to address large quantities of data effectively, which this paper provides

### Attempts to Address DOS Attacks: 
**(This can be expanded using Section 2, Related Work)**
- Protocol: the three security protocols set out by 802.11 for the protection of wireless infrastructure network, are Wired Equivalent Privacy (WEP), Wi-Fi protected access(WPA), and Wi-Fi Protected Access2 (WPA2) all suffer from DOS attacks. 802.11 focuses mainly on ensuring integrity and privacy and doesn't focus on availability
- Existing Algorithms: // Write about DRDA that the paper compares to

### Proposed Solution:
This paper proposes an algorithm for the detection and prevention of authentication request flood attacks, using a MAC filter buffer for the maintenance and filtering of MAC as well as buffer monitoring
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
### Evaluation & Results
- The proposed algorithm show 98.4% improved detection performance compared to standard AP management systems.

### Paper 2 - Recognition and Countermeasure to Hidden Terminal Problem by Packet Analysis in Wireless LAN
https://ieeexplore.ieee.org/document/9250990/

### Problem Context:
- CSMA/CA Overview: In WLAN, a Carrier Sense Multiple Access with Collision Avoidance (CSMA/CA) is used because it's suitable for the distributed wireless scheme in this scheme, before accessing the channel, the wireless terminal, known as a Station (STA), detects the signal using carrier sensing. Which is used for confirming access from the other terminal
- Random Backoff: To avoid simultaneous access between wireless terminals, a random waiting period is set up for spreading the access timing among them, known as a random backoff
- Hidden Terminal Problem: Carrier sensing detection can be interfered with if the power of a detected signal becomes small due to fading and shadow effect leading to multiple wireless terminals accessing the channel at the same time, causing packet collision

### Factors Decreasing Performance During Collissions
The paper notes three factors that decrease performance when collisions happen:
1) The first is retransmission of packets. in WLAN the maximal waiting period for deciding random backoff is extended exponentially with every transmission
2) Second is Adaptive Modulation and Coding Scheme. With WLAN lower Modulation and Coding Scheme (MCS) is selected the lower the quality of the comm link becomes. This lower MCS is selected if the packet fails, resulting in a slower but more robust modulation
3) Third is the Packet Length. Longer packets have more opportunities to collide between other wireless terminals. Lowering MCS makes the packet seem longer in that it takes more time to send the same amount of bits.

### Proposed Solution
- AP-Controlled MCS: The paper proposes that instead of letting a STA choose its MCS based on signal strength, the AP should instead monitor the collision rate. If the AP detects a Hidden Terminal scenario it commands the STAs to use a **higher order MCS** that has a faster transmission rate, and a **Low Coding rate** which has a high amount of redundant bits for every sent bit of data.
- Short Packet Effect: With a shorter packet length, the data per second rate is increased, but also the probability of packet collision becomes smaller, this is known as the short packet effect. The important thing to note is that it is important to avoid long "air time" for the packet, therefore even if a packet might be larger, the main focus is in reducing the transmission time
- In summary: The AP monitors collision rates, and when the AP detects a hidden terminal scenario, commands the STAs to use a faster transmission rate to minimize the collision window

### Evaluation & Results
- While a higher MCS is more sensitive to noise, the benefit of reducing collisions outweighs the risk of noise-related errors. Total throughput was increased an a large decrease in delay because the exponential backoff loop was avoided.
