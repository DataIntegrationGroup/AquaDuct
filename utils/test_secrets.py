import secrets as s

def test_get_secret():
  secret_id = "test"
  assert s.get_secret(secret_id)["id"] == "test_id"
  assert s.get_secret(secret_id)["secret"] == "12345"