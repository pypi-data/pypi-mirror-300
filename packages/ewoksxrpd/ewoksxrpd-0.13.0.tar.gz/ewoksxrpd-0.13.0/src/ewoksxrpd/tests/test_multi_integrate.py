from os import PathLike
import numpy
import json
import h5py

from ewoksxrpd.tasks.integrate import MultiConfigIntegrate1D
from ewoksxrpd.tasks.nexus import SaveNexusMultiPattern1D
from .xrpd_theory import Measurement, Setup, xPattern


def test_multiintegrate1d(
    imageSetup1SampleA: Measurement, setup1: Setup, xSampleA: xPattern
):
    configs = [
        {"nbpt_rad": 50, "unit": "2th_rad"},
        {"nbpt_rad": 50, "unit": "q_A^-1"},
        {"nbpt_rad": 100, "unit": "q_A^-1"},
    ]
    inputs = {
        "image": imageSetup1SampleA.image,
        "detector": setup1.detector,
        "geometry": setup1.geometry,
        "energy": setup1.energy,
        "integration_options": dict(xSampleA.integration_options),
        "configs": configs,
    }

    task = MultiConfigIntegrate1D(inputs=inputs)
    task.execute()
    output_values = task.get_output_values()

    assert len(output_values["xunits"]) == 3
    for unit, config in zip(output_values["xunits"], configs):
        assert unit == config["unit"]

    assert len(output_values["x"]) == 3
    for x, config in zip(output_values["x"], configs):
        assert len(x) == config["nbpt_rad"]

    assert len(output_values["y"]) == 3
    for y, config in zip(output_values["y"], configs):
        assert len(y) == config["nbpt_rad"]

    assert len(output_values["info"]) == 3
    for info, config in zip(output_values["info"], configs):
        assert info["nbpt_rad"] == config["nbpt_rad"]
        assert info["unit"] == config["unit"]


def test_multisave(tmpdir: PathLike, setup1: Setup):
    npt_list = (50, 100, 200)
    inputs = {
        "url": str(tmpdir / "result.h5"),
        "x_list": [numpy.arange(npt) for npt in npt_list],
        "y_list": [numpy.random.random(npt) for npt in npt_list],
        "xunits": ["2th_deg", "q_A^-1", "q_A^-1"],
        "header_list": [
            {
                "energy": 10.2,
                "detector": setup1.detector,
                "geometry": setup1.geometry,
                "npt_radial": npt,
            }
            for npt in npt_list
        ],
    }

    task = SaveNexusMultiPattern1D(inputs=inputs)
    task.execute()

    with h5py.File(str(tmpdir / "result.h5")) as root:
        assert set(root["results"].keys()) == {
            "measurement",
            "integrate_0",
            "integrate_1",
            "integrate_2",
            # "instrument",
            # "dummy",
        }

        for i, (npt, unit) in enumerate(zip(npt_list, inputs["xunits"])):
            nxprocess = root[f"results/integrate_{i}"]
            numpy.testing.assert_array_equal(
                nxprocess[f"integrated/{unit.split('_')[0]}"],
                inputs["x_list"][i],
            )
            numpy.testing.assert_array_equal(
                nxprocess["integrated/intensity"], inputs["y_list"][i]
            )
            numpy.testing.assert_array_equal(
                root[f"results/measurement/integrated_{i}"], inputs["y_list"][i]
            )

            config = json.loads(nxprocess["configuration"]["data"][()])
            assert set(config) == {
                "ewoks_version",
                "energy",
                "detector",
                "geometry",
                "npt_radial",
            }
            numpy.testing.assert_array_equal(config["npt_radial"], npt)
