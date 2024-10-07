"""Tests for `johannesmann` package."""
import numpy as np
import johannesmann


def test_line():
    line = johannesmann.Line(0, 0)
    assert line.slope == 0
    assert line.above(0, 1)
    assert not line.above(0, -1)


def test_tessellation():
    tessel = johannesmann.Tessellation(4, 4, 2)
    # Manually add a non-random line
    tessel.lines = johannesmann.Node(johannesmann.Line(0, 0))
    assert tessel.tile_id(0, 1) == 1
    assert tessel.tile_id(0, -1) == 0
    r = tessel.tile_id_grid(2, 2)
    assert np.allclose(r, np.array([[0, 0], [1, 1]]))

    # Add a second line; nearly vertical
    tessel.lines.above = johannesmann.Node(johannesmann.Line(-1e20, 1e20))
    assert tessel.tile_id(1, 1) == 3
    assert tessel.tile_id(1, -1) == 0
    r = tessel.tile_id_grid(2, 2)
    assert np.allclose(r, np.array([[0, 0], [3, 1]]))
    r = tessel.tile_id_grid(2, 2, squash_ids=True)
    assert np.allclose(r, np.array([[0, 0], [2, 1]]))
