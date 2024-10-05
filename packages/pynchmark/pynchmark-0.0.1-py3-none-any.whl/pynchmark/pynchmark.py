import ast
import inspect
import threading
import multiprocessing
import time
import sys
import json
import gc

from timeit import Timer

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


def timeit(s, repeat=7, num=None, max_repeat_duration=None, agg_fn=None, print_res=True):
    def format_t(t):
        units = ["s", "ms", "μs", "ns"]
        for u in units:
            if t >= 1:
                break
            t *= 1000
        return f"{t:.3f} {u}"

    t = Timer(s, globals=globals())

    durations = []
    try:
        import psutil
    except ImportError:
        psutil = None
    if psutil:
        cpu_begin, t_begin = psutil.cpu_times(percpu=True), time.time()

    class TimerProcess(multiprocessing.Process):

        def __init__(self, *args, **kwargs):
            multiprocessing.Process.__init__(self, *args, **kwargs)
            self._pconn, self._cconn = multiprocessing.Pipe()
            self._result = None


        def run(self):
            try:
                if not num:
                    _num, _duration = t.autorange()
                else:
                    _num = num
                    _duration = t.timeit(number=_num)
                self._cconn.send((_duration, _num))
            except Exception as e:
                self._cconn.send(e)

        @property
        def result(self):
            if self._pconn.poll():
                self._result = self._pconn.recv()
            return self._result


    for _ in range(repeat):

        tp = TimerProcess()
        tp.start()
        tp.join(timeout=max(max_repeat_duration, 0.5) if max_repeat_duration else None)

        if tp.is_alive():
            tp.terminate()
            time.sleep(0.5)
            if tp.is_alive():
                tp.kill()
            raise RuntimeError("Did not finish before max_repeat_duration")
        else:
            if isinstance(tp.result, Exception):
                raise tp.result
            else:
                _duration, _num = tp.result
                duration = _duration / _num
                durations.append(duration)
        tp.close()

    if psutil:
        cpu_end, t_end = psutil.cpu_times(percpu=True), time.time()
        cpu_use = [
            (cpu_end[i].user - cpu_begin[i].user) / (t_end - t_begin)
            for i in range(len(cpu_end))
        ]

    if not agg_fn:
        agg_fn = np.mean
    res = float(agg_fn(durations))
    std = float(np.std(durations))
    cpus = float(np.sum(cpu_use)) if psutil else None
    if print_res:
        print(
            f"{format_t(res)} s ± {format_t(std)} per loop (mean ± std. dev. of {repeat} runs, {num} loops each"
        )
        if psutil:
            print(f"{cpus:.2f} of CPUs used")

    return res, std, cpus


class Pynchmarker():

    # default_pynchmarker = __class__.default_pynchmarker 

    def __init__(self, max_repeat_duration=None):
        self.max_repeat_duration = max_repeat_duration
        self.results = []
        self.params = {}

    def benchit(self, expr, bench_name, bench_params=None, max_repeat_duration=None):
        _bench_params = dict(bench_params) if bench_params else {}
        r = dict(name=bench_name, **_bench_params)
        r.update(self.params)

        for i, ex_r in enumerate(self.results):
            if all(ex_r.get(p) == r[p] for p in r.keys()) and pd.isnull(ex_r.get("err", np.nan)):
                print(f"Skipping existing bench {str(r)[1:-1]}... ", flush=True, file=sys.stderr)
                self.results.pop(i)
                self.results.append(ex_r)
                return
        print(f"Running bench {str(r)[1:-1]}... ", flush=True, file=sys.stderr)

        try:
            gc.collect()
            time, std, cpus = timeit(
                expr, repeat=5, print_res=False, max_repeat_duration=max_repeat_duration or self.max_repeat_duration, agg_fn=lambda l: np.sort(l)[np.size(l)//4]
            )
            r.update(dict(time=time, std=std, cpus=cpus))
            gc.collect()
        except Exception as e:
            r.update(dict(err=str(e)))
        print(json.dumps(r), flush=True)
        self.results.append(r)


    def register_param(self, **kwargs):
        self.params.update(kwargs)


    def bench(self, fn):

        class PMTransformerName(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                node.name = "_pmbench_" + node.name
                return node


        class PMTransformerCode(ast.NodeTransformer):
            def visit_Expr(self, node):
                # print(ast.dump(node))
                bench_name = None
                if (
                    isinstance(node.value, ast.Tuple)
                    and len(node.value.elts) == 2
                    and isinstance(node.value.elts[1], (ast.Constant, ast.JoinedStr))
                ):
                    bench_name = ast.unparse(node.value.elts[1]).lstrip("f").strip("'")
                    bench_fn_node = node.value.elts[0]
                if hasattr(node.value, "op") and isinstance(node.value.op, ast.MatMult):
                    bench_fn_node = node
                    bench_name = ast.unparse(bench_fn_node)
                if bench_name:
                    bench_size_suffix = ""
                    # if isinstance(bench_fn_node, ast.BinOp) and isinstance(bench_fn_node.op, ast.MatMult):
                    #     bench_size_suffix = f"+ \"_\" + str({bench_fn_node.right.id}.shape)[1: -1].strip(',').replace(', ', '_')"

                    # bench_name = f\"{bench_name}\"{bench_size_suffix}
                    code = f'_pmbenchit(lambda: {ast.unparse(bench_fn_node)}, "{bench_name}")'
                    code = inspect.cleandoc(code)
                    # print(code)
                    return ast.parse(code)
                return node


        t = PMTransformerName().visit(ast.parse(inspect.getsource(fn)))
        t = PMTransformerCode().visit(t)
        # print(ast.dump(ast.parse(inspect.getsource(fn)), indent=2))
        # print(ast.dump(t, indent=2))

        # Print transformed function
        # print(ast.unparse(t))

        # Get caller 's globals() and locals()
        caller_g = dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]
        caller_l = dict(inspect.getmembers(inspect.stack()[1][0]))["f_locals"]

        # Define the transformed function and add it to caller's locals()
        exec(ast.unparse(t))
        caller_l.update({"_pmbench_" + fn.__name__: locals()["_pmbench_" + fn.__name__]})

        # Define_pmbenchit() function from current self.benchit() in caller's locals()
        caller_g.update({"_pmbenchit": self.benchit})

        # Replace caller's pynchmark with self
        for m_name, m_val in caller_g.items():
            if getattr(m_val, "__name__", "") == "pynchmark":
                caller_g[m_name] = sys.modules[__name__]

        # Execute the transformed function inside caller context
        exec("_pmbench_" + fn.__name__ + "()", caller_g, caller_l)


    def to_csv(self, fname=None):
        df = pd.DataFrame(self.results)
        for c in df.columns:
            l = max(len(str(s)) for s in df[c].to_list() + [c])
            if l < 32:
                new_c = f"{c:>{l+2}}" if df[c].dtype != float else f"{c:>13}"
                df = df.rename(columns={c: new_c})
                df[new_c] = df[new_c].apply(
                    lambda s: f"{str(s):>{l+2}}" if not isinstance(s, float) else f"{s:>13.9f}"
                )

        if not fname:
            f = sys.stdout
        else:
            f = open(fname, "w")
        df.to_csv(f, index=False)
        if fname:
            f.close()
        return df


    def to_json(self, fname=None):
        if not fname:
            f = sys.stdout
        else:
            f = open(fname, "w")
        json.dump(self.results, f, indent=2)
        if fname:
            f.close()


    def load_json(self, fname):
        with open(fname, "w") as f:
            self.results = json.load(f)


    def load_csv(self, fname):
        self.results = pd.read_csv(fname, skipinitialspace=True).to_dict(orient="records")


    def compare(self, other, compare_group="auto", compare_val="time"):
        df_old = pd.DataFrame(other.results)
        df_new = pd.DataFrame(self.results)

        if compare_group == "auto":
            l = list(df_old.columns)
            compare_group = l[: l.index(compare_val)]
        df_old = df_old[compare_group + [compare_val]]
        df_new = df_new[compare_group + [compare_val]]
        c = df_old.merge(
            df_new, on=compare_group, how="outer", suffixes=("_before", "_after")
        )
        c["diff_%"] = (
            100*(c[compare_val + "_before"] - c[compare_val + "_after"])
            / c[compare_val + "_before"]
        )
        c["diff_%"] = pd.array(c["diff_%"], dtype="int").astype("int")
        c["diff_%"] = c.apply(
            lambda c: "new"
            if pd.isna(c["time_before"])
            else "del"
            if pd.isna(c["time_after"])
            else c["diff_%"],
            axis=1,
        )

        self.results = c.to_dict(orient="records")


# def plot(filter=lambda x: True, params=None):
#     import matplotlib.pyplot as plt
#     fig = plt.figure()
#     fig.size =


    def plot(self, filter=lambda x: True, params=None, out_file=None):
        df = pd.DataFrame(self.results)
        df = df[df.apply(filter, axis=1)]

        fig = plt.figure()
        plt.style.use(["seaborn-v0_8-talk", "seaborn-v0_8-darkgrid"])

        int_params = [c for c in df.columns if df[c].dtype == "int"]
        plot_param = {"hue": "name", "y": "time"}
        if len(int_params) > 0:
            plot_param.update({"x": int_params[0]})
        if len(int_params) > 1:
            plot_param.update({"size": int_params[1], "style": int_params[1]})
        if params:
            plot_param.update(params)
        if "size" in plot_param:
            plot_param.update(
                {"sizes": list(range(1, 1 + len(df[plot_param["size"]].unique())))}
            )

        sns.lineplot(df, **plot_param, markers=True, dashes=False)
        plt.yscale("log")
        plt.xscale("log")
        plt.xticks(
            t := [
                2**p
                for p in range(
                    int(np.floor(np.log2(df[plot_param["x"]].dropna().min()))),
                    1 + int(np.ceil(np.log2(df[plot_param["x"]].dropna().max()))),
                )
            ],
            t,
        )
        plt.yticks(
            t := [
                10**p
                for p in range(
                    int(np.floor(np.log10(df[plot_param["y"]].dropna().min()))),
                    1 + int(np.ceil(np.log10(df[plot_param["y"]].dropna().max()))),
                )
            ],
            t,
        )
        plt.title(" / ".join(sorted(list(df["name"].unique()))))
        if out_file:
            fig.savefig("-".join(sorted({n.split("_")[1] for n in df["name"].unique()})) + ".png")
        else:
            plt.show()
        plt.close()


def main():
    import os
    import pyonf
    import importlib

    config = inspect.cleandoc("""
    format: csv
    out: stdout
    in: ""
    bench_fun: ""
    file: ""
    compare: ""
    max_repeat_duration: 600
    """)

    config = pyonf.pyonf(config)

    if config["format"] not in ("csv", "json"):
        print("format must be json or csv", file=sys.stderr)
        sys.exit(2)

    default_pynchmarker.max_repeat_duration=config["max_repeat_duration"]

    if config["in"]:
        if not os.path.isfile(config["in"]):
            print(f"{config['in']} not found")
            sys.exit(1)
        if config["in"].endswith("csv"):
            load_csv(config["in"])
        if config["in"].endswith("json"):
            load_json(config["in"])
    elif not config.get("file"):
        print("--file or --in option must be given")
        sys.exit(1)

    if config.get("file"):
        if not config.get("bench_fun"):
            print("Missing --bench_fun option")
            sys.exit(1)

        if not os.path.isfile(config["file"]):
            print(f"{config['file']} not found")
            sys.exit(1)

        spec = importlib.util.spec_from_file_location("pmimported", config["file"])
        m = importlib.util.module_from_spec(spec)
        sys.modules["pmimported"] = m
        spec.loader.exec_module(m)

        if not hasattr(m, config["bench_fun"]):
            print(f"No function {config['bench_fun']} found in {config['file']}")
            sys.exit(1)

        globals().update(
            {n: getattr(m, n) for n in m.__all__}
            if hasattr(m, "__all__")
            else {k: v for (k, v) in m.__dict__.items() if not k.startswith("_")}
        )

        bench(getattr(m, config["bench_fun"]))

    if config["compare"]:
        old_pm = Pynchmarker()

        if not os.path.isfile(config["compare"]):
            print(f"{config['compare']} not found")
            sys.exit(1)
        if config["compare"].endswith("csv"):
            old_pm.load_csv(config["compare"])
        if config["compare"].endswith("json"):
            old_pm.load_json(config["compare"])
        compare(old_pm)

    if config["format"] == "csv":
        to_csv(config["out"] if config["out"] != "stdout" else None)
    elif config["format"] == "json":
        to_json(config["out"] if config["out"] != "stdout" else None)

default_pynchmarker = Pynchmarker()
register_param = default_pynchmarker.register_param
benchit = default_pynchmarker.benchit
bench = default_pynchmarker.bench
load_csv = default_pynchmarker.load_csv
load_json = default_pynchmarker.load_json
to_csv = default_pynchmarker.to_csv
to_json = default_pynchmarker.to_json
compare = default_pynchmarker.compare
plot =default_pynchmarker.plot


if __name__ == "__main__":
    main()
