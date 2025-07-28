from main import convert_to_hex

def test_convert_to_hex():
    assert convert_to_hex(255) == '0xff'