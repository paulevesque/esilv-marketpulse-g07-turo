"""Dash presentation of the MarketPulse snapshot.

This file only displays what build_market_snapshot() returns. It does not
call a provider and it does not calculate anything.
"""

from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


app = Dash(__name__)
app.title = "MarketPulse"

snapshot = build_market_snapshot()

provider = snapshot["provider"]
if snapshot["access_mode"]:
    provider = f"{provider} - {snapshot['access_mode']}"

lookback = snapshot["lookback"]
interval = snapshot["interval"]

instrument = snapshot["instrument"]
benchmark = snapshot["benchmark"]

instrument_return = snapshot["instrument_return"]
benchmark_return = snapshot["benchmark_return"]
relative_performance = snapshot["relative_performance"]

instrument_base_100 = snapshot["instrument_base_100"]
benchmark_base_100 = snapshot["benchmark_base_100"]


PAGE_STYLE = {
    "fontFamily": "Arial, sans-serif",
    "maxWidth": "960px",
    "margin": "0 auto",
    "padding": "16px",
}
CARD_ROW_STYLE = {"display": "flex", "gap": "16px"}
CARD_STYLE = {
    "flex": "1",
    "border": "1px solid #cccccc",
    "borderRadius": "6px",
    "padding": "8px 16px",
}
VALUE_STYLE = {"fontSize": "24px", "fontWeight": "bold"}


def performance_card(title, value):
    return html.Div(
        [
            html.H3(title),
            html.P(value, style=VALUE_STYLE),
        ],
        style=CARD_STYLE,
    )


context = html.Div(
    [
        html.P(f"Provider: {provider}"),
        html.P(
            f"Instrument: "
            f"{instrument['ticker']} - {instrument['name']}"
        ),
        html.P(
            f"Benchmark: "
            f"{benchmark['ticker']} - {benchmark['name']}"
        ),
        html.P(f"Lookback: {lookback}"),
        html.P(f"Interval: {interval}"),
    ]
)

performance = html.Div(
    [
        performance_card(
            "Instrument Return",
            f"{instrument_return:+.2f}%",
        ),
        performance_card(
            "Benchmark Return",
            f"{benchmark_return:+.2f}%",
        ),
        performance_card(
            "Relative Performance",
            f"{relative_performance:+.2f} pts",
        ),
    ],
    style=CARD_ROW_STYLE,
)

figure = go.Figure()

for asset, base_100 in (
    (instrument, instrument_base_100),
    (benchmark, benchmark_base_100),
):
    figure.add_trace(
        go.Scatter(
            x=[row["date"] for row in base_100],
            y=[row["value"] for row in base_100],
            mode="lines",
            name=asset["ticker"],
        )
    )

figure.update_layout(
    title="Instrument vs Benchmark - Base 100",
    xaxis_title="Date",
    yaxis_title="Base 100",
)

app.layout = html.Div(
    [
        html.H1("MarketPulse"),
        html.P("Instrument vs Benchmark market comparison"),
        context,
        performance,
        dcc.Graph(figure=figure),
    ],
    style=PAGE_STYLE,
)


if __name__ == "__main__":
    app.run(debug=False)
