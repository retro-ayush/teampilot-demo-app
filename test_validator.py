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
    assert validate_login("jane@example.com", "s3cretpass")["ok"] is True
    res = validate_login("", "short")
    assert res["ok"] is False and len(res["errors"]) == 2
    assert "invalid email" in res["errors"]
    assert "password must be at least 8 characters" in res["errors"]


def test_login_empty_inputs():
    res = validate_login("", "")
    assert res["ok"] is False and len(res["errors"]) == 2
    assert "invalid email" in res["errors"]
    assert "password must be at least 8 characters" in res["errors"]

    res_spaces = validate_login("   ", "        ")
    assert res_spaces["ok"] is False and len(res_spaces["errors"]) == 2

    res_none = validate_login(None, None)
    assert res_none["ok"] is False and len(res_none["errors"]) == 2


def test_login_validation_edge_cases():
    # Valid email with short password
    res1 = validate_login("jane@example.com", "short")
    assert res1["ok"] is False
    assert res1["errors"] == ["password must be at least 8 characters"]

    # Whitespace email with valid password
    res2 = validate_login("   ", "validpassword123")
    assert res2["ok"] is False
    assert res2["errors"] == ["invalid email"]

    # Whitespace-only password (8 characters of whitespace)
    res3 = validate_login("jane@example.com", "        ")
    assert res3["ok"] is False
    assert "password must be at least 8 characters" in res3["errors"]

