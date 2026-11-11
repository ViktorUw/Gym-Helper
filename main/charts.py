import base64
from io import BytesIO

import matplotlib

matplotlib.use("Agg")  # render to images only; GUI backends break in server threads
import matplotlib.pyplot as plt  # noqa: E402


def line_chart(dates, values, unit="kg"):
    """A line chart as a base64 PNG for <img src="data:image/png;base64,...">.

    Colours match main/static/main/css/style.css (dark theme, yellow accent).
    """
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(dates, values, color="#f2b705", linewidth=2.5, marker="o", markersize=5)
    ax.set_ylabel(unit, color="#9ba1a9")
    ax.tick_params(colors="#9ba1a9")
    ax.grid(axis="y", color="#383c43", linewidth=0.8)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#383c43")
    fig.autofmt_xdate()
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True, dpi=150)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")
