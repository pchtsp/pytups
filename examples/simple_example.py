# from pytups.pytups.tuplist import TupList
# from pytups.pytups.superdict import SuperDict

from pytups import TupList, Superdict

# Data example
data = [
    dict(name="Alex", birthyear=1980, sex="M", height=175),
    dict(name="Bernard", birthyear=1955, sex="M", height=164),
    dict(name="Chloe", birthyear=1995, sex="F", height=178),
    dict(name="Daniel", birthyear=2010, sex="M", height=131),
    dict(name="Ellen", birthyear=1968, sex="F", height=158),
]

data_tl = TupList(data)

# get all adult males (adults in 2021)
adults_M = data_tl.vfilter(lambda v: v["sex"] == "M").vfilter(
    lambda v: v["birthyear"] <= 2003
)
print("adults_M:", adults_M)

# get only their names and birthyear
adults_M_names_BY = adults_M.take(["name", "birthyear"])
print("adults_M_names_BY:", adults_M_names_BY)

# get only their names
adults_M_names = adults_M.take("name")
print("adults_M_names:", adults_M_names)

# get everyone age (in 2021)
year = 2021
ages = data_tl.vapply(lambda v: year - v["birthyear"])
print("ages:", ages)

# names sorted by age (reverse oof birthyear)
age_sorted = data_tl.sorted(key=lambda v: v["birthyear"], reverse=True).take("name")
print("age_sorted:", age_sorted)

# go from a list of dict to a list of tuples
data_tl2 = data_tl.take(["name", "birthyear", "height", "sex"])
print("data_tl2:", data_tl2)

# get height depending on birthyear and sex
height_data = data_tl.to_dict(
    result_col="height", indices=["birthyear", "sex"], is_list=False
)
print("height_data:", height_data)

# Get heights for each sex
sex_height_data = data_tl.to_dict(result_col="height", indices="sex", is_list=True)
print("sex_height_data:", sex_height_data)

# Transform the tuplist in a dict indexed by name
dict_name = data_tl2.to_dict(result_col=None, indices=0, is_list=False)
print("dict_name:", dict_name)

## Work with superdict
# Transform tuplist into dict indexed by names
data_sd = data_tl.to_dict(indices="name", result_col=None)
print("data_sd:", data_sd)

# Equivalent superdict created with dict comprehension
equivalent_sd = SuperDict.from_dict({d["name"]: d for d in data})
print("equivalent_sd:", equivalent_sd)

# Get a dict of heights
dict_height = data_sd.get_property("height")
print("dict_height:", dict_height)

# Separate males and females
dict_sex = data_sd.index_by_property("sex")
print("dict_sex", dict_sex)
