"""MarketPulse Dash dashboard.

Presentation only: every value comes from build_market_snapshot().
No provider call and no analytical formula belong in this file.

Run from the repository root:
    python src/dashboard.py
"""

from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


snapshot = build_market_snapshot()

provider = snapshot["provider"]
lookback = snapshot["lookback"]
interval = snapshot["interval"]

instrument = snapshot["instrument"]
benchmark = snapshot["benchmark"]

instrument_return = snapshot["instrument_return"]
benchmark_return = snapshot["benchmark_return"]
relative_performance = snapshot["relative_performance"]

instrument_base_100 = snapshot["instrument_base_100"]
benchmark_base_100 = snapshot["benchmark_base_100"]


CARD_STYLE = {
    "border": "1px solid #d0d7de",
    "borderRadius": "8px",
    "padding": "8px 20px",
    "minWidth": "180px",
}


def indicator(title, value):
    return html.Div(
        [
            html.H3(title),
            html.P(value, style={"fontSize": "24px", "fontWeight": "bold"}),
        ],
        style=CARD_STYLE,
    )


def base_100_trace(series, asset):
    return go.Scatter(
        x=[row["date"] for row in series],
        y=[row["value"] for row in series],
        mode="lines",
        name=asset["ticker"],
    )


context = html.Div(
    [
        html.P(f"Provider: {provider}"),
        html.P(f"Instrument: {instrument['ticker']} - {instrument['name']}"),
        html.P(f"Benchmark: {benchmark['ticker']} - {benchmark['name']}"),
        html.P(f"Lookback: {lookback}"),
        html.P(f"Interval: {interval}"),
    ]
)

performance = html.Div(
    [
        indicator("Instrument Return", f"{instrument_return:+.2f}%"),
        indicator("Benchmark Return", f"{benchmark_return:+.2f}%"),
        indicator("Relative Performance", f"{relative_performance:+.2f} pts"),
    ],
    style={"display": "flex", "gap": "16px", "flexWrap": "wrap"},
)

figure = go.Figure()
figure.add_trace(base_100_trace(instrument_base_100, instrument))
figure.add_trace(base_100_trace(benchmark_base_100, benchmark))
figure.update_layout(
    title="Instrument vs Benchmark - Base 100",
    xaxis_title="Date",
    yaxis_title="Base 100",
)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("MarketPulse"),
        html.P("Instrument vs Benchmark market comparison"),
        context,
        performance,
        dcc.Graph(figure=figure),
    ],
    style={"fontFamily": "sans-serif", "margin": "24px"},
)


if __name__ == "__main__":
    app.run(debug=False)
