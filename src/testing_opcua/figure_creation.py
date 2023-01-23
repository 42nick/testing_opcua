import plotly.graph_objects as go


def get_gauge_chart(val=21, desc: str = "", mmin: float = 0.0, mmax: float = 100.0):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=val,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": desc},
            gauge={"axis": {"range": [mmin, mmax]}},
        )
    )
    return fig
