from pathlib import Path

from icplot.graph import Plot, LinePlotSeries
from icplot.graph.matplotlib import MatplotlibPlotter


def test_line_plot():

    data = [([0, 5, 10], [1, 2, 3]), ([0, 5, 10], [3, 6, 9]), ([0, 5, 10], [4, 8, 12])]

    series = []
    for idx, [x, y] in enumerate(data):
        series_config = {"label" : f"Series {idx}", "x" : x, "y" : y}
        series.append(LinePlotSeries(**series_config))
        
    plot_config = {"title": "test",
                   "legend_label" : "test_legend",
                   "series" : series,
                   "x_axis" : {"label" : "test_x",
                               "ticks" : {"lower" : 0,
                                          "upper" : 10,
                                          "step" : 5}}}

    plot = Plot(**plot_config)

    output_path = Path() / "output.svg"

    plotter = MatplotlibPlotter()
    plotter.plot(plot, output_path)

    assert output_path.exists()
    output_path.unlink()
