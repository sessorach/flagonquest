"""Long runs that survive a restart (2026-10-29).

The container's worker restarts now and then, and every process goes
with it; files stay. A long script keeps a `Partial` next to its output:
each finished job's result is appended (and flushed) as it comes in, and
a restarted run skips the jobs already in it. Results are the same as an
unbroken run's as long as each job is seeded on its own, which every
sim job here is. The file goes once the output's written.
"""
import json
import os


class Partial:
    def __init__(self, path):
        self.path = path
        self.got = {}
        if os.path.exists(path):
            good = []
            with open(path, encoding="utf-8") as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                    except ValueError:
                        break  # a line cut off mid-write: redo that job
                    self.got[rec["k"]] = rec["v"]
                    good.append(line)
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(good)
        self.f = open(path, "a", encoding="utf-8")

    @staticmethod
    def key(k):
        return k if isinstance(k, str) else json.dumps(k, sort_keys=True, default=str)

    def __contains__(self, k):
        return self.key(k) in self.got

    def get(self, k):
        return self.got[self.key(k)]

    def add(self, k, v):
        k = self.key(k)
        self.got[k] = v
        self.f.write(json.dumps({"k": k, "v": v}) + "\n")
        self.f.flush()
        os.fsync(self.f.fileno())

    def finish(self):
        self.f.close()
        if os.path.exists(self.path):
            os.remove(self.path)
