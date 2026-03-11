# COMP4203 Final Project

A Python simulation for distinguishing DoS flooding attacks from hidden terminal collisions in 802.11 wireless networks.

## What it does

Simulates an Access Point managing two simultaneous problems:
- **DoS flooding** — an attacker spoofing random MACs to exhaust the AP's auth buffer
- **Hidden terminal collisions** — two nodes that can't hear each other causing packet collisions at the AP

Three AP variants are compared: standard, MAC filtering only, and an adaptive AP that handles both.

## References

- Elhigazi et al. — Authentication Flooding DOS Attack Detection and Prevention in 802.11 (IEEE SCOReD, 2020)
- Tamai et al. — Recognition and Countermeasure to Hidden Terminal Problem by Packet Analysis in Wireless LAN (IEEE, 2020)

### Authors 

Mohammad Rehman
Yacine Saoudi
Devanjali Das
