#!/usr/bin/env python

__author__ = 'Khamdihi Dev'
__github__ = 'https://github.com/khamdihi-dev'


import random
from faker import Faker

fake = Faker()

class useragent:

    def __init__(self):pass

    def android(self, developer=None, app_version=None, version_code=None, android_name=None, language=None):
        if not app_version: return {'status': 'fail','message': 'read documentation'}
        if not version_code: return {'status': 'fail','message': 'read documentation'}
        if developer != __author__:
            return {'status': 'fail','message': 'read documentation'}

        self.androidlist = random.choice(['24/7.0','26/8.0.0','23/6.0.1','22/5.1.1','21/5.0.1','21/5.0.2','25/7.1.1','19/4.4.4','21/5.0','19/4.4.2','27/8.1.0','28/9','29/10','26/9','29/10','30/11','25/7.1.2'])
        self.androiddpis = random.choice(['320dpi','640dpi','213dpi','480dpi','420dpi','240dpi','280dpi','160dpi','560dpi','540dpi','272dpi','360dpi','720dpi','270dpi','450dpi','600dpi','279dpi','210dpi','180dpi','510dpi','300dpi','454dpi','314dpi','288dpi','401dpi','153dpi','267dpi','345dpi','493dpi','340dpi','604dpi','465dpi','680dpi','256dpi','290dpi','432dpi','273dpi','120dpi','200dpi','367dpi','419dpi','306dpi','303dpi','411dpi','195dpi','518dpi','230dpi','384dpi','315dpi','293dpi','274dpi','235dpi'])
        self.androidpxls = random.choice(['720x1280','1440x2560','1440x2768','1280x720','1280x800','1080x1920','540x960','1080x2076','1080x2094','1080x2220','480x800','768x1024','1440x2792','1200x1920','720x1384','1920x1080','720x1369','800x1280','720x1440','1080x2058','600x1024','720x1396','2792x1440','1920x1200','2560x1440','1536x2048','720x1382','1080x2113','1080x2198','1080x2131','720x1423','1080x2069','720x1481','1080x2047','1080x2110','1080x2181','1080x2209','1080x2180','1080x2020','1080x2095','1440x2723','1080x2175','720x1365','1440x2699','1080x2218','2699x1440','1440x2907','1080x2257','720x1370','1080x2042','720x1372','1080x2200','1080x2186','720x1361','1080x2024','1080x2006','720x1402','1440x2831','720x1454','1080x2064','1440x2933','720x1411','720x1450','1440x2730','1080x2046','2094x1080','540x888','1440x2759','1080x2274','1080x2178','1440x2706','720x1356','720x1466','1440x2900','2560x1600','1080x2038','1600x2452','1080x2129','720x1422','720x1381','1080x2183','1080x2285','800x1216','1080x2216','1080x2168','1080x2119','1080x2128','1080x2273','2274x1080','1080x2162','1080x2164','2076x1080','1024x768','1080x2173','1440x2845','1080x2134','720x1379','1440x2838','1080x2139','2131x1080','1440x2744','1080x2192','720x1406','1440x2960','1080x2029','2042x1080','1080x2212','1406x720','1080x2288','2047x1080','1080x2051','720x1398','1280x736','1382x720','720x1353','1080x2050','1080x2028','1080x2256','2711x1440','2175x1080','1080x2281','2560x1492','1440x2923','1200x1845','1080x2189','1080x2002','1440x2711','2110x1080','960x540','1080x2033','2200x1080','720x1452','720x1480','1440x2735','720x1472','1080x2277','1080x2169','2874x1440','1600x2560','1080x2151','2218x1080','1080x2182','720x1468','1440x2898','1080x2011','1080x2201','720x1380','1080x2287','2069x1080','1200x1836','2046x1080','720x1439','2058x1080','2182x1080','720x1399','1080x2282','1440x2721','1080x2324','720x1432','1080x2165','1080x2150','1080x2156','1080x1872','1440x3048','1532x2560','720x1355','720x1390','720x1476','720x1410','1080x2032','720x1437','1440x2682','1440x2921','1080x2270','1080x2160','720x1446','1200x1848','1440x2874','1080x2309','1080x2174','1440x2867','1080x2060','1080x2196','1080x2401','1536x1922','1080x2280','1080x2123','720x1435','1440x2927','1080x2276','720x1448','720x1469','720x1344','1080x2187','540x937','1440x3028','1080x2184','1440x2718','1080x2326','840x1834','1440x2935','1440x2880','1440x2892','2048x2048','1080x2195','1080x2322','720x1419','987x1450','1080x2092','1440x3047','720x1358','1080x2136','720x1357','1080x2093','720x1477','1080x2312','1080x2361','720x1341','720x1507','1080x2172','720x1337','1080x2177','1080x2125','1440x2891','1600x2434','720x1394','1080x2159','720x1387','1080x2166','1080x2154','1080x2147','1440x2747','1080x2105','1440x2911','720x1473','1080x2055','1080x2265','720x1436','1080x2190','1600x2526','720x1373','720x1415','1080x2249','1080x2254','720x1455','1440x3040','1080x2149','720x1385','1440x3036','1080x2111','1440x2904','720x1442','720x1377','1080x2307','1080x2327','1080x2141','1080x2025','720x1430','720x1375','1080x2283','1440x2779','1080x2321','1080x2268','1440x2758','1752x2698','1080x2267','1200x1856','1440x2756','720x1464','1080x2234','1080x2171','1080x2155','720x1463','1080x2122','720x1467','1080x2264','720x1349','1440x2999','720x1458','1080x2015','720x1431','1242x2208','1080x2185','1080x2148','1080x2163','1440x2780','720x1445','1080x2146','1200x1916','720x1502','1200x1928','720x1506','720x1424','720x1465','720x1420','1080x2176','720x1521','1080x2315','1080x2400','720x1471','1080x2157','1600x2458','1080x2067','1080x2191','1080x2271','720x1407','800x1208','1080x2087','1080x2199','578x1028','720x1485','540x879','1080x2179','720x1555','810x1598','720x1378','1200x1897','720x1395','720x1459','900x1600','1080x2275','1440x2733'])

        self.devlava = f'Instagram {app_version} Android ({self.androidlist}; {self.androiddpis}; {self.androidpxls}; LAVA; Z60s; Z60s; mt6739; {language}; {version_code})'
        self.devtcl = f'Instagram {app_version} Android ({self.androidlist}; {self.androiddpis}; {self.androidpxls}; TCL; 5087Z; Doha_TMO; mt6762; {language}; {version_code})'
        self.devrealme = f'Instagram {app_version} Android ({self.androidlist}; {self.androiddpis}; {self.androidpxls}; realme; RMX3782; RE5C6CL1; mt6835; {language}; {version_code})'
        self.devmediacom = f'Instagram {app_version} Android ({self.androidlist}; {self.androiddpis}; {self.androidpxls}; mediacom; 1AEC; 1AEC; mt6735; {language}; {version_code})'        
        self.devamazon = f'Instagram {app_version} Android ({self.androidlist}; {self.androiddpis}; {self.androidpxls}; Amazon; KFGIWI; giza; mt8163; {language}; {version_code})'
        self.devtabet  = f'Instagram {app_version} Android ({self.androidlist}; {self.androiddpis}; {self.androidpxls}; Amazon; KFRAWI; raspite; mt8169; {language}; {version_code})'
        self.devgoogle = f'Instagram {app_version} Android ({self.androidlist}; {self.androiddpis}; {self.androidpxls}; Google/google; Pixel 7 Pro; cheetah; cheetah; {language}; {version_code})'
        self.devxiomai = f'Instagram {app_version} Android ({self.androidlist}; {self.androiddpis}; {self.androidpxls}; Xiaomi; M2007J3SG; apollo; qcom; {language}; {version_code})'
        self.alldevice = random.choice([
            self.devlava, self.devtcl, self.devrealme, self.devmediacom, self.devamazon, self.devtabet, self.devgoogle, self.devxiomai
        ])
        if android_name == 'all':return {'status':'ok','message': True,'useragent': self.alldevice}
        elif android_name == 'xiomai':return {'status':'ok','message': True,'useragent': self.devxiomai}
        elif android_name == 'google':return {'status':'ok','message': True,'useragent': self.devgoogle}
        elif android_name == 'tablet':return {'status':'ok','message': True,'useragent': self.devtabet}
        elif android_name == 'amazon':return {'status':'ok','message': True,'useragent': self.devamazon}
        elif android_name == 'mediacom':return {'status':'ok','message': True,'useragent': self.devmediacom}
        elif android_name == 'realme':return {'status':'ok','message': True,'useragent': self.devrealme}
        elif android_name == 'tcl':return {'status':'ok','message': True,'useragent': self.devtcl}
        elif android_name == 'lava':return {'status':'ok','message': True,'useragent': self.devlava}
        else:return {'status': 'fail','message': f'andorid {android_name} not foud!'}
        
    def ios(self, developer=None, app_version=None, version_code=None, ios=None, language=None):
        self.devices = random.choice([
            "iPhone12,3",  # iPhone 11 Pro
            "iPhone12,5",  # iPhone 11 Pro Max
            "iPhone13,1",  # iPhone 12 Mini
            "iPhone13,2",  # iPhone 12
            "iPhone13,3",  # iPhone 12 Pro
            "iPhone13,4",  # iPhone 12 Pro Max
            "iPhone14,4",  # iPhone 13 Mini
            "iPhone12,1",  # iPhone 11
            "iPhone14,5",  # iPhone 13
            "iPhone14,2",  # iPhone 13 Pro
            "iPhone14,3",  # iPhone 13 Pro Max
            "iPhone15,2",  # iPhone 14
            "iPhone15,3",  # iPhone 14 Plus
            "iPhone15,4",  # iPhone 14 Pro
            "iPhone15,5",  # iPhone 14 Pro Max
            "iPhone10,3",  # iPhone X
            "iPhone10,6",  # iPhone X
            "iPhone11,2",  # iPhone XS
            "iPhone11,4",  # iPhone XS Max
            "iPhone11,8",  # iPhone XR
            "iPhone11,6",  # iPhone 11 Pro Max
            "iPhone12,8",  # iPhone SE (2nd generation)
            "iPhone13,3",  # iPhone 12 Pro
            "iPhone14,1",  # iPhone 13
            "iPhone14,2",  # iPhone 13 Pro
            "iPhone14,3",  # iPhone 13 Pro Max
            "iPad8,1",     # iPad Pro 11
            "iPad8,2",     # iPad Pro 11
            "iPad8,3",     # iPad Pro 11
            "iPad8,4",     # iPad Pro 11
            "iPad9,1",     # iPad (9th generation)
            "iPad9,2",     # iPad (9th generation)
            "iPad9,3",     # iPad (9th generation)
            "iPad9,4",     # iPad (9th generation)
            "iPadPro12,9"  # iPad Pro 12.9
        ])
        if developer != __author__:
            return {'message': 'Bukan Developers', 'useragent': None}
        if not app_version:
            return {'message': 'Berikan saya app_version','useragent':None}
        if not language:
            return {'message': 'Berikan saya language devices','useragent':None}

        self.ios_version = random.choice(["17_5_1", "17_5_0", "17_4_2", "17_4_1","16_6_1", "16_6_0", "16_5_2", "16_5_1","16_5_0", "16_4_1", "15_7_1", "15_6_1","15_5_2", "15_4_0", "14_8_1", "14_7_1","14_6_0", "14_5_0", "14_4_2"])
        self.scale = random.choice([2.75, 3.00, 3.50, 2.90, 3.20,2.80, 3.10, 2.60, 3.30, 2.40])
        self.resolution = random.choice(["1290x2796", "1125x2436", "828x1792","750x1334", "640x1136", "2048x2732","2048x1536", "2560x1600", "3200x1800","1440x2560", "1080x1920", "750x1334","1242x2688", "640x960", "1536x2048"])
        return {'message': True,'useragent':f'Instagram {app_version} ({self.devices}; iOS {self.ios_version}; {language}; {language.replace("_","-")}; scale={self.scale}; gamut=normal; {self.resolution})'}

# print(useragent().ios(developer=__author__,app_version='37.0.0.9.96',version_code='',ios='',language='in_ID'))