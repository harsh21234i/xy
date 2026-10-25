"""Stateful pyplot compatibility behavior without optional Matplotlib."""

from __future__ import annotations

import numpy as np
import pytest

import xy.pyplot as xyplt


def test_limit_helpers_accept_matplotlib_bound_aliases() -> None:
    _fig, ax = xyplt.subplots()
    ax.plot([0.0, 10.0], [0.0, 10.0])

    assert xyplt.xlim(xmin=1.0, xmax=8.0) == (1.0, 8.0)
    assert xyplt.xlim(xmin=2.0) == (2.0, 8.0)
    assert xyplt.ylim(ymin=3.0, ymax=9.0) == (3.0, 9.0)
    assert xyplt.ylim(ymax=7.0) == (3.0, 7.0)
    with pytest.raises(TypeError, match="both 'left' and 'xmin'"):
        xyplt.xlim(left=0.0, xmin=1.0)
    with pytest.raises(TypeError, match="both 'bottom' and 'ymin'"):
        xyplt.ylim(bottom=0.0, ymin=1.0)
    assert ax.get_xlim() == (2.0, 8.0)
    assert ax.get_ylim() == (3.0, 7.0)


def test_minor_tick_setter_returns_current_minor_ticks_not_major_ticks() -> None:
    _fig, ax = xyplt.subplots()
    ax.plot([0.0, 10.0], [0.0, 10.0])
    ax.set_xlim(0.0, 10.0)
    ax.set_ylim(0.0, 10.0)
    ax.minorticks_on()
    ax._build_chart(640, 480)
    major_x = ax.get_xticks().copy()
    major_y = ax.get_yticks().copy()
    minor_x = ax.get_xticks(minor=True).copy()
    minor_y = ax.get_yticks(minor=True).copy()
    assert minor_x.size > 0
    assert minor_y.size > 0

    xlocations, xlabels = xyplt.xticks([2.5, 7.5], minor=True)
    ylocations, ylabels = xyplt.yticks([2.5, 7.5], minor=True)

    np.testing.assert_array_equal(xlocations, minor_x)
    np.testing.assert_array_equal(ylocations, minor_y)
    np.testing.assert_array_equal(ax.get_xticks(), major_x)
    np.testing.assert_array_equal(ax.get_yticks(), major_y)
    assert xlabels == ax.xaxis.get_minorticklabels()
    assert ylabels == ax.yaxis.get_minorticklabels()
