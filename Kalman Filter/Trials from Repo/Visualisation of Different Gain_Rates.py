"""Simple constant-drift + proportional-correction estimator demo.

Adds verbose debugging so you can see exactly how gain_rate (the assumed
constant daily drift) affects the prediction before the measurement update.
scale_factor is the fraction of the residual (measurement - prediction)
you apply as a correction (a fixed, ad‑hoc 'filter gain').
"""

from dataclasses import dataclass
from typing import List, Iterable, Dict, Any

# weights = [
#     158.0, 164.2, 160.3, 159.9, 162.1, 164.6,
#     169.6, 167.4, 166.4, 171.0, 171.2, 172.6
# ]

weights = [
    100, 97, 103,100, 97, 103,100, 97, 103,100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
]

time_step = 1  # days
scale_factor = 0.4  # measurement incorporation gain


@dataclass
class StepRecord:
    idx: int
    measurement: float
    prev_estimate: float
    predicted: float
    drift_applied: float
    residual: float
    correction: float
    new_estimate: float


def prediction_using_gain(estimated_weight: float, gain_rate: float, do_print: bool = True) -> List[StepRecord]:
    """Run the simple filter and optionally print a detailed table.

    gain_rate: assumed constant daily change (drift) added each step BEFORE
               applying the measurement correction.
    Returns list of StepRecord for further analysis / plotting.
    """
    history: List[StepRecord] = []

    if do_print:
        print(f"Running with gain_rate (assumed drift per day) = {gain_rate}\n")
        header = (
            f"{'i':>2}  {'meas':>6}  {'prev':>6}  {'pred':>6}  {'drift':>6}  "
            f"{'resid':>7}  {'corr':>7}  {'new':>6}"
        )
        print(header)
        print('-' * len(header))

    for i, measurement in enumerate(weights, start=1):
        prev_estimate = estimated_weight
        drift = gain_rate * time_step
        predicted_weight = prev_estimate + drift  # prediction step (apply drift)
        residual = measurement - predicted_weight  # innovation
        correction = scale_factor * residual       # how much we adjust
        estimated_weight = predicted_weight + correction  # updated estimate

        rec = StepRecord(
            idx=i,
            measurement=measurement,
            prev_estimate=prev_estimate,
            predicted=predicted_weight,
            drift_applied=drift,
            residual=residual,
            correction=correction,
            new_estimate=estimated_weight,
        )
        history.append(rec)

        if do_print:
            print(
                f"{i:>2}  {measurement:6.1f}  {prev_estimate:6.2f}  {predicted_weight:6.2f}  "
                f"{drift:6.2f}  {residual:7.2f}  {correction:7.2f}  {estimated_weight:6.2f}"
            )

    return history


def compare_gain_rates(initial_estimate: float, gain_rates: Iterable[float]) -> Dict[float, List[StepRecord]]:
    """Run the filter for several gain_rates and return histories.

    Helpful to see how too-small or too-large drift assumptions bias results.
    Printing is suppressed; you can add custom logic or plotting later.
    """
    results: Dict[float, List[StepRecord]] = {}
    for g in gain_rates:
        results[g] = prediction_using_gain(initial_estimate, g, do_print=False)
    return results


def summarize_bias(history: List[StepRecord]):
    residuals = [r.residual for r in history]
    mean_resid = sum(residuals)/len(residuals)
    print(f"\nResidual mean (should be ~0 if no bias): {mean_resid:.3f}")
    print(f"Residual min/max: {min(residuals):.2f}/{max(residuals):.2f}")


def demo():
    initial_estimate = 160.0
    hist = prediction_using_gain(initial_estimate, gain_rate=1.0, do_print=True)
    summarize_bias(hist)

    # Example comparison (uncomment if you want to quickly inspect summaries)
    # multi = compare_gain_rates(initial_estimate, [-0.5, 0.0, 0.5, 1.0, 2.0])
    # for g, hist in multi.items():
    #     print(f"\nGain rate {g}: final estimate {hist[-1].new_estimate:.2f}")

    # Optional quick plot (only if matplotlib is available)
    try:
        import matplotlib.pyplot as plt  # type: ignore
        g_examples = [-0.5, 0.0, 0.5, 1.0, 1.5, 2, 2.5]
        comp = compare_gain_rates(160.0, g_examples)
        plt.figure(figsize=(7, 4))
        plt.plot(weights, 'k--o', label='Measurement')
        for g in g_examples:
            plt.plot([r.new_estimate for r in comp[g]], label=f'est g={g}')
        plt.title('Effect of gain_rate (assumed drift)')
        plt.xlabel('Step')
        plt.ylabel('Weight')
        plt.legend()
        plt.tight_layout()
        plt.show()
    except Exception:
        pass  # plotting is optional


if __name__ == "__main__":
    demo()