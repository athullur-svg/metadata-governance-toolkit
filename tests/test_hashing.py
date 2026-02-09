from src.mgt.core.hashing import stable_hash

def test_stable_hash_is_case_insensitive():
    assert stable_hash("A", "b") == stable_hash(" a ", "B")

def test_stable_hash_changes_when_parts_change():
    assert stable_hash("a", "b") != stable_hash("a", "c")