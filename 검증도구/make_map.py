# -*- coding: utf-8 -*-
# 부산 구군 판정 지도 초안 — 공개 경계(southkorea-maps, KOSTAT 2013) + 반출 승인 판정
import io, json
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BASE = 'C:/Users/진세운/Desktop/빅데이터 대회'
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

SURF = '#fcfcfb'
INK = '#0b0b0b'
INK2 = '#52514e'
C_ETC = '#9ec3ee'    # 기타: slot1 파랑의 연한 단계 (배경 역할)
C_OLD = '#eb6834'    # 사각지대
C_EX = '#1baf7a'     # 예외 동구

g = gpd.read_file(BASE + '/data/경계/skorea_municipalities.json')
bs = g[g['code'].astype(str).str.startswith('21')].copy()

BLIND = ['중구', '서구', '영도구', '사상구', '사하구']
def color_of(nm):
    if nm in BLIND: return C_OLD
    if nm == '동구': return C_EX
    return C_ETC
bs['fill'] = bs['name'].map(color_of)

fig, ax = plt.subplots(figsize=(7.5, 7.2), facecolor=SURF)
ax.set_facecolor(SURF)
bs.plot(ax=ax, color=bs['fill'], edgecolor=SURF, linewidth=1.6)
ax.set_axis_off()

# 라벨: 큰 구는 내부, 작은 원도심은 지시선으로 바깥
cent = bs.copy()
cent['pt'] = cent.geometry.representative_point()
outside = {  # (라벨 위치 dx, dy in 도 단위)
    '중구':  (-0.115, -0.045), '서구': (-0.13, 0.005), '동구': (-0.02, -0.095),
    '영도구': (0.05, -0.075),
}
for _, r in cent.iterrows():
    x, y = r['pt'].x, r['pt'].y
    nm = r['name']
    strong = nm in BLIND or nm == '동구'
    if nm in outside:
        dx, dy = outside[nm]
        ax.annotate(nm, (x, y), xytext=(x + dx, y + dy), fontsize=10.5,
                    fontweight='bold', color=INK,
                    arrowprops=dict(arrowstyle='-', color=INK2, lw=0.9),
                    ha='center', va='center', zorder=6)
    else:
        ax.annotate(nm, (x, y), ha='center', va='center', fontsize=9.5,
                    color=INK if strong else INK2,
                    fontweight='bold' if strong else 'normal', zorder=5)

ax.set_title('판정 사각지대는 어디인가 — 부산 원도심과 사상구', fontsize=15,
             color=INK, loc='left', pad=14, fontweight='bold')
ax.text(0, 1.005, '고령 고객 상위 & 가맹점 종료·개점 모두 하위 (반출 승인 산출물 기준, 2023.06~2026.04)',
        transform=ax.transAxes, fontsize=9.5, color=INK2)

legend = [
    Line2D([0], [0], marker='s', color='none', markerfacecolor=C_OLD, markersize=13,
           label='정체 상권 5곳 (중·서·영도·사상·사하)'),
    Line2D([0], [0], marker='s', color='none', markerfacecolor=C_EX, markersize=13,
           label='예외: 동구 (개점은 활발)'),
    Line2D([0], [0], marker='s', color='none', markerfacecolor=C_ETC, markersize=13,
           label='그 외 구·군'),
]
ax.legend(handles=legend, loc='upper left', bbox_to_anchor=(0.0, 0.98),
          frameon=False, fontsize=9.5, labelcolor=INK2)

fig.savefig(BASE + '/지도_초안.png', dpi=160, facecolor=SURF, bbox_inches='tight')
print('saved 지도_초안.png')
