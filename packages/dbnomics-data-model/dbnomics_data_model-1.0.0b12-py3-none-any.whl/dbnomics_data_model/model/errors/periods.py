from dbnomics_data_model.errors import DataModelError


class PeriodParseError(DataModelError):
    def __init__(self, *, period_raw: str) -> None:
        msg = f"Could not parse a period from string {period_raw!r}"
        super().__init__(msg=msg)
        self.value = period_raw
