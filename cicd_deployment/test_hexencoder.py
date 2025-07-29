from cicd_deployment.hexencoder import hex_encode_text, hex_decode_text

def test_encode():
    assert hex_encode_text('Héllo') == '48c3a96c6c6f'

def test_decode():
    assert hex_decode_text('48c3a96c6c6f') == "Héllo"
