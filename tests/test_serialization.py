from garmin_mcp.utils.serialization import serialize_response


def test_serialize_none():
    assert serialize_response(None) == "null"


def test_serialize_string_passthrough():
    assert serialize_response("ok") == "ok"


def test_serialize_dict_pretty_json():
    out = serialize_response({"a": 1, "b": "c"})
    # Garantir que é JSON e contém chaves.
    assert '"a"' in out
    assert '"b"' in out


def test_serialize_list_pretty_json():
    out = serialize_response([1, 2, 3])
    assert "1" in out and "2" in out and "3" in out


