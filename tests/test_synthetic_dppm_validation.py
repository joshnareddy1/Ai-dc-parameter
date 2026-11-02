from dcopt.synthetic_dppm_validation import upper_dppm


def test_zero_event_upper_bound_passes_50_dppm_at_60000_devices():
    assert upper_dppm(0, 60000, 0.95) < 50


def test_zero_event_upper_bound_fails_at_current_holdout_volume():
    assert upper_dppm(0, 8820, 0.95) > 50
