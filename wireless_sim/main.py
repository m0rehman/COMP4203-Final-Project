# main.py
# runs four scenarios comparing AP behavior under different network conditions.
# each scenario seeds the RNG so all three APs see identical traffic.

import random
from core.node import node
from core.simulation import simulation
from ap.standard_ap import standard_ap
from ap.mac_filter_ap import mac_filter_ap
from ap.adaptive_ap import adaptive_ap

DURATION_MS = 60000
SEED = 42


def make_hidden_terminal_nodes():
    # two legitimate nodes out of range of each other — the canonical hidden terminal scenario.
    node_a = node(mac="aa:aa:aa:aa:aa:aa", x=0,   y=50, tx_range=60, send_rate=1000)
    node_b = node(mac="bb:bb:bb:bb:bb:bb", x=100, y=50, tx_range=60, send_rate=1000)
    return [node_a, node_b]


def make_dos_only_nodes():
    # one legitimate node and one attacker, both within range of each other.
    # no hidden terminal effect — isolates the DoS detection problem.
    legitimate = node(mac="aa:aa:aa:aa:aa:aa", x=0,  y=0, tx_range=200, send_rate=1000)
    attacker   = node(mac="ee:ee:ee:ee:ee:ee", x=50, y=0, tx_range=200, send_rate=20, is_attacker=True)
    return [legitimate, attacker]


def make_combined_nodes():
    # four legitimate nodes forming multiple hidden terminal pairs (a-b, c-d, a-d, b-c)
    # plus one attacker. attacker bypasses CSMA/CA so its position doesn't affect
    # the hidden terminal dynamics.
    node_a   = node(mac="aa:aa:aa:aa:aa:aa", x=0,   y=50,  tx_range=60, send_rate=200)
    node_b   = node(mac="bb:bb:bb:bb:bb:bb", x=100, y=50,  tx_range=60, send_rate=200)
    node_c   = node(mac="cc:cc:cc:cc:cc:cc", x=0,   y=100, tx_range=60, send_rate=200)
    node_d   = node(mac="dd:dd:dd:dd:dd:dd", x=100, y=100, tx_range=60, send_rate=200)
    attacker = node(mac="ee:ee:ee:ee:ee:ee", x=50,  y=75,  tx_range=60, send_rate=20, is_attacker=True)
    return [node_a, node_b, node_c, node_d, attacker]


def make_stress_nodes():
    # six legitimate nodes in two columns 100 apart — every cross-column pair
    # is a hidden terminal (distance >= 100, range 60). same-column pairs can
    # hear each other (distance 50, range 60).
    node_a    = node(mac="aa:aa:aa:aa:aa:aa", x=0,   y=50,  tx_range=60, send_rate=200)
    node_b    = node(mac="bb:bb:bb:bb:bb:bb", x=100, y=50,  tx_range=60, send_rate=200)
    node_c    = node(mac="cc:cc:cc:cc:cc:cc", x=0,   y=100, tx_range=60, send_rate=200)
    node_d    = node(mac="dd:dd:dd:dd:dd:dd", x=100, y=100, tx_range=60, send_rate=200)
    node_e    = node(mac="ff:ff:ff:ff:ff:ff", x=0,   y=150, tx_range=60, send_rate=200)
    node_f    = node(mac="11:11:11:11:11:11", x=100, y=150, tx_range=60, send_rate=200)
    attacker1 = node(mac="22:22:22:22:22:22", x=50,  y=75,  tx_range=60, send_rate=20, is_attacker=True)
    attacker2 = node(mac="33:33:33:33:33:33", x=50,  y=125, tx_range=60, send_rate=20, is_attacker=True)
    return [node_a, node_b, node_c, node_d, node_e, node_f, attacker1, attacker2]


def run_scenario(name, ap, nodes):
    print(f"\n--- {name} ---")
    sim = simulation(nodes, ap, DURATION_MS)
    sim.run()
    for k, v in ap.stats().items():
        print(f"  {k}: {v}")
    return ap.stats()


def run_scenario_group(name, make_nodes_fn):
    print(f"\n=== {name} ===")

    random.seed(SEED)
    std_stats = run_scenario("standard ap",   standard_ap(),       make_nodes_fn())

    random.seed(SEED)
    mac_stats = run_scenario("mac filter ap", mac_filter_ap(),     make_nodes_fn())

    random.seed(SEED)
    nodes = make_nodes_fn()
    ada_stats = run_scenario("adaptive ap",   adaptive_ap(nodes),  nodes)

    return [
        ("Standard AP",   std_stats),
        ("MAC Filter AP", mac_stats),
        ("Adaptive AP",   ada_stats),
    ]


def main():
    results = {
        "Scenario 1\nHidden Terminals": run_scenario_group("scenario 1: hidden terminals only", make_hidden_terminal_nodes),
        "Scenario 2\nDoS Only":         run_scenario_group("scenario 2: dos attack only",       make_dos_only_nodes),
        "Scenario 3\nCombined":         run_scenario_group("scenario 3: combined",              make_combined_nodes),
        "Scenario 4\nStress Test":      run_scenario_group("scenario 4: stress test",           make_stress_nodes),
    }

    from visualize import plot
    plot(results)


if __name__ == "__main__":
    main()