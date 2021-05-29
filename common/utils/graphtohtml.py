import plotly.express as px

class DataToGraphUtils:

    def plot_daywise(data,col):
        fig = px.line(data, x="Date mutation", y=col, width=700,
                      line_shape='spline')
        return fig.to_html()