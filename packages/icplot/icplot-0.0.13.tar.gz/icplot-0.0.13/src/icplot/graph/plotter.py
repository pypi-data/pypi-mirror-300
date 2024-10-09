from pathlib import Path

from icplot.color import ColorMap

from .plot import Plot


class Plotter:

    def __init__(self, cmap: ColorMap):
        self.cmap = cmap

    def apply_cmap_colors(self, plot: Plot):
        non_highlight = []
        for idx, series in enumerate(plot.series):
            if not series.highlight:
                non_highlight.append(series)

        for idx, series in enumerate(non_highlight):
            series.color = self.cmap.get_color(idx, non_highlight)

    def plot(self, plot: Plot, path: Path | None = None):
        pass
