#!/usr/bin/env python3

from runtest import TestBase

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'sort',"""
# Function Call Graph for 't-sort' (session: a0e1748898d10ad1)
========== FUNCTION CALL GRAPH ==========
# SELF AVG   SELF MAX   SELF MIN    FUNCTION
                                     : (1) t-sort
  161.125 us  161.125 us  161.125 us :  +-(1) __monstartup
                                     :  |
    0.625 us    0.625 us    0.625 us :  +-(1) __cxa_atexit
                                     :  |
   69.166 us   69.166 us   69.166 us :  +-(1) main
    2.666 us    4.958 us    0.375 us :     +-(2) foo
    8.736 us   36.625 us    3.125 us :     | (6) loop
                                     :     |
   23.167 us   23.167 us   23.167 us :     +-(1) bar
   11.413 ms   11.413 ms   11.413 ms :       (1) usleep
""")

    def prepare(self):
        self.subcmd = 'record'
        return self.runcmd()

    def setup(self):
        self.subcmd = 'graph'
        self.option = '-f self-avg,self-max,self-min'
        self.exearg = 'main'
    def sort(self, output):
        result = []

        for ln in output.split('\n'):
            if not ln.strip() or ln.startswith('#') or ':' not in ln:
                continue

            parts = ln.split(':')[0].strip().split()
            if len(parts) < 6:
                continue

            unit = parts[1].lower()

            try:
                def convert(value):
                    v = float(value)
                    if unit == 'us':
                        return v
                    if unit == 'ms':
                        return v * 1000
                    if unit == 'ns':
                        return v / 1000
                    raise ValueError(f"Unknown time unit: {unit}")

                avg = convert(parts[0])
                max_ = convert(parts[2])
                min_ = convert(parts[4])
            except Exception:
                result.append(f"Parse error: {ln}")
                continue

            if not (min_ <= avg <= max_):
                result.append(f"Invalid order: avg={avg}, min={min_}, max={max_} | Line: {ln}")

        return '\n'.join(result)
