# -*- coding: utf-8 -*-
# 그림 2 — 판정 대조: 닫힘 단일 지표 vs 신진대사 판정 (보고서 4-1/4-2용)
# x=소멸률(닫힘 지표), y=개점률. 중앙값 십자선 → 좌하 4분면 = 정체 상권 5곳.
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BASE = 'C:/Users/진세운/Desktop/빅데이터 대회'
EXP = BASE + '/0_부산 데이터 오픈랩 09.03. 반출 신청 데이터_260904'
OUT = BASE + '/제출자료/1_시각화'
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
SURF = '#fcfcfb'; INK = '#0b0b0b'; INK2 = '#52514e'; GRID = '#e8e7e4'
C_ETC = '#2a78d6'; C_OLD = '#eb6834'; C_EX = '#1baf7a'

d7 = pd.read_csv(EXP + '/out7_gu_closure.csv', dtype={'gu': str})
nm = pd.read_csv(BASE + '/data/구군코드_매핑.csv', encoding='utf-8-sig', dtype={'gu': str})
df = d7.merge(nm, on='gu')
BLIND = ['중구', '서구', '영도구', '사상구', '사하구']
med_c = df['cls_old'].median()
med_n = df['new_rate'].median()

fig, ax = plt.subplots(figsize=(9.6, 7.6), facecolor=SURF)
ax.set_facecolor(SURF)
for sp in ['top', 'right']:
    ax.spines[sp].set_visible(False)
for sp in ['left', 'bottom']:
    ax.spines[sp].set_color(GRID)
ax.grid(True, color=GRID, linewidth=0.8, zorder=0)

# 좌하 4분면 배경 음영
ax.axvspan(8.0, med_c, ymin=0, ymax=(med_n - 21.5) / (40.5 - 21.5),
           color='#f8e3d8', alpha=0.55, zorder=0)
ax.axvline(med_c, color=INK2, linewidth=1.0, linestyle='--', zorder=1)
ax.axhline(med_n, color=INK2, linewidth=1.0, linestyle='--', zorder=1)

nudge = {'해운대구': (-58, -4), '수영구': (10, 4), '남구': (10, 2), '기장군': (-14, 9),
         '강서구': (-50, 2), '동구': (10, 3), '연제구': (-16, 9), '금정구': (10, -11),
         '동래구': (10, -2), '부산진구': (-30, 10), '북구': (10, -3), '사하구': (10, -4),
         '서구': (10, 2), '영도구': (-10, 10), '중구': (10, -3), '사상구': (10, -3)}
for _, r in df.iterrows():
    if r['sigungu'] in BLIND:
        col = C_OLD
    elif r['sigungu'] == '동구':
        col = C_EX
    else:
        col = C_ETC
    ax.scatter(r['cls_old'], r['new_rate'], s=170, c=col, edgecolors=SURF,
               linewidths=2, zorder=3)
    dx, dy = nudge.get(r['sigungu'], (10, 0))
    ax.annotate(r['sigungu'], (r['cls_old'], r['new_rate']), xytext=(dx, dy),
                textcoords='offset points', fontsize=10, zorder=4,
                color=INK if col != C_ETC else INK2,
                fontweight='bold' if col != C_ETC else 'normal')

ax.set_xlim(8.0, 15.8)
ax.set_ylim(21.5, 40.5)
ax.set_xlabel('기존 가맹점 소멸률 (%) — 닫힘 지표\n'
              '◀ 닫힘 지표의 시각으로는 "안정"          닫힘 지표의 시각으로는 "위기" ▶',
              fontsize=11, color=INK)
ax.set_ylabel('신규 개점 가맹점 비중 (%)', fontsize=11, color=INK2)
ax.tick_params(colors=INK2, labelsize=10)

# 4분면 이름표
ax.text(8.15, 21.75, '소멸·개점 모두 중앙값 미만 = 정체 상권 5곳\n'
        '닫힘 지표로는 점검 대상에서 빠진다', fontsize=10.5, color='#b5502a',
        fontweight='bold', va='bottom')
ax.text(15.65, 33.8, '소멸·개점 모두 높음 = 활발한 신진대사\n닫힘 지표로는 "위기"로 읽힌다',
        fontsize=10, color=INK2, ha='right', va='top')
ax.text(8.2, 39.8, '닫히지 않고 열림 (동구 예외)', fontsize=10, color='#12825a', va='top')

# 사상구 콜아웃
sas = df[df['sigungu'] == '사상구'].iloc[0]
ax.annotate('사상구: 소멸률 16곳 중 최저 = 닫힘 지표 "최안정"\n'
            '그러나 개점률도 최저 = 신진대사 "최정체"',
            (sas['cls_old'], sas['new_rate']), xytext=(9.35, 25.0), fontsize=10,
            color=INK, arrowprops=dict(arrowstyle='-', color=INK2, lw=0.9), va='center')

ax.set_title('같은 데이터, 다른 지표, 정반대의 판정', fontsize=16.5, color=INK,
             loc='left', pad=30, fontweight='bold')
ax.text(0, 1.045, '부산 16개 구·군 | BC카드 가맹 기준 2023.06~2026.04 (35개월 누적) · '
        '점선 = 16곳 중앙값 (소멸 12.19% · 개점 30.70%) | 반출 승인 산출물',
        transform=ax.transAxes, fontsize=10, color=INK2)
ax.text(0, 1.008, '소멸률 상위 8곳(닫힘 지표 "위기"군)에 정체 상권 0곳 — 정체 5곳은 모두 '
        '닫힘 지표 "안정"권(9·12·13·15·16위)', transform=ax.transAxes, fontsize=10, color=INK2)

legend = [
    Line2D([0], [0], marker='o', color='none', markerfacecolor=C_OLD, markeredgecolor=SURF,
           markersize=11, label='정체 상권 5곳 (중·서·영도·사상·사하)'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor=C_EX, markeredgecolor=SURF,
           markersize=11, label='예외: 동구 (소멸 낮음 + 개점 활발)'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor=C_ETC, markeredgecolor=SURF,
           markersize=11, label='그 외 구·군'),
]
ax.legend(handles=legend, loc='upper center', bbox_to_anchor=(0.5, 1.0),
          frameon=False, fontsize=9.5, labelcolor=INK2)

fig.tight_layout()
fig.savefig(OUT + '/그림2_판정대조.png', dpi=200, facecolor=SURF, bbox_inches='tight')
fig.savefig(OUT + '/그림2_판정대조.pdf', facecolor=SURF, bbox_inches='tight')
print('saved fig2')
