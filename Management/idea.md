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
