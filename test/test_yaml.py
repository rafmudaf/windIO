import numpy as np
from io import StringIO
from pathlib import Path

import windIO
import windIO.yaml


def assert_equal_dicts(d1, d2):
    np.testing.assert_equal(type(d1), type(d2))
    for key, val in d1.items():
        if isinstance(val, dict):
            assert_equal_dicts(val, d2[key])
        elif isinstance(val, list):
            assert_equal_lists(val, d2[key])
        np.testing.assert_equal(type(val), type(d2[key]))
        np.testing.assert_equal(val, d2[key])


def assert_equal_lists(l1, l2):
    np.testing.assert_equal(type(l1), type(l2))
    np.testing.assert_equal(len(l1), len(l2))
    for val1, val2 in zip(l1, l2):
        if isinstance(val1, dict):
            assert_equal_dicts(val1, val2)
        elif isinstance(val1, list):
            assert_equal_lists(val1, val2)
        np.testing.assert_equal(type(val1), type(val2))
        np.testing.assert_equal(val1, val2)


def test_write_list_flow_style():
    data = {
        "a": [1, 2, 3],
        "b": [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]],
        "c": [1, "XY"],
        "d": ["1", "2", "3"],
        "e": [{"a": [1, 2], "b": [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]}],
    }

    def get_yaml_str(data, flow_style=False):
        out = StringIO()
        yml_obj = windIO.YAML(typ="safe")
        yml_obj.default_flow_style = flow_style
        yml_obj.dump(data, out)
        return out.getvalue()

    # WithOUT flow style
    out1 = StringIO()
    windIO.yaml.get_YAML(n_list_flow_style=0).dump(data, out1)
    str_data1 = out1.getvalue()
    assert str_data1 == get_yaml_str(data)

    # With flow-style for 1D numeric array
    out1 = StringIO()
    windIO.yaml.get_YAML(n_list_flow_style=1).dump(data, out1)
    str_data1 = out1.getvalue()
    for line in str_data1.split("\n"):
        if "[" in line:
            assert line.count("[") == 1 and line.count("]") == 1

    # With flow-style for 2D numeric array
    out1 = StringIO()
    windIO.yaml.get_YAML(n_list_flow_style=2).dump(data, out1)
    str_data1 = out1.getvalue()
    for line in str_data1.split("\n"):
        if "[" in line:
            if line.count("[") > 1:
                assert line.count("[") == 3 and line.count("]") == 3
            else:
                assert line.count("[") == 1 and line.count("]") == 1

    # With flow-style for 3D numeric array
    out1 = StringIO()
    windIO.yaml.get_YAML(n_list_flow_style=3).dump(data, out1)
    str_data1 = out1.getvalue()
    for line in str_data1.split("\n"):
        if "[" in line:
            if line.count("[") > 1:
                assert line.count("[") == 7 and line.count("]") == 7
            else:
                assert line.count("[") == 1 and line.count("]") == 1


def test_write_numpy():

    # Data to test against
    test_data = dict(
        a=[0.1, 0.2],
        b=40,
        c=30.0,
        d="test",
        e=[[0.1, 0.2], [0.3, 0.4]],
        f=dict(a=[0.1, 0.2], b=40, c=30.0, d="test", e=[[0.1, 0.2], [0.3, 0.4]]),
        g=[5, [1.0, 3.0], "test"],
    )

    # Data containing numpy types
    din = dict(
        a=np.array([0.1, 0.2]),
        b=np.int16(40),
        c=np.float16(30.0),
        d=np.str_("test"),
        e=np.array([[0.1, 0.2], [0.3, 0.4]]),
        f=dict(
            a=np.array([0.1, 0.2]),
            b=np.int16(40),
            c=np.float16(30.0),
            d=np.str_("test"),
            e=np.array([[0.1, 0.2], [0.3, 0.4]]),
        ),
        g=[5, np.array([1.0, 3.0]), "test"],
    )

    # File StringIO "file" to write to
    tfile = StringIO()

    # Write data to "file"
    windIO.yaml.get_YAML().dump(din, tfile)
    # Reset file location
    tfile.seek(0)

    # Convert "file" to python data (using the "safe" loader do get a python dict)
    dout = windIO.yaml.get_YAML("safe").load(tfile)

    # Asserting that dicts are equal
    assert_equal_dicts(test_data, dout)


def test_include():
    base_path = Path(windIO.plant_ex.__file__).parent
    # Include YAML file
    filename = base_path / "plant_energy_site/IEA37_case_study_1_2_energy_site.yaml"
    # without include
    with open(filename, "r") as f:
        for i in range(4):
            f.readline()
        out
    out = windIO.yaml.get_YAML(read_include=False).load(filename)

    # Include netCFD file
    windIO.yaml.get_YAML().load(
        base_path / "plant_energy_resource/GriddedResource_nc.yaml"
    )
    raise NotImplementedError("Should be tested against a manually embedding")


def test_numpy_read():
    raise NotImplementedError("Test for reading numeric array into numpy")
