# -*- coding: utf-8 -*-
# 방어용 재검증 3종 — 반출 승인 산출물(out1·out7)만 재가공. 새 원천 데이터 없음.
#  A. 정체 상권 판정 임계값 민감도 (중앙값 컷 → P40~P60 컷에서 집합이 흔들리는가)
#  B. 발견쌍(-0.612 / -0.550) 강건성: Kendall tau + 순열검정 p (스피어만)
#  C. 기존 지표 시야 검사: MPI(35개월 평균 순위)·소멸률 순위에서 정체 5곳이 어디에 있나
#     → "기존 지표로는 안 잡힌다(사각지대)" 주장의 정량화 + 그림2(판정 대조 2x2) 재료
import numpy as np
import pandas as pd

BASE = 'C:/Users/진세운/Desktop/빅데이터 대회'
EXP = BASE + '/0_부산 데이터 오픈랩 09.03. 반출 신청 데이터_260904'
OUTDIR = BASE + '/제출자료/2_보고서_재료'

d7 = pd.read_csv(EXP + '/out7_gu_closure.csv', dtype={'gu': str})
d1 = pd.read_csv(EXP + '/out1_mpi_gu_rank.csv', dtype={'gu': str})
nm = pd.read_csv(BASE + '/data/구군코드_매핑.csv', encoding='utf-8-sig', dtype={'gu': str})
df = d7.merge(nm, on='gu')
df['age_pct'] = df['age'] * 100
NL = chr(10)
lines = []


def log(s=''):
    lines.append(s)


# ---------- A. 임계값 민감도 ----------
log('=' * 72)
log('A. 정체 상권 판정 임계값 민감도')
log('   정의: 소멸률(cls_old)과 개점률(new_rate)이 모두 컷 미만')
log('=' * 72)
base_set = None
for p in [40, 45, 50, 55, 60]:
    c_cut = np.percentile(df['cls_old'], p)
    n_cut = np.percentile(df['new_rate'], p)
    sel = sorted(df.loc[(df['cls_old'] < c_cut) & (df['new_rate'] < n_cut), 'sigungu'])
    if p == 50:
        base_set = set(sel)
    log(f'P{p} 컷  소멸<{c_cut:.2f} & 개점<{n_cut:.2f}  →  {len(sel)}곳: ' + ', '.join(sel))
log('')
log(f'중앙값(P50) 기준 집합 = {sorted(base_set)}')
for p in [40, 45, 55, 60]:
    c_cut = np.percentile(df['cls_old'], p)
    n_cut = np.percentile(df['new_rate'], p)
    sel = set(df.loc[(df['cls_old'] < c_cut) & (df['new_rate'] < n_cut), 'sigungu'])
    gained = sorted(sel - base_set)
    lost = sorted(base_set - sel)
    log(f'P{p} 대비: 추가 {gained if gained else "없음"} / 이탈 {lost if lost else "없음"}')
log('')
# 각 구의 컷까지 여유(마진)
med_c = df['cls_old'].median()
med_n = df['new_rate'].median()
med_a = df['age_pct'].median()
log(f'중앙값: 소멸 {med_c:.3f} / 개점 {med_n:.3f} / 고령 {med_a:.2f}%')
log('구군별 중앙값까지 마진 (음수 = 중앙값 미만):')
for _, r in df.sort_values('cls_old').iterrows():
    log(f"  {r['sigungu']:<5} 소멸 {r['cls_old']:>6.2f} ({r['cls_old']-med_c:+6.2f})"
        f"  개점 {r['new_rate']:>6.2f} ({r['new_rate']-med_n:+6.2f})"
        f"  고령 {r['age_pct']:>6.2f} ({r['age_pct']-med_a:+6.2f})")

# ---------- B. 발견쌍 강건성 ----------
log('')
log('=' * 72)
log('B. 발견쌍 강건성 — Kendall tau + 순열검정(스피어만, 20,000회)')
log('=' * 72)
rng = np.random.default_rng(20260906)


def spearman(x, y):
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    return np.corrcoef(rx, ry)[0, 1]


def kendall(x, y):
    n = len(x)
    conc = disc = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = np.sign(x[i] - x[j]) * np.sign(y[i] - y[j])
            if s > 0:
                conc += 1
            elif s < 0:
                disc += 1
    denom = n * (n - 1) / 2
    return (conc - disc) / denom


def perm_p(x, y, n_perm=20000):
    obs = spearman(x, y)
    y = np.asarray(y, dtype=float)
    cnt = 0
    for _ in range(n_perm):
        if abs(spearman(x, rng.permutation(y))) >= abs(obs):
            cnt += 1
    return obs, (cnt + 1) / (n_perm + 1)


try:
    from scipy import stats
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

for ycol, label in [('cls_old', '소멸률'), ('new_rate', '개점률')]:
    x = df['age_pct'].values
    y = df[ycol].values
    rho, pp = perm_p(x, y)
    tau = kendall(x, y)
    row = f'고령 x {label}:  스피어만 rho={rho:+.4f}  순열 p={pp:.4f}  켄달 tau={tau:+.4f}'
    if HAVE_SCIPY:
        t2, tp = stats.kendalltau(x, y)
        s2, sp = stats.spearmanr(x, y)
        row += f'  (scipy: tau p={tp:.4f}, spearman p={sp:.4f})'
    log(row)
log('')
log('해석 게이트: 순열 p가 기존 점근 p(.012/.027)와 크게 다르면 보고서 수치 재검토.')
log('켄달 tau는 방향·유의성 보조 확인용(본문 인용은 스피어만 유지).')

# ---------- C. 기존 지표 시야 검사 ----------
log('')
log('=' * 72)
log('C. 기존 지표 시야 검사 — 정체 5곳이 기존 지표에서 어디에 있나')
log('=' * 72)
BLIND = {'중구', '서구', '영도구', '사상구', '사하구'}
# C-1. MPI 35개월 평균 순위 (out1.rnk: 1 = MPI 최고 = 압박 최상위)
mpi_rank = d1.groupby('gu')['rnk'].mean().reset_index().merge(nm, on='gu')
mpi_rank = mpi_rank.sort_values('rnk').reset_index(drop=True)
mpi_rank['order'] = mpi_rank.index + 1
log('C-1. MPI(매입/매출 지수) 35개월 평균 순위 — 1위 = 압박 최상위:')
for _, r in mpi_rank.iterrows():
    mark = ' ◀ 정체' if r['sigungu'] in BLIND else ''
    log(f"  {int(r['order']):>2}위  {r['sigungu']:<5} 평균순위 {r['rnk']:5.2f}{mark}")
top8 = set(mpi_rank.head(8)['sigungu'])
log(f'  → MPI 상위 8곳 안에 든 정체 상권: {sorted(BLIND & top8) if BLIND & top8 else "없음"}'
    f' / 하위 8곳에 {len(BLIND - top8)}곳')
# C-2. 소멸률 순위 (높을수록 위기로 읽히는 기존 관행)
cls_rank = df.sort_values('cls_old', ascending=False).reset_index(drop=True)
cls_rank['order'] = cls_rank.index + 1
log('')
log('C-2. 소멸률 순위 — 1위 = 소멸 최다(기존 시각의 "위기"):')
for _, r in cls_rank.iterrows():
    mark = ' ◀ 정체' if r['sigungu'] in BLIND else ''
    log(f"  {int(r['order']):>2}위  {r['sigungu']:<5} 소멸률 {r['cls_old']:5.2f}%{mark}")
worst8 = set(cls_rank.head(8)['sigungu'])
log(f'  → 소멸률 상위 8곳(기존 시각 위기군)에 든 정체 상권: '
    f'{sorted(BLIND & worst8) if BLIND & worst8 else "없음"}')
# C-3. 판정 대조 2x2 (그림2 재료)
log('')
log('C-3. 판정 대조 2x2 (그림2 재료) — 행: 기존 지표(소멸률 상위 8 = 위기),'
    ' 열: 신진대사 판정(정체 5)')
a = len(worst8 & BLIND)
b = len(worst8 - BLIND)
c = len(BLIND - worst8)
d = 16 - a - b - c
log(f'                     신진대사 정체    정상')
log(f'  기존지표 위기       {a:>3}            {b:>3}')
log(f'  기존지표 정상       {c:>3}            {d:>3}')
log('')
log('C-4. MPI 기준으로도 동일 대조 — 행: MPI 평균순위 상위 8 = 압박:')
a2 = len(top8 & BLIND)
c2 = len(BLIND - top8)
log(f'  MPI 압박 상위 8곳 중 정체 상권: {a2}곳 / 정체 5곳 중 MPI 하위군: {c2}곳')
log('')
log('해석 게이트: C에서 정체 5곳이 기존 지표 상위에 몰려 있으면 "사각지대" 주장 폐기.')
log('반대로 하위(정상)에 몰려 있으면 "기존 지표로는 포착되지 않는다"를 수치로 지지.')
log('')
log('C-5. 방어선 — "MPI 상위에 정체 3곳이 겹치는데 MPI가 유용한 것 아닌가?"에 대한 답:')
from math import comb
N, K, n = 16, 8, 5
p_ge = sum(comb(K, k) * comb(N - K, n - k) for k in range(3, 6)) / comb(N, n)
exp = n * K / N
log(f'  초기하검정: 16곳 중 상위 8곳에 5곳 배치 시 기대 겹침 {exp:.1f}곳, 관측 3곳,'
    f' P(X>=3)={p_ge:.3f}')
log('  → 겹침 3곳은 우연 수준(기대값 2.5와 사실상 동일). MPI가 정체 상권을')
log('    선별한다는 증거가 아니며, MPI-소멸 상관 미지지(-0.115)와 모순되지 않는다.')

txt = NL.join(lines)
import os
os.makedirs(OUTDIR, exist_ok=True)
with open(OUTDIR + '/강건성_추가검증.txt', 'w', encoding='utf-8-sig') as f:
    f.write(txt + NL)
print('saved', OUTDIR + '/강건성_추가검증.txt')
print('lines:', len(lines))
