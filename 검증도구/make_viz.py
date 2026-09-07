# -*- coding: utf-8 -*-
# 시각화 1장 초안 — 반출 승인 수치만 사용
# 팔레트: dataviz 검증기 ALL PASS (#2a78d6, #eb6834 / surface #fcfcfb)
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.font_manager as fm

BASE = 'C:/Users/진세운/Desktop/빅데이터 대회'
EXP = BASE + '/0_부산 데이터 오픈랩 09.03. 반출 신청 데이터_260904'

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

SURF = '#fcfcfb'
INK = '#0b0b0b'
INK2 = '#52514e'
C_ETC = '#2a78d6'    # slot1 파랑 = 그 외 구군
C_OLD = '#eb6834'    # slot2 주황 = 정체 상권 5곳 (중·서·영도·사상·사하)
C_EX  = '#1baf7a'    # slot3 아쿠아 = 예외 동구 (종료 낮음·개점 활발)
GRID = '#e8e7e4'

d7 = pd.read_csv(EXP + '/out7_gu_closure.csv', encoding='utf-8-sig')
nm = pd.read_csv(BASE + '/data/구군코드_매핑.csv', encoding='utf-8-sig', dtype={'gu': str})
nn = pd.read_csv(BASE + '/data/구군_가맹점수_n_old_new.csv', encoding='utf-8-sig', comment='#', dtype={'gu': str})
d7['gu'] = d7['gu'].astype(str)
df = d7.merge(nm, on='gu').merge(nn[['gu', 'n_old', 'n_new']], on='gu')
df['age_pct'] = df['age'] * 100
df['n_tot'] = df['n_old'] + df['n_new']

BLIND = ['중구', '서구', '영도구', '사상구', '사하구']   # 고령 상위 & 종료·개점 모두 중앙값 미만
df['grp'] = 'etc'
df.loc[df['sigungu'].isin(BLIND), 'grp'] = 'blind'
df.loc[df['sigungu'] == '동구', 'grp'] = 'ex'

fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6), facecolor=SURF, sharex=True)
fig.subplots_adjust(left=0.06, right=0.985, top=0.76, bottom=0.13, wspace=0.16)

panels = [
    ('cls_old', '기존 가맹점 소멸률 (%)', '가게가 문을 닫는가', 'ρ = -0.61'),
    ('new_rate', '신규 개점 가맹점 비중 (%)', '가게가 새로 생기는가', 'ρ = -0.55'),
]

smin, smax = 120, 900
sz = smin + (df['n_tot'] - df['n_tot'].min()) / (df['n_tot'].max() - df['n_tot'].min()) * (smax - smin)

# 라벨 겹침 수동 오프셋 (구군명: (dx, dy) 포인트)
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
for ax, (ycol, ylab, ptitle, rho) in zip(axes, panels):
    ax.set_facecolor(SURF)
    ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(GRID)
    for g, color in [('etc', C_ETC), ('blind', C_OLD), ('ex', C_EX)]:
        sub = df[df['grp'] == g]
        ax.scatter(sub['age_pct'], sub[ycol], s=sz[sub.index], c=color,
                   edgecolors=SURF, linewidths=2, zorder=3, alpha=0.95)
    for _, r in df.iterrows():
        dx, dy = nudge.get((ycol, r['sigungu']), (9, 0))
        ax.annotate(r['sigungu'], (r['age_pct'], r[ycol]),
                    xytext=(dx, dy), textcoords='offset points',
                    fontsize=8.5, color=INK if r['grp'] != 'etc' else INK2, zorder=4,
                    fontweight='bold' if r['grp'] != 'etc' else 'normal')
    ax.set_title(ptitle, fontsize=12, color=INK, pad=10, fontweight='bold', loc='left')
    ax.set_ylabel(ylab, fontsize=9.5, color=INK2)
    ax.set_xlabel('60세 이상 고객 결제액 비중 (%)  —  동백전, 2023.06~2023.09 겹침 구간', fontsize=9.5, color=INK2)
    ax.text(0.985, 0.955, '스피어만 ' + rho, transform=ax.transAxes, ha='right', va='top',
            fontsize=9.5, color=INK2)
    ax.tick_params(colors=INK2, labelsize=8.5)
    ax.set_xlim(12.2, 31.2)

fig.suptitle('고객이 늙은 상권일수록, 가게는 닫히지도 새로 열리지도 않는다',
             fontsize=16, color=INK, x=0.06, y=0.965, ha='left', fontweight='bold')
fig.text(0.06, 0.870, '부산 16개 구·군 · BC카드 가맹점 신진대사 2023.06~2026.04 (35개월 누적) · 버블 크기 = 가맹점 수 · n=16 탐색적 상관\n'
         '종료율 = BC카드 가맹 종료 기준(행정 폐업의 대리지표) · 부산 빅데이터 오픈랩 반출 승인 산출물',
         fontsize=9.5, color=INK2)

legend = [
    Line2D([0], [0], marker='o', color='none', markerfacecolor=C_OLD, markeredgecolor=SURF,
           markersize=11, label='정체 상권 5곳 (중·서·영도·사상·사하)'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor=C_EX, markeredgecolor=SURF,
           markersize=11, label='예외: 동구 (개점은 활발)'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor=C_ETC, markeredgecolor=SURF,
           markersize=11, label='그 외 구·군'),
]
fig.legend(handles=legend, loc='upper right', bbox_to_anchor=(0.985, 0.865),
           frameon=False, fontsize=9, labelcolor=INK2, ncol=3)

fig.savefig(BASE + '/시각화_초안.pdf', facecolor=SURF)
fig.savefig(BASE + '/시각화_초안.png', dpi=160, facecolor=SURF)
print('saved 시각화_초안.pdf / .png')
