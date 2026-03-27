# main.py
# runs all three scenarios with the same network topology and prints results.
# each scenario uses the same node positions and traffic, just a different AP.

from core.node import node
from core.simulation import simulation
from ap.standard_ap import standard_ap
from ap.mac_filter_ap import mac_filter_ap
from ap.adaptive_ap import adaptive_ap

DURATION_MS = 10000

def make_nodes():
    # two legitimate nodes positioned such that they can't hear each other
    # but both can reach the AP at (50, 50). this creates the hidden terminal scenario.
    node_a = node(mac="aa:aa:aa:aa:aa:aa", x=0,   y=50, tx_range=60, send_rate=500)
    node_b = node(mac="bb:bb:bb:bb:bb:bb", x=100, y=50, tx_range=60, send_rate=500)

    # attacker sends much more frequently and spoofs a new MAC each time
    attacker = node(mac="cc:cc:cc:cc:cc:cc", x=50, y=0, tx_range=60, send_rate=50, is_attacker=True)

    return [node_a, node_b, attacker]

def run_scenario(name, ap, nodes):
    print(f"\n--- {name} ---")
    sim = simulation(nodes, ap, DURATION_MS)
    sim.run()
    for k, v in ap.stats().items():
        print(f"  {k}: {v}")

def main():
    # reset nodes for each scenario so state doesn't carry over
    run_scenario("standard ap",     standard_ap(),          make_nodes())
    run_scenario("mac filter ap",   mac_filter_ap(),        make_nodes())

    # adaptive ap needs a reference to nodes for MCS broadcasts
    nodes = make_nodes()
    run_scenario("adaptive ap",     adaptive_ap(nodes),     nodes)

if __name__ == "__main__":
    main()
