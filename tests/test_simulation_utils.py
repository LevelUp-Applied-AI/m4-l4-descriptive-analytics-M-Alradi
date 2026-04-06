from utils.simulation_utils import false_positive_simulation


def test_false_positive_close_to_alpha():
    alpha = 0.05
    rate = false_positive_simulation(
        n_simulations=2000,
        alpha=alpha,
        random_state=42
    )

    assert abs(rate - alpha) < 0.02