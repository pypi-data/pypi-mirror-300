import gurobipy as gp
import polars as pl

model = gp.Model()


df = pl.DataFrame(
    data=["aaa", "bbb", "ccc", "aaa", "bbb", "ccc"],
    schema=[("txt", pl.String)],
).with_columns(a=pl.int_range(pl.len()).cast(pl.Float64))
df_ = df.gp.add_vars(model, "t", ub=pl.col.a)
df.head()
# df.gp.assign(t2=lambda d: d["t"] * d["t"]).gp.add_constrs(
#     model, "t", gp.GRB.LESS_EQUAL, "t", name="C"
# )
