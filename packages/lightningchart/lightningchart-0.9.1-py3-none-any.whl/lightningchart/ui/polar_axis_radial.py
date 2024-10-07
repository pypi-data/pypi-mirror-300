from __future__ import annotations

import lightningchart
from lightningchart.ui.polar_axis import PolarAxis

class PolarAxisRadial(PolarAxis):
    """Class representing the radial axis in a polar chart."""

    def __init__(self, chart):
        super().__init__(chart)
        self.instance.send(self.id, 'addPolarAxisRadial', {'chart': self.chart.id})

    def set_division(self, sections_count: int):
        """Set how many sections the Radial Axis is divided into by Ticks.

        Args:
            sections_count: Amount of sections.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDivision', {'sectionsCount': sections_count})
        return self

    def set_clockwise(self, clockwise: bool):
        """Set whether PolarAxisRadial direction is clockwise or counterclockwise.

        Args:
            clockwise: True for clockwise direction, False for counterclockwise.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setClockwise', {'clockwise': clockwise})
        return self

    def set_north(self, angle: int):
        """Set rotation of Radial Axis by specifying degree angle that is depicted at North position (horizontally centered, vertically highest).

        Args:
            angle: Angle as degrees that will be depicted at North position. Defaults to 90.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setNorth', {'angle': angle})
        return self
