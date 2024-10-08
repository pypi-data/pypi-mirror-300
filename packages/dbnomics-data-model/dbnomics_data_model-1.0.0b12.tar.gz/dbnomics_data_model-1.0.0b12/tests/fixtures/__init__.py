from .git import *

# TODO


# __all__ = ["invalid_dataset_code", "invalid_provider_code", "invalid_release_code", "invalid_dataset_code_release_code"]


# invalid_provider_codes = ["", " ", " P", "P ", " P ", "P 1", "%", "% ", " %", " % ", "P/1", "P+1"]


# @pytest.fixture(params=invalid_provider_codes)
# def invalid_provider_code(request: pytest.FixtureRequest) -> str:
#     return cast(str, request.param)


# invalid_dataset_codes = ["", " ", " D", "D ", " D ", "D 1", "%", "% ", " %", " % ", "D/1", "D+1"]


# @pytest.fixture(params=invalid_dataset_codes)
# def invalid_dataset_code(request: pytest.FixtureRequest) -> str:
#     return cast(str, request.param)


# # Do not add "latest" because it's a valid release code, althrough it is invalid when used in a dataset code.
# invalid_release_codes = ["a b", "a ", " a", " a ", "", " "]


# @pytest.fixture(params=invalid_release_codes)
# def invalid_release_code(request: pytest.FixtureRequest) -> str:
#     return cast(str, request.param)


# @pytest.fixture(params=[*invalid_release_codes, "latest"])
# def invalid_dataset_code_release_code(request: pytest.FixtureRequest) -> str:
#     """Return an invalid release code in the context of a dataset code."""
#     return cast(str, request.param)
