"""Run with: python3 -m pytest demo-repo -q
Two tests fail until the bug in validator.py is fixed — that failure is the
demo's starting point, not a mistake."""
from validator import validate_email, validate_login


def test_valid_email():
    assert validate_email("jane@example.com") is True
    assert validate_email("user.name+tag@domain.co.uk") is True


def test_rejects_malformed():
    assert validate_email("jane@") is False
    assert validate_email("@example.com") is False
    assert validate_email("jane@example") is False
    assert validate_email("jane example@domain.com") is False
    assert validate_email("jane@@example.com") is False


def test_rejects_empty_and_whitespace_email():
    assert validate_email("") is False
    assert validate_email("   ") is False
    assert validate_email("\t\n") is False
    assert validate_email("\r\n") is False


def test_rejects_none_email():
    assert validate_email(None) is False


def test_valid_email_with_surrounding_whitespace():
    assert validate_email("  jane@example.com  ") is True
    assert validate_email("\tjane@example.com\n") is True


def test_login_flow():
    # Valid login
    assert validate_login("jane@example.com", "s3cretpass")["ok"] is True
    
    # Both email and password invalid
    res = validate_login("", "short")
    assert res["ok"] is False and len(res["errors"]) == 2
    assert "invalid email" in res["errors"]
    assert "password must be at least 8 characters" in res["errors"]

    # Whitespace email with valid password
    res_ws = validate_login("   ", "s3cretpass")
    assert res_ws["ok"] is False
    assert "invalid email" in res_ws["errors"]

    # Valid email with short/empty password
    res_short = validate_login("jane@example.com", "short")
    assert res_short["ok"] is False
    assert "password must be at least 8 characters" in res_short["errors"]

    # None inputs
    res_none = validate_login(None, None)
    assert res_none["ok"] is False
    assert len(res_none["errors"]) == 2

