import pytest
from encrypt_decrypt import validate_choice, encrypt, decryption_text_valdiation, decrypt


def test_validate_choice():
    with pytest.raises(ValueError):
        assert validate_choice("")
        assert validate_choice("0")
        assert validate_choice("123")
        assert validate_choice("abc")


def test_encrypt():
    assert encrypt("AbCd", "0123") == "GeCa"
    assert encrypt("AbCD", "wxyz") == "caYw"
    assert encrypt("123789", "wasd") == "149@@@#0##9##8#468"
    assert encrypt("1a5b3C", "8") == "5k#0#J@I#8#2"
    assert encrypt("@-((2)).#", "8") == ")#(.))#9#((-)@("
    assert encrypt("123789 1a5b3C @-((2)).#", "8") == "149@@@#0##9##8#468 5k#0#J@I#8#2 )#(.))#9#((-)@("


def test_decryption_text_valdiation():
    assert decryption_text_valdiation("abc") == True
    assert decryption_text_valdiation("6@1") == True
    assert decryption_text_valdiation("46@@16") == True
    assert decryption_text_valdiation("46@)@(@16") == True
    assert decryption_text_valdiation("46@@16 6@1") == True
    assert decryption_text_valdiation("46@@16 )#() #8# 6@1") == True

def test_decrypt():
    assert decrypt("GeCa", "0123") == "AbCd"
    assert decrypt("caYw", "wxyz") == "AbCD"
    assert decrypt("149@@@#0##9##8#468", "wasd") == "123789"
    assert decrypt("5k#0#J@I#8#2", "8") == "1a5b3C"
    assert decrypt(")#(.))#9#((-)@(", "8") == "@-((2)).#"
    assert decrypt("149@@@#0##9##8#468 5k#0#J@I#8#2 )#(.))#9#((-)@(", "8") == "123789 1a5b3C @-((2)).#"
