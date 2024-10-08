import pytest

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods import (
    BimesterPeriod,
    DayPeriod,
    MonthPeriod,
    Period,
    QuarterPeriod,
    SemesterPeriod,
    WeekPeriod,
    YearPeriod,
)


@pytest.mark.parametrize(
    ("period_input", "expected_output"),
    [
        ("2014", YearPeriod(year_num=2014)),
        ("2014-S1", SemesterPeriod(semester_num=1, year_num=2014)),
        ("2014-B1", BimesterPeriod(bimester_num=1, year_num=2014)),
        ("2014-Q1", QuarterPeriod(quarter_num=1, year_num=2014)),
        ("2014-01", MonthPeriod(month_num=1, year_num=2014)),
        ("2014-W01", WeekPeriod(week_num=1, year_num=2014)),
        ("2015-W53", WeekPeriod(week_num=53, year_num=2015)),
        ("2019-W53", WeekPeriod(week_num=53, year_num=2019)),
        ("2014-12-01", DayPeriod(day_num=1, month_num=12, year_num=2014)),
    ],
)
def test_period_parse_valid_input(period_input: str, expected_output: Period) -> None:
    assert Period.parse(period_input) == expected_output


@pytest.mark.parametrize(
    ("period_input"),
    [
        "0",
        "-1000",
        "1000000",
        "2014-1",
        "2014-S0",
        "2014 S1",
        "2014S1",
        "2014-S01",
        "2014-S3",
        "2014-B0",
        "2014 B1",
        "2014B1",
        "2014-B01",
        "2014-B7",
        "2014-Q0",
        "2014 Q1",
        "2014Q1",
        "2014-Q01",
        "2014-Q5",
        "2014-W1",
        "2014 W01",
        "2014W01",
        "2014W1",
        "2014-W00",
        "2014-W54",
        "2014-12-1",
        "2014-12 01",
        "2014 12 01",
        "2014 12-01",
        "20141201",
        "2014-12-00",
        "2014-12-32",
        "2014-13-01",
        "ABCDE",
        "2014Z01",
    ],
)
def test_period_parse_invalid_input(period_input: str) -> None:
    with pytest.raises(PeriodParseError):
        Period.parse(period_input)


#     # From period format corresponding to frequency:
#     >>> detect_frequency('2014', '2015')
#     (<Frequency.ANNUAL: 'annual'>, None)
#     >>> detect_frequency('2014', '2016')
#     (<Frequency.ANNUAL: 'annual'>, None)
#     >>> detect_frequency('2014-S1', '2014-S2')
#     (<Frequency.BI_ANNUAL: 'bi-annual'>, None)
#     >>> detect_frequency('2014-S1', '2015-S2')
#     (<Frequency.BI_ANNUAL: 'bi-annual'>, None)
#     >>> detect_frequency('2014-Q1', '2014-Q2')
#     (<Frequency.QUARTERLY: 'quarterly'>, None)
#     >>> detect_frequency('2014-Q1', '2014-Q3')
#     (<Frequency.QUARTERLY: 'quarterly'>, None)
#     >>> detect_frequency('2014-B1', '2014-B2')
#     (<Frequency.BI_MONTHLY: 'bi-monthly'>, None)
#     >>> detect_frequency('2014-B1', '2014-B3')
#     (<Frequency.BI_MONTHLY: 'bi-monthly'>, None)
#     >>> detect_frequency('2014-01', '2014-02')
#     (<Frequency.MONTHLY: 'monthly'>, None)
#     >>> detect_frequency('2014-01', '2014-03')
#     (<Frequency.MONTHLY: 'monthly'>, None)
#     >>> detect_frequency('2014-W01', '2014-W02')
#     (<Frequency.WEEKLY: 'weekly'>, None)
#     >>> detect_frequency('2014-W01', '2014-W03')
#     (<Frequency.WEEKLY: 'weekly'>, None)
#     >>> detect_frequency('2014-01-01', '2014-01-02')
#     (<Frequency.DAILY: 'daily'>, None)
#     >>> detect_frequency('2014-01-01', '2014-01-03')
#     (<Frequency.DAILY: 'daily'>, None)

#     # From daily period format:
#     >>> detect_frequency('2014-01-01', '2015-01-01')  # doctest: +ELLIPSIS
#     (<Frequency.ANNUAL: 'annual'>, ...)
#     >>> detect_frequency('2014-01-01', '2014-07-01')  # doctest: +ELLIPSIS
#     (<Frequency.BI_ANNUAL: 'bi-annual'>, ...)
#     >>> detect_frequency('2014-01-01', '2014-04-01')  # doctest: +ELLIPSIS
#     (<Frequency.QUARTERLY: 'quarterly'>, ...)
#     >>> detect_frequency('1919-03-31', '1919-06-30')  # doctest: +ELLIPSIS
#     (<Frequency.QUARTERLY: 'quarterly'>, ...)
#     >>> detect_frequency('2014-01-01', '2014-03-01')  # doctest: +ELLIPSIS
#     (<Frequency.BI_MONTHLY: 'bi-monthly'>, ...)
#     >>> detect_frequency('2014-01-01', '2014-02-01')  # doctest: +ELLIPSIS
#     (<Frequency.MONTHLY: 'monthly'>, ...)
#     >>> detect_frequency('2014-01-15', '2014-02-15')  # doctest: +ELLIPSIS
#     (<Frequency.MONTHLY: 'monthly'>, ...)
#     >>> detect_frequency('2014-01-01', '2014-01-31')  # doctest: +ELLIPSIS
#     (<Frequency.DAILY: 'daily'>, ...)
#     >>> detect_frequency('2014-01-06', '2014-01-13')  # doctest: +ELLIPSIS
#     (<Frequency.WEEKLY: 'weekly'>, ...)
#     >>> detect_frequency('2014-01-07', '2014-01-14')  # doctest: +ELLIPSIS
#     (<Frequency.WEEKLY: 'weekly'>, ...)
#     >>> detect_frequency('2014-01-06', '2014-01-14')  # doctest: +ELLIPSIS
#     (<Frequency.DAILY: 'daily'>, ...)
#     >>> detect_frequency('2014-01-03', '2014-01-11')  # doctest: +ELLIPSIS
#     (<Frequency.DAILY: 'daily'>, ...)

#     # Invalid or different period formats:
#     >>> detect_frequency('2014', '2015-02')
#     (None, None)
#     >>> detect_frequency('2014', '2014Z2')
#     (None, None)
#     >>> detect_frequency('2014Z2', '2014')
#     (None, None)
#     >>> detect_frequency('2014Z2', '2014Z2')
#     (None, None)
