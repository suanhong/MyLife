from app.backup_verification import EXPECTED, VERIFIED_SHA256


def test_verified_backup_contract_matches_recovery():
    assert EXPECTED == {"posts": 2822, "user_images": 252, "image_references": 252}
    assert VERIFIED_SHA256 == "8edb7cfc8bd196d238b0044e146aa0742a01175824c707c4cc673419f01713fb"
