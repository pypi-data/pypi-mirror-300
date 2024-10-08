# %%

from pathlib import Path

from cysimdjson.cysimdjson import JSONParser

# %%

parser = JSONParser()

# %%

good_json_file = Path("./good.json")
bad_json_file = Path("./bad.json")
plain_json_file = Path("./plain.json")

# %%

parser.load(str(good_json_file))

# %%

parser.load(str(bad_json_file))

# %%

parser.load(str(plain_json_file))

# %%

data = parser.parse_string('{"a": [1]}')
data

# %%

data["a"]

# %%

data.export()
