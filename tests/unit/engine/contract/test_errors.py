from platform_core.engine.errors import EngineError, EngineErrorCategory


def test_error_category() -> None:

    error = EngineError(
        category=EngineErrorCategory.VALIDATION,
        message="invalid manifest",
    )

    assert error.category is EngineErrorCategory.VALIDATION


def test_error_is_immutable() -> None:

    error = EngineError(
        category=EngineErrorCategory.INTERNAL,
        message="boom",
    )

    assert error.message == "boom"


def test_all_categories_exist() -> None:

    expected = {
        "validation",
        "configuration",
        "dependency",
        "execution",
        "timeout",
        "cancellation",
        "internal",
    }

    actual = {category.value for category in EngineErrorCategory}

    assert actual == expected
