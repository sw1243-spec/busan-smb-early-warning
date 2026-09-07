# -*- coding: utf-8 -*-
# 현장코드 S0~S8 을 mock 데이터에 실제 실행 (드라이런)
import io, sys, traceback, importlib.util, contextlib

spec = importlib.util.spec_from_file_location('b', 'build_field_code.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

MOCK = "D:/mocklab2/20260901_mock"
NS = {}
log = []


def run(nm, lines, patches):
    src = "\n".join(lines)
    for a, b in patches:
        src = src.replace(a, b)
    buf = io.StringIO()
    log.append("")
    log.append("=" * 70)
    log.append("### " + nm)
    log.append("=" * 70)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(src, nm, "exec"), NS)
        out = buf.getvalue()
        log.append(out[:6000])
        log.append(">>> RESULT: OK")
        return True
    except Exception:
        log.append(buf.getvalue()[-3000:])
        log.append(">>> RESULT: FAIL")
        log.append(traceback.format_exc())
        return False


P_BASE = [("sorted(glob.glob('D:/2026*'))[0].replace(chr(92), '/')", repr(MOCK)),
          ("duckdb.connect('D:/lab2026.duckdb')", "duckdb.connect()"),
          ("con.execute(\"SET temp_directory='D:/duck_tmp'\")", "pass"),
          ("con.execute(\"SET memory_limit='24GB'\")", "con.execute(\"SET memory_limit='4GB'\")")]
P_BAD = [("BAD = []   # <-- S1-1 에서 False 로 찍힌 테이블명을 여기에 넣는다",
          "BAD = ['SPN092']")]
P_OUT = [("OUT = 'D:/out_2026'", "OUT = 'D:/mocklab2/out'"), ("D:/out_2026/summary.txt", "D:/mocklab2/out/summary.txt")]

PLAN = [
    ("S0_부팅", P_BASE),
    ("S1_구조확인", []),
    ("S1-4_REL020", []),
    ("S2_뷰생성", []),
    ("S2B_예비경로", P_BAD),
    ("S3_스키마", []),
    ("S4_게이트", []),
    ("S4-6_Q8B", []),
    ("S5_MPI", []),
    ("S6_연령구조", []),
    ("S7_거래폐업", []),
    ("S8_반출준비", P_OUT),
    ("S9_대체축POP019", []),
    ("S10_결과요약", P_OUT),
]

SH = dict(m.SHEETS)
nfail = 0
for nm, pat in PLAN:
    good = run(nm, SH[nm], pat)
    if not good:
        nfail += 1

log.append("")
log.append("=" * 70)
log.append("FAILED BLOCKS: " + str(nfail) + " / " + str(len(PLAN)))
io.open("dryrun.txt", "w", encoding="utf-8").write("\n".join(log))
print("fail", nfail)
