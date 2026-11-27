"""Dash presentation of MarketPulse.

The dashboard only displays the application snapshot built by
build_market_snapshot(). It does not call any provider and does not
calculate any return, base 100 or relative performance.

Run from the repository root:

    python src/dashboard.py
"""

import sys

from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


CARD_STYLE = {
    "border": "1px solid #d0d7de",
    "borderRadius": "6px",
    "padding": "8px 16px",
    "minWidth": "200px",
}


def build_context(snapshot):
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    return html.Div(
        [
            html.P(f"Provider: {snapshot['provider']}"),
            html.P(
                f"Instrument: {instrument['ticker']} - {instrument['name']}"
            ),
            html.P(
                f"Benchmark: {benchmark['ticker']} - {benchmark['name']}"
            ),
            html.P(f"Lookback: {snapshot['lookback']}"),
            html.P(f"Interval: {snapshot['interval']}"),
        ]
    )


def build_indicator(title, value):
    return html.Div([html.H3(title), html.P(value)], style=CARD_STYLE)


def build_performance(snapshot):
    return html.Div(
        [
            build_indicator(
                "Instrument Return",
                f"{snapshot['instrument_return']:+.2f}%",
            ),
            build_indicator(
                "Benchmark Return",
                f"{snapshot['benchmark_return']:+.2f}%",
            ),
            build_indicator(
                "Relative Performance",
                f"{snapshot['relative_performance']:+.2f} pts",
            ),
        ],
        style={"display": "flex", "gap": "16px", "flexWrap": "wrap"},
    )


def build_figure(snapshot):
    figure = go.Figure()

    for asset, series in (
        (snapshot["instrument"], snapshot["instrument_base_100"]),
        (snapshot["benchmark"], snapshot["benchmark_base_100"]),
    ):
        figure.add_trace(
            go.Scatter(
                x=[row["date"] for row in series],
                y=[row["value"] for row in series],
                mode="lines",
                name=asset["ticker"],
            )
        )

    figure.update_layout(
        title="Instrument vs Benchmark - Base 100",
        xaxis_title="Date",
        yaxis_title="Base 100",
    )

    return figure


def build_layout(snapshot):
    return html.Div(
        [
            html.H1("MarketPulse"),
            html.P("Instrument vs Benchmark market comparison"),
            build_context(snapshot),
            build_performance(snapshot),
            dcc.Graph(figure=build_figure(snapshot)),
        ],
        style={
            "fontFamily": "Arial, sans-serif",
            "maxWidth": "960px",
            "margin": "0 auto",
            "padding": "16px",
        },
    )


app = Dash(__name__)


if __name__ == "__main__":
    # Optional, as in main.py: "python src/dashboard.py yahoo" or "... csv".
    try:
        snapshot = build_market_snapshot(*sys.argv[1:2])
    except ValueError as error:
        sys.exit(str(error))

    app.layout = build_layout(snapshot)
    app.run(debug=False)
