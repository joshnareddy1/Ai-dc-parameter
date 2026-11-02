import pandas as pd

from dcopt.predictive import FEATURES, clopper_pearson_upper, interval_inside_limits


def test_features_never_include_labels() -> None:
    prohibited = {"is_latent_defect_truth", "sort_pass", "burnin_fail", "rma", "first_fail_test"}
    assert prohibited.isdisjoint(FEATURES)


def test_interval_must_fit_both_margins() -> None:
    lower = pd.Series([4.6, 4.0])
    upper = pd.Series([4.4, 5.0])
    inside = interval_inside_limits(lower, upper, 0.0, 5.0, 0.10)
    assert inside.tolist() == [True, False]


def test_clopper_pearson_upper_is_bounded() -> None:
    upper = clopper_pearson_upper(0, 100, 0.95)
    assert 0.0 <= upper <= 1.0


def test_unique_failure_guard_forces_run() -> None:
    from dcopt.predictive import apply_unique_fail_guard

    train = pd.DataFrame({"A_PF": ["F", "P"], "B_PF": ["P", "F"]})
    catalog = pd.DataFrame({"test": ["A", "B"]})
    skip = pd.Series([True, True], index=train.index)
    assert apply_unique_fail_guard(skip, train, "A", catalog).tolist() == [False, False]


def test_unique_failure_guard_keeps_safe_candidate_decisions() -> None:
    from dcopt.predictive import apply_unique_fail_guard

    train = pd.DataFrame({"A_PF": ["F", "P"], "B_PF": ["F", "P"]})
    catalog = pd.DataFrame({"test": ["A", "B"]})
    skip = pd.Series([True, False], index=train.index)
    assert apply_unique_fail_guard(skip, train, "A", catalog).tolist() == [True, False]
