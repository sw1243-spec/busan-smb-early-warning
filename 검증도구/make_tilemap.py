# -*- coding: utf-8 -*-
# 부산 16개 구군 타일 지도(카토그램) — 면적 왜곡 없이 지리 배치 유지
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

BASE = 'C:/Users/진세운/Desktop/빅데이터 대회'
EXP = BASE + '/0_부산 데이터 오픈랩 09.03. 반출 신청 데이터_260904'
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

SURF = '#fcfcfb'; INK = '#0b0b0b'; INK2 = '#52514e'
C_ETC = '#9ec3ee'; C_OLD = '#eb6834'; C_EX = '#1baf7a'

# 대략적 지리 배치 (col, row) — row 0이 북쪽
POS = {
    '금정구': (3, 0), '기장군': (4, 0),
    '북구': (2, 1), '동래구': (3, 1), '해운대구': (4, 1),
    '강서구': (0, 2), '사상구': (1, 2), '부산진구': (2, 2), '연제구': (3, 2), '수영구': (4, 2),
    '사하구': (1, 3), '서구': (2, 3), '동구': (3, 3), '남구': (4, 3),
    '중구': (2, 4), '영도구': (3, 4),
}
BLIND = ['중구', '서구', '영도구', '사상구', '사하구']

d7 = pd.read_csv(EXP + '/out7_gu_closure.csv', encoding='utf-8-sig', dtype={'gu': str})
nm = pd.read_csv(BASE + '/data/구군코드_매핑.csv', encoding='utf-8-sig', dtype={'gu': str})
df = d7.merge(nm, on='gu').set_index('sigungu')

fig, ax = plt.subplots(figsize=(7.6, 7.0), facecolor=SURF)
ax.set_facecolor(SURF)
ax.set_xlim(-0.25, 5.05)
ax.set_ylim(5.0, -0.85)
ax.set_axis_off()

for name, (c, r) in POS.items():
    if name in BLIND:
        fill = C_OLD; tcol = '#ffffff'
    elif name == '동구':
        fill = C_EX; tcol = '#ffffff'
    else:
        fill = C_ETC; tcol = INK2
    box = FancyBboxPatch((c + 0.05, r + 0.05), 0.9, 0.9,
                         boxstyle='round,pad=0.012,rounding_size=0.06',
                         linewidth=0, facecolor=fill)
    ax.add_patch(box)
    row = df.loc[name]
    ax.text(c + 0.5, r + 0.36, name, ha='center', va='center',
            fontsize=11.5, fontweight='bold', color=INK if fill == C_ETC else tcol)
    ax.text(c + 0.5, r + 0.62, f"종료 {row['cls_old']:.1f}%", ha='center', va='center',
            fontsize=8.6, color=INK2 if fill == C_ETC else tcol)
    ax.text(c + 0.5, r + 0.80, f"개점 {row['new_rate']:.1f}%", ha='center', va='center',
            fontsize=8.6, color=INK2 if fill == C_ETC else tcol)

ax.set_title('판정 사각지대는 어디인가 — 타일 지도 (면적 왜곡 없음)',
             fontsize=15, color=INK, loc='left', pad=16, fontweight='bold')
ax.text(0, -0.62, '타일 위치 = 대략적 지리 배치 · 가맹 종료·개점 모두 중앙값 미만 = 주황 (정체 상권)'
        '\n종료·개점 = BC카드 가맹 기준 35개월 누적 (반출 승인 산출물)',
        fontsize=9.3, color=INK2)

legend = [
    Line2D([0], [0], marker='s', color='none', markerfacecolor=C_OLD, markersize=13,
           label='정체 상권 5곳 (중·서·영도·사상·사하)'),
    Line2D([0], [0], marker='s', color='none', markerfacecolor=C_EX, markersize=13,
           label='예외: 동구 (개점은 활발)'),
    Line2D([0], [0], marker='s', color='none', markerfacecolor=C_ETC, markersize=13,
           label='그 외 구·군'),
]
ax.legend(handles=legend, loc='lower left', bbox_to_anchor=(0.0, 0.02),
          frameon=False, fontsize=9.3, labelcolor=INK2)

fig.savefig(BASE + '/지도_타일_초안.png', dpi=160, facecolor=SURF, bbox_inches='tight')
print('saved 지도_타일_초안.png')
