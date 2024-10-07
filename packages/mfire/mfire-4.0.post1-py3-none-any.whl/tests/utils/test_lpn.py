import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.utils.date import Datetime
from tests.functions_test import assert_identically_close
from tests.utils.factories import LpnFactory


class TestLpn:
    @pytest.mark.parametrize(
        "lpn,expected",
        [
            # No variations
            ([0], xr.DataArray([0], coords={"valid_time": [Datetime(2023, 3, 1)]})),
            (
                [0, 40, 30, 0],
                xr.DataArray([0], coords={"valid_time": [Datetime(2023, 3, 1)]}),
            ),
            ([110], xr.DataArray([100], coords={"valid_time": [Datetime(2023, 3, 1)]})),
            (
                [100, 199],
                xr.DataArray([100], coords={"valid_time": [Datetime(2023, 3, 1)]}),
            ),
            # One variation
            (
                [100, 330, 450, 670],
                xr.DataArray(
                    [100, 600],
                    coords={"valid_time": [Datetime(2023, 3, 1, i) for i in [0, 3]]},
                ),
            ),
            (
                [560, 330, 45],
                xr.DataArray(
                    [500, 0],
                    coords={"valid_time": [Datetime(2023, 3, 1, i) for i in [0, 2]]},
                ),
            ),
            # Two variations
            (
                [100, 200, 190, 300],
                xr.DataArray(
                    [100, 300],
                    coords={"valid_time": [Datetime(2023, 3, 1, i) for i in [0, 3]]},
                ),
            ),
            (
                [400, 380, 600],
                xr.DataArray(
                    [300, 600],
                    coords={"valid_time": [Datetime(2023, 3, 1, i) for i in [0, 2]]},
                ),
            ),
            (
                [100, 500, 490],
                xr.DataArray(
                    [100, 400],
                    coords={"valid_time": [Datetime(2023, 3, 1, i) for i in [0, 2]]},
                ),
            ),
            # More than 3 variations
            (
                [120, 500, 470, 460, 800, 820, 530],
                xr.DataArray(
                    [100, 800, 500],
                    coords={"valid_time": [Datetime(2023, 3, 1, i) for i in [0, 5, 6]]},
                ),
            ),
        ],
    )
    def test_extremums_da(self, lpn, expected):
        lpn = LpnFactory(
            da=xr.DataArray(
                [[lpn, [v + 5 for v in lpn]]],  # test minimal value taken over space
                coords={
                    "latitude": [30],
                    "longitude": [40, 41],
                    "valid_time": [Datetime(2023, 3, 1, i) for i in range(len(lpn))],
                },
            )
        )
        assert_identically_close(lpn.extremums_da, expected)

    @pytest.mark.parametrize(
        "extremums,expected",
        [
            (None, None),
            ([100], "1xlpn"),
            ([100, 200], "2xlpn+"),
            ([200, 100], "2xlpn-"),
            ([100, 200, 100], "3xlpn+"),
            ([200, 100, 200], "3xlpn-"),
        ],
    )
    def test_template_key(self, extremums, expected):
        lpn_da = xr.DataArray(
            [[[np.nan]]],
            coords={
                "longitude": [40],
                "latitude": [30],
                "valid_time": [Datetime(2023, 3, 1)],
            },
        )  # To handle extremums=None

        assert (
            LpnFactory(
                da=lpn_da,
                extremums_da_factory=xr.DataArray(extremums) if extremums else None,
            ).template_key
            == expected
        )
