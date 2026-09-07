# -*- coding: utf-8 -*-
# 시각화 1장 최종 합성 — A4 가로: 산점도 2패널(좌) + 타일 지도(우상) + 콜아웃(우하)
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

BASE = 'C:/Users/진세운/Desktop/빅데이터 대회'
EXP = BASE + '/0_부산 데이터 오픈랩 09.03. 반출 신청 데이터_260904'
OUT = BASE + '/제출자료/1_시각화'

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
SURF = '#fcfcfb'; INK = '#0b0b0b'; INK2 = '#52514e'; GRID = '#e8e7e4'
C_ETC = '#2a78d6'; C_OLD = '#eb6834'; C_EX = '#1baf7a'; C_TILE_ETC = '#9ec3ee'

d7 = pd.read_csv(EXP + '/out7_gu_closure.csv', encoding='utf-8-sig', dtype={'gu': str})
nm = pd.read_csv(BASE + '/data/구군코드_매핑.csv', encoding='utf-8-sig', dtype={'gu': str})
nn = pd.read_csv(BASE + '/data/구군_가맹점수_n_old_new.csv', encoding='utf-8-sig', comment='#', dtype={'gu': str})
df = d7.merge(nm, on='gu').merge(nn[['gu', 'n_old', 'n_new']], on='gu')
df['age_pct'] = df['age'] * 100
df['n_tot'] = df['n_old'] + df['n_new']
BLIND = ['중구', '서구', '영도구', '사상구', '사하구']
df['grp'] = 'etc'
df.loc[df['sigungu'].isin(BLIND), 'grp'] = 'blind'
df.loc[df['sigungu'] == '동구', 'grp'] = 'ex'

fig = plt.figure(figsize=(16.5, 11.7), facecolor=SURF)   # A4 가로 비율 확대판
gs = fig.add_gridspec(2, 2, left=0.05, right=0.985, top=0.845, bottom=0.055,
                      wspace=0.14, hspace=0.30, width_ratios=[1.15, 1.0])
axL1 = fig.add_subplot(gs[0, 0])
axL2 = fig.add_subplot(gs[1, 0])
axR1 = fig.add_subplot(gs[0, 1])
axR2 = fig.add_subplot(gs[1, 1])

# ---------- 제목부
fig.suptitle('고객이 늙은 상권일수록, 가게는 닫히지도 새로 열리지도 않는다',
             fontsize=23, color=INK, x=0.05, y=0.965, ha='left', fontweight='bold')
fig.text(0.05, 0.925, '부산 16개 구·군 | 가맹점 신진대사(소멸·개점): BC카드, 2023.06~2026.04 · 35개월 누적 | '
         '고객 연령: 동백전, 2023.06~2023.09 겹침 구간 | n=16 스피어만 순위상관 · 탐색적',
         fontsize=11.5, color=INK2)
fig.text(0.05, 0.900, '소멸률 = BC카드 가맹 종료 기준(행정 폐업의 대리지표) · 버블 크기 = 가맹점 수 · '
         '부산 빅데이터 오픈랩 반출 승인 산출물', fontsize=11.5, color=INK2)

# ---------- 좌측: 산점도 2패널
smin, smax = 100, 780
sz = smin + (df['n_tot'] - df['n_tot'].min()) / (df['n_tot'].max() - df['n_tot'].min()) * (smax - smin)
nudge = {
    ('cls_old', '해운대구'): (-56, -3), ('cls_old', '동래구'): (-12, 11), ('cls_old', '부산진구'): (11, 6),
    ('cls_old', '금정구'): (12, -4), ('cls_old', '연제구'): (-18, -15), ('cls_old', '사하구'): (10, -12),
    ('cls_old', '수영구'): (10, 4), ('cls_old', '남구'): (9, 4), ('cls_old', '북구'): (0, 10),
    ('cls_old', '기장군'): (10, -3), ('cls_old', '강서구'): (0, -15), ('cls_old', '사상구'): (0, -15),
    ('cls_old', '영도구'): (-46, 3), ('cls_old', '서구'): (10, -4), ('cls_old', '동구'): (10, 2),
    ('cls_old', '중구'): (-40, -4),
    ('new_rate', '해운대구'): (-56, -4), ('new_rate', '수영구'): (10, 6), ('new_rate', '남구'): (-36, 6),
    ('new_rate', '연제구'): (-42, -2), ('new_rate', '부산진구'): (12, 4), ('new_rate', '북구'): (12, -8),
    ('new_rate', '동래구'): (-12, -15), ('new_rate', '금정구'): (12, -4), ('new_rate', '사하구'): (0, -14),
    ('new_rate', '기장군'): (10, -4), ('new_rate', '강서구'): (10, -4), ('new_rate', '사상구'): (0, -15),
    ('new_rate', '영도구'): (-14, 10), ('new_rate', '서구'): (9, -13), ('new_rate', '동구'): (-40, 4),
    ('new_rate', '중구'): (-40, -3),
}
panels = [(axL1, 'cls_old', '기존 가맹점 소멸률 (%)', '① 가게가 문을 닫는가', 'ρ = -0.61'),
          (axL2, 'new_rate', '신규 개점 가맹점 비중 (%)', '② 가게가 새로 생기는가', 'ρ = -0.55')]
for ax, ycol, ylab, ptitle, rho in panels:
    ax.set_facecolor(SURF)
    ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
    for sp in ['top', 'right']: ax.spines[sp].set_visible(False)
    for sp in ['left', 'bottom']: ax.spines[sp].set_color(GRID)
    for g, color in [('etc', C_ETC), ('blind', C_OLD), ('ex', C_EX)]:
        sub = df[df['grp'] == g]
        ax.scatter(sub['age_pct'], sub[ycol], s=sz[sub.index], c=color,
                   edgecolors=SURF, linewidths=2, zorder=3, alpha=0.95)
    for _, r in df.iterrows():
        dx, dy = nudge.get((ycol, r['sigungu']), (9, 0))
        ax.annotate(r['sigungu'], (r['age_pct'], r[ycol]), xytext=(dx, dy),
                    textcoords='offset points', fontsize=9,
                    color=INK if r['grp'] != 'etc' else INK2, zorder=4,
                    fontweight='bold' if r['grp'] != 'etc' else 'normal')
    ax.set_title(ptitle, fontsize=14, color=INK, pad=8, fontweight='bold', loc='left')
    ax.set_ylabel(ylab, fontsize=10, color=INK2)
    ax.text(0.985, 0.955, '스피어만 ' + rho, transform=ax.transAxes, ha='right', va='top',
            fontsize=10.5, color=INK2)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.set_xlim(12.2, 31.2)
axL2.set_xlabel('60세 이상 고객 결제액 비중 (%) — 동백전, 2023.06~2023.09 겹침 구간', fontsize=10, color=INK2)
axL1.set_xlabel('')

# ---------- 우상: 타일 지도
POS = {'금정구': (3, 0), '기장군': (4, 0),
       '북구': (2, 1), '동래구': (3, 1), '해운대구': (4, 1),
       '강서구': (0, 2), '사상구': (1, 2), '부산진구': (2, 2), '연제구': (3, 2), '수영구': (4, 2),
       '사하구': (1, 3), '서구': (2, 3), '동구': (3, 3), '남구': (4, 3),
       '중구': (2, 4), '영도구': (3, 4)}
dfx = df.set_index('sigungu')
axR1.set_facecolor(SURF)
axR1.set_xlim(-0.15, 5.05)
axR1.set_ylim(5.05, -0.5)
axR1.set_axis_off()
axR1.set_title('③ 사각지대는 어디인가 — 타일 지도', fontsize=14, color=INK, loc='left',
               pad=8, fontweight='bold')
for name, (c, r) in POS.items():
    if name in BLIND: fill, tcol = C_OLD, '#ffffff'
    elif name == '동구': fill, tcol = C_EX, '#ffffff'
    else: fill, tcol = C_TILE_ETC, INK2
    axR1.add_patch(FancyBboxPatch((c + 0.05, r + 0.05), 0.9, 0.9,
                   boxstyle='round,pad=0.012,rounding_size=0.06', linewidth=0, facecolor=fill))
    row = dfx.loc[name]
    axR1.text(c + 0.5, r + 0.34, name, ha='center', va='center', fontsize=10.5,
              fontweight='bold', color=INK if fill == C_TILE_ETC else tcol)
    axR1.text(c + 0.5, r + 0.60, f"소멸 {row['cls_old']:.1f}", ha='center', va='center',
              fontsize=8, color=INK2 if fill == C_TILE_ETC else tcol)
    axR1.text(c + 0.5, r + 0.79, f"개점 {row['new_rate']:.1f}", ha='center', va='center',
              fontsize=8, color=INK2 if fill == C_TILE_ETC else tcol)
axR1.text(0, 5.02, '타일 위치는 대략적 지리 배치 (실제 경계 아님) · 단위 %', fontsize=8.5, color=INK2)

# ---------- 우하: 콜아웃 3 + 범례
axR2.set_axis_off()
axR2.set_facecolor(SURF)
cards = [
    ('19.76%', '동백전 결제액 중 60세 이상 비중\n(부산 전체 · 관측 전 기간, 결제 1억 2,842만 건)'),
    ('+4.5%p', '관측 전반기 대비 후반기\n60세+ 비중 상승 (행정동 평균)'),
    ('5곳', '소멸·개점 모두 중앙값 미만 (정체 상권)\n= 중구·서구·영도구·사상구·사하구'),
]
for i, (big, small) in enumerate(cards):
    x0 = 0.005 + i * 0.34
    axR2.add_patch(FancyBboxPatch((x0, 0.42), 0.31, 0.46, transform=axR2.transAxes,
                   boxstyle='round,pad=0.012,rounding_size=0.03',
                   linewidth=1.2, edgecolor=GRID, facecolor='#ffffff'))
    axR2.text(x0 + 0.155, 0.74, big, transform=axR2.transAxes, ha='center', va='center',
              fontsize=21, fontweight='bold', color=C_OLD if i == 2 else INK)
    axR2.text(x0 + 0.155, 0.545, small, transform=axR2.transAxes, ha='center', va='center',
              fontsize=8.7, color=INK2)
legend = [
    Line2D([0], [0], marker='o', color='none', markerfacecolor=C_OLD, markeredgecolor=SURF,
           markersize=12, label='정체 상권 5곳 (중·서·영도·사상·사하) — 소멸률 지표로는 "안정", 신진대사로는 "정체"'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor=C_EX, markeredgecolor=SURF,
           markersize=12, label='예외: 동구 (고령 최상위지만 개점은 활발 — 다축 판정이 필요한 이유)'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor=C_ETC, markeredgecolor=SURF,
           markersize=12, label='그 외 구·군'),
]
axR2.legend(handles=legend, loc='lower left', bbox_to_anchor=(-0.02, -0.06),
            frameon=False, fontsize=10, labelcolor=INK2, handletextpad=0.4,
            borderaxespad=0)
axR2.text(0.0, 0.30, '해석 지침: 상관은 동행 관계이며 인과가 아님 · 9변수 36쌍 탐색 중 발견된 탐색적 신호\n'
          '(가맹점 수 통제 부분상관 -0.68/-0.66 · 구군 1곳씩 제외 시 부호 불변)',
          transform=axR2.transAxes, fontsize=8.7, color=INK2, va='top')

import os
os.makedirs(OUT, exist_ok=True)
fig.savefig(OUT + '/시각화_1장_최종.pdf', facecolor=SURF)
fig.savefig(OUT + '/시각화_1장_최종.png', dpi=150, facecolor=SURF)
print('saved onepager')
