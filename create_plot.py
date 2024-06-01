import plotly.graph_objs as go

def create_plot(percentage_high_target, percentage_low_target):
    labels = ['High Target', 'Low Target']
    values = [percentage_high_target, percentage_low_target]

    trace = go.Bar(
        x=labels,
        y=values,
        marker=dict(
            color=['red' if v < 0 else 'green' for v in values]  # Color based on the sign of the percentage
        )
    )

    layout = go.Layout(
        title='Percentage Difference from Price Targets',
        yaxis=dict(title='Percentage Difference (%)')
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig.to_html(full_html=False)
