from django.conf import settings

from shortener.codegen import generate_code


def test_generated_code_uses_default_length() -> None:
    code = generate_code()

    assert len(code) == settings.DEFAULT_CODE_LENGTH
