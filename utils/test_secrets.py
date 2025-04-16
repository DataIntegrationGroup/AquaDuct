import secrets as s

def test_get_secret():
  secret_id = "test"
  assert s.get(secret_id)["id"] == "test_id"
  assert s.get(secret_id)["secret"] == "12345"