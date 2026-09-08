"""Initial project setup tests."""


def test_project_packages_import():
    """The planned package structure can be imported by Python."""
    import ai
    import game
    import units

    assert ai is not None
    assert game is not None
    assert units is not None