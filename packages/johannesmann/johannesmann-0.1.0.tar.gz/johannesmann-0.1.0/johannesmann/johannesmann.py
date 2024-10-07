"""Main module."""
from __future__ import annotations

import numpy as np

from dataclasses import dataclass
from numpy.typing import NDArray

__all__ = ['Line', 'Node', 'Tessellation']


@dataclass
class Line:
    """Class to represent a line.

    Args:
        y_0: Y-intercept of the line.
        slope: Slope of the line.
    """
    y_0: float
    slope: float

    def above(self, x: float, y: float) -> bool:
        """Check if a given point is above the line.

        Args:
            x: X-Coordinate of the point.
            y: Y-Coordinate of the point.

        Returns:
            True if the point is above the line.
        """
        return y > self.y_0 + x * self.slope


@dataclass
class Node:
    """Node for a binary tree to realise space partitioning.

    Args:
        line: Line object.
        above: Node with lines in the space above the line in this node.
        below: Node with lines in the space below the line in this node.
    """
    line: Line
    above: Node = None
    below: Node = None


class Tessellation:
    """Class to realise the Johannesmann Spatial Tessellation on a given
    rectangular region.
    """

    def __init__(self, x_range: float, y_range: float, cuts: int) -> None:
        """Class constructor.

        Args:
            x_range: Range to tessellate in x direction.
            y_range: Range to tessellate in y direction.
            cuts: Number of cuts.
        """
        self.x_range = x_range
        self.y_range = y_range

        self.lines = None

        for _ in range(cuts):
            # Random point in range
            x = (np.random.rand() - 0.5) * self.x_range
            y = (np.random.rand() - 0.5) * self.y_range
            # Random slope
            slope = np.tan((np.random.rand() - 0.5) * np.pi)

            if self.lines is None:
                self.lines = Node(Line(
                    y_0=y - slope * x,
                    slope=slope
                ))
            else:
                self.attach_node(
                    self.lines, x, y,
                    Line(y_0=y - slope * x, slope=slope)
                )

    def attach_node(self, node: Node, x: float, y: float, line: Line):
        """Recursivity search the binary tree and attach a new node with a
        line.

        Args:
            node: Node to check or search the children of.
            x: X-Coordinate of the point defining origin of the new line.
            y: Y-Coordinate of the point defining origin of the new line.
            line: Line of the new node to attach to the tree.
        """
        if node.line.above(x, y):
            if node.above is None:
                node.above = Node(line)
            else:
                self.attach_node(node.above, x, y, line)
        else:
            if node.below is None:
                node.below = Node(line)
            else:
                self.attach_node(node.below, x, y, line)

    def search_tree(self, node: Node, x: float, y: float) -> list[bool]:
        """Recursively search the tree to return a binary sequence which
        identifies in which tile a given point is located.

        Args:
            node: Node to check or search the children of.
            x: X-Coordinate of the point defining origin of the new line.
            y: Y-Coordinate of the point defining origin of the new line.

        Returns:
            list: List of booleans that identify a tile.
        """
        if node.line.above(x, y):
            if node.above is None:
                return [True]
            else:
                return [True] + self.search_tree(node.above, x, y)
        else:
            if node.below is None:
                return [False]
            else:
                return [False] + self.search_tree(node.below, x, y)

    def tile_id(self, x: float, y: float) -> int:
        """Return a unique id for the tile a point is placed on. This is done
        by checking above which of the lines to point is located and then
        interpreting the list of booleans as an integer.

        Args:
            x: X-Coordinate of the point.
            y: Y-Coordinate of the point.

        Returns:
            Id of the tile the point is placed on.
        """
        aboves = self.search_tree(self.lines, x, y)
        return sum(int(2 ** exp * bit) for exp, bit in enumerate(aboves))

    def tile_id_grid(self, x_samples: int, y_samples: int,
                     squash_ids: bool = False) -> NDArray[np.int_]:
        """Sample the rectangular region in equidistant steps and return an
        array of tile ids.

        Args:
            x_samples: Number of samples in x direction.
            y_samples: Number of samples in y direction.
            squash_ids: Squash the range of tile ids by removing unused ones.

        Returns:
            Array of tile ids.
        """
        xs, ys = np.meshgrid(
            np.linspace(
                -self.x_range / 2,
                self.x_range / 2,
                x_samples,
                endpoint=True
            ),
            np.linspace(
                -self.y_range / 2,
                self.y_range / 2,
                y_samples,
                endpoint=True
            )
        )

        result = np.zeros((x_samples, y_samples), dtype=int)
        for idx, x in np.ndenumerate(xs):
            result[idx] = self.tile_id(x, ys[idx])

        if squash_ids is True:
            _, result = np.unique(result, return_inverse=True)
            result = result.reshape((x_samples, y_samples))

        return result
