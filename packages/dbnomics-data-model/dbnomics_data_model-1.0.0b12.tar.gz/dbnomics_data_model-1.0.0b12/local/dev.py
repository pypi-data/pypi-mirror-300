# %%

from itertools import accumulate, repeat
from pathlib import Path
from typing import List  # noqa: UP035

from isoweek import Week
from rich import print

from dbnomics_data_model.json_utils.dumping import dump_as_json_data
from dbnomics_data_model.json_utils.loading import load_json_data
from dbnomics_data_model.json_utils.parsing import JsonParser
from dbnomics_data_model.model import BimesterPeriod, MonthPeriod
from dbnomics_data_model.model.periods import DayPeriod, QuarterPeriod, SemesterPeriod, WeekPeriod
from dbnomics_data_model.storage.adapters.filesystem.model.category_tree_json import CategoryTreeNodeJson
from dbnomics_data_model.storage.adapters.filesystem.model.loading import filesystem_model_loader
from dbnomics_data_model.storage.storage_uri import StorageUri

# %%
category_tree_json_file = Path("/home/cbenz/Dev/dbnomics/dbnomics-fetchers/ons-fetcher/json-data/category_tree.json")

# %%

parser = JsonParser.create()
category_tree_json_data = parser.parse_file(category_tree_json_file)
category_tree_json_data


# %%

nodes = load_json_data(category_tree_json_data, loader=filesystem_model_loader, type_=List[CategoryTreeNodeJson])  # noqa: UP006
print(nodes)

# %%


StorageUri.parse("lalala:/x")

# %%

m1 = MonthPeriod(2000, 12)
m1

# %%

m1.quarter.first_month.quarter.semester.year

# %%

MonthPeriod(2000, 10) - MonthPeriod(1999, 1)

# %%

QuarterPeriod(2000, 3) - QuarterPeriod(1999, 1)

# %%

SemesterPeriod(2000, 2) - SemesterPeriod(1999, 1)

# %%
BimesterPeriod(2000, 2) - BimesterPeriod(2000, 1)
# %%
WeekPeriod(2000, 2) - WeekPeriod(2000, 1)
# %%
DayPeriod(2000, 3, 1) - DayPeriod(2000, 2, 1)

# %%

SemesterPeriod.max_semester_num
# %%


p1 = MonthPeriod(2000, 1)
p1


# %%

p2 = p1 + 1
p2

# %%

p2 - 1 == p1

# %%

list(accumulate(repeat(1, 20), initial=MonthPeriod(2000, 1)))

# %%

p1 - 2

# %%

p3 = BimesterPeriod(2000, 1)
p3


# %%

dump_as_json_data(p3)

# %%

p3.next

# %%

p3.previous
# %%

p3 - 0 is p3


# %%

w1 = Week(2000, 1)
w1


# %%

# w1.toordinal()
w1.monday().toordinal()  # // 7 + 1


# %%
