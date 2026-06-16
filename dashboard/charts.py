import plotly.express as px

def score_chart(df):

    fig = px.line(
        df,
        x="scan_time",
        y="score",
        title="Score History"
    )

    return fig