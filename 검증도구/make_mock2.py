# -*- coding: utf-8 -*-
# mock v2 : 정의서(3.데이터_정의서.pdf) 원문 컬럼명 그대로.
# v1 은 내 잘못된 가정으로 만들어 코드의 오류를 검증하지 못했다.
# 함정을 의도적으로 심는다.
import os, io, random, shutil
random.seed(11)

ROOT = "D:/mocklab2/20260901_mock"
if os.path.exists(ROOT):
    shutil.rmtree(ROOT)
os.makedirs(ROOT)

PIPE = ['CRD020','CRD021','CRD022','CRD023','CRD024','CRD025','CRD026',
        'POP019','POP022','SPN020','SPN058','SPN059','SPN082',
        'SPN088','SPN089','SPN090','SPN091','SPN092','TOU007']
COMMA = ['POP001','POP014','REL015','SPN057','SPN060','SPN093','SPN094']

GU = ['26110','26140','26170','26200','26230','26260','26290','26320',
      '26350','26380','26410','26440','26470','26500','26530','26710']
ADM8  = [g + str(i).zfill(3) for g in GU for i in range(1, 14)][:205]      # 행정동 8자리
ADM10 = [g + str(i).zfill(5) for g in GU for i in range(1, 14)][:205]     # 행정동 10자리
BJD10 = [g + str(i).zfill(5) for g in GU for i in range(50, 66)][:254]    # 법정동 10자리
YM_KCD = ['202306', '202307', '202308', '202309']
YM_DBJ = ['202201', '202207', '202212', '202306', '202309']
LCLS = ['A', 'B', 'C', 'D']
MCLS = ['A01', 'A02', 'B01', 'C01']


def w(tab, fname, header, rows, d, hdr=True):
    p = ROOT + "/" + tab
    if not os.path.exists(p):
        os.makedirs(p)
    f = io.open(p + "/" + fname, "w", encoding="utf-8", newline="")
    if hdr:
        f.write(d.join(header) + "\n")
    for r in rows:
        f.write(d.join([str(x) for x in r]) + "\n")
    f.close()


# ---------- SPN088 카드매출 (행정동 10자리)
H88 = ['CRTR_YMD','ADMNST_CD','INDST_SE_LCLS_CD','INDST_SE_MCLS_CD','TME_CD','CARD_SLS_AMT','CARD_SLS_CNT']
for ym in YM_KCD:
    rows = [[ym+'01', cd, LCLS[k], MCLS[k], '12', round(random.uniform(3e6, 9e6), 2), random.randint(9, 500)]
            for cd in ADM10 for k in range(3)]
    w('SPN088', 'SPN088_'+ym+'.csv', H88, rows, '|')

# ---------- SPN089 현금+세금계산서 매출 (금액 컬럼 2개. 일부 공란 = 함정)
H89 = ['CRTR_YMD','ADMNST_CD','INDST_SE_LCLS_CD','INDST_SE_MCLS_CD',
       'CASH_SLS_AMT','CASH_SLS_CNT','TAX_SLS_AMT','TAX_SLS_CNT']
for ym in YM_KCD:
    rows = []
    for cd in ADM10:
        for k in range(3):
            tax = '' if random.random() < 0.25 else round(random.uniform(2e5, 2e6), 2)
            rows.append([ym+'01', cd, LCLS[k], MCLS[k],
                         round(random.uniform(1e5, 1e6), 2), random.randint(1, 90),
                         tax, random.randint(0, 30)])
    w('SPN089', 'SPN089_'+ym+'.csv', H89, rows, '|')

# ---------- SPN090 매입 : 법정동 코드 (정의서 비고대로. 최악 시나리오 함정)
H90 = ['CRTR_YMD','ADMNST_CD','INDST_SE_LCLS_CD','INDST_SE_MCLS_CD',
       'CASH_PRCH_AMT','CASH_PRCH_CNT','TAX_PRCH_AMT','TAX_PRCH_CNT']
for ym in YM_KCD:
    rows = [[ym+'01', cd, LCLS[k], MCLS[k],
             round(random.uniform(3e5, 2e6), 2), random.randint(1, 60),
             round(random.uniform(5e5, 3e6), 2), random.randint(1, 40)]
            for cd in BJD10 for k in range(3)]
    w('SPN090', 'SPN090_'+ym+'.csv', H90, rows, '|')

# ---------- SPN091 메뉴
H91 = ['CRTR_YMD','ADMNST_CD','INDST_SE_LCLS_CD','INDST_SE_MCLS_CD','MENU_STD_NM',
       'MENU_LCLS_NM','MENU_MCLS_NM','MENU_SCLS_NM','MENU_PRC','MENU_SLS_AMT','MENU_SLS_CNT']
for ym in YM_KCD:
    rows = [[ym+'01', cd, 'A', 'A01', 'MENU', 'L', 'M', 'S',
             random.randint(4000, 20000), random.randint(100000, 900000), random.randint(5, 90)]
            for cd in ADM10[:50]]
    w('SPN091', 'SPN091_'+ym+'.csv', H91, rows, '|')

# ---------- SPN059 동백전 행정동 (ADM_CD = 8자리. 함정: 한 달은 기준일자 공란)
H59 = ['STRD_DATE','STRD_TIME','CITY_NM','SIGU_NM','ADM_NM','ADM_CD','CARD_CO_NM',
       'BUSIN_CD','BUSIN_NM','BIRTH_YEAR','GENDER','TRANS_CNT','TRANS_SUM','LOAD_DTM','CENTER_CD']
for ym in YM_DBJ:
    rows = []
    for cd in ADM8:
        for by in [1950, 1958, 1966, 1979, 1991, 1999]:
            d = '' if ym == '202212' else ym + '15'      # <<< 함정: 202212 는 기준일자 공란
            rows.append([d, '12', 'BUSAN', 'GU', 'DONG', cd, 'BC', '4010', 'CVS',
                         by, random.choice(['M','F']), random.randint(1, 80),
                         random.randint(9000, 800000), '20230101000000', 'ZZZZZZ'])
    w('SPN059', 'SPN059_'+ym+'.csv', H59, rows, '|')

# ---------- SPN060 집계구 (COMMA)
H60 = ['STRD_DATE','STRD_TIME','CITY_NM','SIGU_NM','ADM_NM','TZ_AREA_VAL','TZ_AREA_XCRDT_VAL',
       'TZ_AREA_YCRDT_VAL','CARD_CO_NM','BUSIN_CD','BUSIN_NM','BIRTH_YEAR','GENDER',
       'TRANS_CNT','TRANS_SUM','LOAD_DTM','CENTER_CD']
for ym in YM_DBJ:
    rows = [[ym+'15','12','BUSAN','GU','DONG', cd+'000001', 129.036128340, 35.102156972,
             'BC','4010','CVS', random.choice([1955,1975,1995]), random.choice(['M','F']),
             random.randint(1,9), random.randint(5000,90000), '20230101000000','ZZZZZZ']
            for cd in ADM8[:60]]
    w('SPN060', 'SPN060_'+ym+'.csv', H60, rows, ',')

# ---------- SPN058 전통시장
H58 = ['STRD_DATE','STRD_TIME','MART_NM','MART_ADDR','CARD_CO_NM','BUSIN_CD','BUSIN_NM',
       'BIRTH_YEAR','GENDER','TRANS_CNT','TRANS_SUM','LOAD_DTM','CENTER_CD']
for ym in YM_DBJ:
    rows = [[ym+'15','12','MKT'+str(i),'BUSAN','BC','4010','CVS', 1960,
             'M', random.randint(1,50), random.randint(10000,500000),'20230101000000','ZZZZZZ']
            for i in range(30)]
    w('SPN058', 'SPN058_'+ym+'.csv', H58, rows, '|')

# ---------- CRD022 기업정보 (202501~ 만. 생존편향 함정)
H22 = ['CRTR_YM','ENT_CD','IDCD','BRNO','CRNO','CP_CD','ENP_SZE','STRTUP_YMD',
       'ESTBL_YMD','JOIN_CNT','ENP_NM','INDST_CD_ID']
for ym in ['202501','202502','202503']:
    rows = [[ym,'E'+str(i).zfill(6),'I'+str(i).zfill(6), str(600000000+i).zfill(10),
             '1'*13, random.choice(['1','9','9','9']), random.choice(['2','3']),
             '20150101','20150101', random.randint(1,30),'CORP','C10']
            for i in range(400)]           # <<< 0~399 만. CRD025 는 0~599 -> 200명 결손
    w('CRD022', 'CRD022_'+ym+'.csv', H22, rows, '|')

# ---------- CRD023 사업장 (폐업일자는 코드 '2' 에만 채움 = 휴업/폐업 분리 함정)
H23 = ['CRTR_YM','ENT_CD','IDCD','BZPLC_SE_CD','BZPL_NM','KOR_BZPLC_ADDR','LOT','LAT',
       'TP_BIZ_NM','BZSTAT_NM','CLSB_SE_CD','CLSB_YMD']
for ym in ['202501','202502','202503']:
    rows = []
    for i in range(400):
        c = random.choice(['1','1','1','2','3'])
        xy = ('', '') if random.random() < 0.30 else (129.0328, 35.1021)
        rows.append([ym,'E'+str(i).zfill(6),'I'+str(i).zfill(6),'01','SHOP','BUSAN',
                     xy[0], xy[1],'RETAIL','SALES', c, '20250115' if c == '2' else ''])
    w('CRD023', 'CRD023_'+ym+'.csv', H23, rows, '|')

# ---------- CRD024 재무
H24 = ['CRTR_YM','ENT_CD','IDCD','ACCT_DT','RPT_CD','ARTCL_CD_SLS','AMT_THW','CPST_RT','ICDC_RT']
for ym in YM_KCD:
    rows = [[ym,'E'+str(i).zfill(6),'I'+str(i).zfill(6),'20231231','01','1000',
             random.randint(10000,900000), 100.0, round(random.uniform(-30,30),1)] for i in range(200)]
    w('CRD024', 'CRD024_'+ym+'.csv', H24, rows, '|')

# ---------- CRD025 매출매입 (DLR_BRNO 거래처 · PT1 가액비중)
H25 = ['CRTR_YM','BRNO','VAT_STRT_YMD','VAT_END_YMD','DATA_SE_SLS_PRCHS_CD','DLR_BRNO','PT1','PT2']
for ym in YM_KCD:
    rows = []
    for i in range(600):
        for k in range(random.randint(1, 4)):
            rows.append([ym, str(600000000+i).zfill(10), ym+'01', ym+'28',
                         random.choice(['1','2']), str(700000000+random.randint(0,120)).zfill(10),
                         round(random.uniform(0, 100), 2), round(random.uniform(0, 100), 2)])
    w('CRD025', 'CRD025_'+ym+'.csv', H25, rows, '|')

# ---------- CRD026 전입전출
H26 = ['CRTR_YM','BRNO','CRNO','IDCD','SE_GB','BF_ADMNST_CD','AF_ADMNST_CD','BF_SIDO_NM',
       'BF_SIGUN_NM','BF_ADMI_NM','CTPV_NM','SIGUN_NM','FRCS_LCTN_STDG','INDST_SE_LCLS_CD',
       'INDST_SE_LCLS_NM','INDST_SE_MCLS_CD','INDST_SE_MCLS_NM','ENP_SZE']
for ym in YM_KCD:
    rows = [[ym, str(600000000+random.randint(0,599)).zfill(10),'1'*13,'I'+str(i).zfill(6),
             random.choice(['0','1','2']), ADM10[0], ADM10[1],'BUSAN','GU','DONG',
             'BUSAN','GU','DONG','A','AA','A01','AAA','2'] for i in range(40)]
    w('CRD026', 'CRD026_'+ym+'.csv', H26, rows, '|')

# ---------- CRD020 소득 / CRD021 대출 / SPN092  (ADMNST_CD 8자리)
for ym in YM_KCD:
    rows = [[ym,'ADM','26','BUSAN', cd[:5],'GU', cd,'DONG','M','40','1','0','5',
             1000,2000, random.randint(100,900)] for cd in ADM8]
    w('CRD020','CRD020_'+ym+'.csv',
      ['CRTR_YM','SE_NM','CTPV_CD','CTPV_NM','SGG_CD','SGG_NM','ADMNST_CD','ADMNST_DONG_NM',
       'GNDR','AGE_CD','JOB_CD','LN_CD','INC_10PERC','INC_MIN','INC_MAX','CNT_POP'], rows, '|')
    rows = [[ym,'ADM','26','BUSAN', cd[:5],'GU', cd,'DONG','M','40','1','0','5',
             random.randint(1,9), random.randint(100,9000), random.randint(10,900)] for cd in ADM8]
    w('CRD021','CRD021_'+ym+'.csv',
      ['CRTR_YM','SE_NM','CTPV_CD','CTPV_NM','SGG_CD','SGG_NM','ADMNST_CD','ADMNST_DONG_NM',
       'GNDR','AGE_CD','JOB_CD','LN_CD','LN_10PERC','CNT_LN','DONG_PPLTN_CNT','CNT_POP_LN_EFF'], rows, '|')
    rows = [[ym,'ADM','26','BUSAN', cd[:5],'GU', cd,'DONG','M','40','1','5',
             random.randint(100,9000), random.randint(1,90), random.randint(1,90), random.randint(1,90)] for cd in ADM8[:60]]
    w('SPN092','SPN092_'+ym+'.csv',
      ['CRTR_YM','SE_NM','CTPV_CD','CTPV_NM','SGG_CD','SGG_NM','ADMNST_CD','ADMNST_DONG_NM',
       'GNDR','AGE_CD','JOB_CD','CD_10PERC','DONG_PPLTN_CNT','CNT_CD_OWN_SIN','CNT_CD_OWN_CHK','CNT_CD_OWN'], rows, '|')

# ---------- POP019 (ADMNST_INST_CD 행정기관코드 10자리 · AGE_GRP · HAB_PPLTN)
H019 = ['CRTR_YMD','ADMNST_INST_CD','GNDR','AGE_GRP','HAB_PPLTN','WRC_PPLTN','VST_PPLTN']
for ym in YM_KCD:
    rows = [[ym+'01', cd, random.choice(['M','F']), a,
             round(random.uniform(50, 5000), 2), round(random.uniform(10, 900), 2),
             round(random.uniform(10, 900), 2)]
            for cd in ADM10 for a in ['20대','40대','60대','70대이상']]
    w('POP019', 'POP019_'+ym+'.csv', H019, rows, '|')

# ---------- POP022
for ym in YM_KCD:
    rows = [[ym+'01', cd, str(h).zfill(2), round(random.uniform(50,5000),2),
             round(random.uniform(10,900),2), round(random.uniform(10,900),2)]
            for cd in ADM10[:60] for h in [9, 18]]
    w('POP022','POP022_'+ym+'.csv',
      ['CRTR_YMD','ADMNST_CD','TME','HAB_PPLTN','WRC_PPLTN','VST_PPLTN'], rows, '|')

# ---------- SPN082 창폐업 (ADMNST_CD 10자리)
H82 = ['CRTR_YM','ADMNST_CD','INDST_SE_LCLS_CD','INDST_SE_MCLS_CD','INDST_SE_SCLS_CD',
       'BZMN_SE','USE_AMT','USE_CNT','NEW_SHOP_CNT','OPRTNG_SHOP_CNT','CLSB_SHOP_CNT']
for ym in YM_KCD:
    rows = [[ym, cd,'A','A01','A0101', random.choice(['개인','법인']),
             random.randint(1000000,90000000), random.randint(10,900), random.randint(0,9),
             random.randint(10,300), random.randint(0,12)] for cd in ADM10]
    w('SPN082','SPN082_'+ym+'.csv', H82, rows, '|')

# ---------- SPN020 / SPN093 / SPN094 업종코드
w('SPN020','SPN020_202201.csv',
  ['INDST_SE_LCLS_CD','INDST_SE_LCLS_NM','INDST_SE_MCLS_CD','INDST_SE_MCLS_NM',
   'INDST_SE_SCLS_CD','INDST_SE_SCLS_NM','CRTR_YM','LOAD_YMD'],
  [[str(i).zfill(2),'L'+str(i), str(i).zfill(2),'M'+str(i), str(i).zfill(4),'S'+str(i),
    '202201','20220101'] for i in range(20)], '|')
w('SPN093','SPN093_2025.csv',
  ['INDST_SE_LCLS_CD','INDST_SE_LCLS_NM','INDST_SE_MCLS_CD','INDST_SE_MCLS_NM',
   'INDST_SE_SCLS_CD','INDST_SE_SCLS_NM'],
  [[str(i).zfill(4),'L'+str(i), str(i).zfill(4),'M'+str(i), str(i).zfill(6),'S'+str(i)] for i in range(20)], ',')
w('SPN094','SPN094_2025.csv',
  ['INDST_SE_LCLS_CD','INDST_SE_LCLS_NM','INDST_SE_MCLS_CD','INDST_SE_MCLS_NM'],
  [[LCLS[i%4],'KCD_L'+str(i), MCLS[i%4],'KCD_M'+str(i)] for i in range(8)], ',')

# ---------- TOU007 (YYYYMM_BASE · ADM_CD 8자리 · EMP_NUM_CLASS · BUSINESS_NUM)
H007 = ['YYYYMM_BASE','ADM_CD','AREA_CD','IND_CLASS_CD','IND_CLASS_NM','EMP_NUM_CLASS',
        'REVENUE_CLASS','BUSINESS_NUM','LOAD_DTM','CENT_CD']
for y in ['202112','202212','202312']:
    rows = [[y, cd, cd+'000001','C10','RETAIL', e,'1억미만',
             random.randint(1, 120),'20240101','ZZ']
            for cd in ADM8 for e in ['1-4인','5-9인','10인이상']]
    w('TOU007','TOU007_'+y+'.csv', H007, rows, '|')

# ---------- SPN057 (8자리 <-> 10자리 매핑 허브)
w('SPN057','SPN057_202307.csv',
  ['CTPV','SGG','ADMNST_NM','ADMNST_INST_NM','ADMNST_CD','ADMNST_INST_CD10',
   'ADMNST_INST_CD8','CRTR_YM','LOAD_YMD'],
  [['부산','구','동','주민센터', ADM8[i], ADM10[i], ADM8[i],'202307','20230701']
   for i in range(205)], ',')

# ---------- POP001 / POP014 / REL015
w('POP001','POP001_2021.csv',
  ['TOT_ZONE_CD','ROAD_NM_ADDR','LOTNO_ADDR','TOT_ZONE_CENT_LOT','TOT_ZONE_CENT_LAT','CRTR_YR','LOAD_YMD'],
  [[cd+'000001','ROAD','LOT',129.0,35.1,'2021','20210101'] for cd in ADM8], ',')
for y in ['2022','2023']:
    w('POP001','POP001_'+y+'.csv',
      ['TOT_ZONE_CD','ROAD_NM_ADDR','LOTNO_ADDR','TOT_ZONE_CENT_LOT','TOT_ZONE_CENT_LAT','CRTR_YR','LOAD_YMD'],
      [[cd+'000001','ROAD','LOT',129.0,35.1,y,y+'0101'] for cd in ADM8], ',')
H014 = ['STRD_YYMM','CTPR_CD_VAL','CCG_VAL','TOWN_VAL','TZ_AREA_VAL','CTPR_NM','CCG_NM',
        'TOWN_NM','TZ_AREA_NM','AGGR_DV_VAL','SEX_CTGO_VAL','PUL_NUM','LOAD_DTM','CENT_CD']
for ym in ['202108','202208','202308']:
    w('POP014','POP014_'+ym+'.csv', H014,
      [[ym,'26', cd[:5], cd, cd+'000001','부산','구','동','집계구','60대','M',
        random.randint(50,5000),'20240101','ZZ'] for cd in ADM8], ',')
H015 = ['YYYYMM_BASE','ADDR_ADR','ADDR_ADM','ADM_CD','AREA_CD','RENT_DEPOSIT','RENT_MONTHLY',
        'CONTRACT_BLD_AREA','RENT_TYPE','STRUCTURE','LOAD_DTM','CENT_CD']
for ym in ['202107','202207','202307']:
    w('REL015','REL015_'+ym+'.csv', H015,
      [[ym,'법정동주소','행정동주소', cd, cd+'000001', random.randint(1000,90000),
        random.randint(20,300), random.randint(20,120),'월세','아파트','20240101','ZZ'] for cd in ADM8], ',')

# ---------- 함정 A : SPN092 는 마지막 파일에서만 헤더 없음 (fs[:3] 로는 못 잡음)
p = ROOT + "/SPN092"
fn = sorted(os.listdir(p))[-1]
t = io.open(p+"/"+fn, encoding="utf-8").read().split("\n")
io.open(p+"/"+fn, "w", encoding="utf-8", newline="").write("\n".join(t[1:]))
print("trapA: header removed from", fn)

# ---------- REL020 SHP (A1 = 법정동코드. SPN090 과 같은 체계여야 판정이 맞음)
import geopandas as gpd
from shapely.geometry import Point
os.makedirs(ROOT + "/REL020")
gdf = gpd.GeoDataFrame({'A1': BJD10, 'A2': ['NM'+c[-3:] for c in BJD10],
                        'A9': [random.randint(100000, 9000000) for _ in BJD10]},
                       geometry=[Point(129.0+i*0.001, 35.1+i*0.001) for i in range(len(BJD10))],
                       crs="EPSG:5186")
gdf.to_file(ROOT + "/REL020/AL_D150_26_20240125.shp", encoding="utf-8")

n = sum(len(os.listdir(ROOT+"/"+d)) for d in sorted(os.listdir(ROOT)))
io.open("mock2_report.txt","w",encoding="utf-8").write(
    "ROOT "+ROOT+"\nfolders "+str(len(os.listdir(ROOT)))+"\nfiles "+str(n)+
    "\n함정: SPN090=법정동 / SPN059.ADM_CD=8자리 / SPN059 202212 기준일자공란 /"
    " SPN089 TAX 25%공란 / CRD022 200명결손 / CLSB_YMD는 코드2만 / SPN092 헤더1개\n")
print("mock2 done")
