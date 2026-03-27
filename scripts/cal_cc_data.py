import re
import statistics

def parse_time_to_ms(value_str, unit_str):
    value = float(value_str)
    if unit_str == 'ms': return value
    elif unit_str in ['µs', 'us']: return value / 1000.0
    elif unit_str == 's': return value * 1000.0
    return value

def parse_and_analyze(log_content):
    lines = log_content.strip().split('\n')
    
    re_cc = re.compile(r"\[STATS\] Function: (DefId\(.*?\)) \| CC: (\d+)")
    re_time = re.compile(r"Total Time of (DefId\(.*?\)):\s+([\d\.]+)(ms|µs|us|s)")
    re_splice = re.compile(r"(DefId\(.*?\)) contains SCC \d+ stopped after (\d+) splicing iterations in depth (\d+)")

    data_points = []
    current = {}
    state = 0 # 0=CC, 1=Time, 2=Splice
    
    for line in lines:
        line = line.strip()
        if not line: continue

        match_cc = re_cc.search(line)
        if match_cc:
            current = {'func': match_cc.group(1), 'cc': int(match_cc.group(2))}
            state = 1
            continue
            
        if state == 1:
            match_time = re_time.search(line)
            if match_time and match_time.group(1) == current['func']:
                current['time'] = parse_time_to_ms(match_time.group(2), match_time.group(3))
                state = 2
                continue
            else:
                state = 0
                
        if state == 2:
            match_splice = re_splice.search(line)
            if match_splice and match_splice.group(1) == current['func']:
                current['splicing'] = int(match_splice.group(2))
                current['depth'] = int(match_splice.group(3))
                data_points.append(current)
                state = 0
                current = {}
            else:
                state = 0

    print_stats("By CC Range", aggregate_by_cc(data_points))
    print("\n" + "="*80 + "\n")
    print_stats("By Loop Depth (from log)", aggregate_by_depth(data_points))

def aggregate_by_cc(data):
    buckets = {
        '<= 3':  [],
        '4':     [],
        '5':     [],
        '6-8':   [],
        '> 8':   []
    }
    for d in data:
        cc = d['cc']
        if cc <= 3: k = '<= 3'
        elif cc == 4: k = '4'
        elif cc == 5: k = '5'
        elif 6 <= cc <= 8: k = '6-8'
        else: k = '> 8'
        buckets[k].append(d)
    return buckets

def aggregate_by_depth(data):
    buckets = {}
    for d in data:
        depth = d.get('depth', 0)
        k = str(depth)
        if k not in buckets: buckets[k] = []
        buckets[k].append(d)
    
    sorted_keys = sorted(buckets.keys(), key=lambda x: int(x))
    return {k: buckets[k] for k in sorted_keys}

def print_stats(title, buckets):
    print(f"--- {title} ---")
    print(f"{'Range':<10} | {'Avg Time':<10} | {'Med Time':<10} | {'Avg Splice':<10} | {'Count':<5}")
    print("-" * 60)
    
    for k, items in buckets.items():
        if not items:
            continue
        
        times = [d['time'] for d in items]
        splices = [d['splicing'] for d in items]
        
        avg_time = statistics.mean(times)
        med_time = statistics.median(times)
        avg_splice = statistics.mean(splices)
        
        print(f"{k:<10} | {avg_time:<10.4f} | {med_time:<10.4f} | {avg_splice:<10.2f} | {len(items):<5}")

# parse_and_analyze(raw_log)
# ==========================================
raw_log = """
12:52:59|-|: [STATS] Function: DefId(0:3 ~ test5[dd47]::random) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:4 ~ test5[dd47]::scc_topo_case_1) | CC: 5 | Nodes: 17 | Edges: 20
12:52:59|-|: Total Time of DefId(0:4 ~ test5[dd47]::scc_topo_case_1):        1.89ms
12:52:59|-|: DefId(0:4 ~ test5[dd47]::scc_topo_case_1) contains SCC 1 stopped after 4 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:6 ~ test5[dd47]::scc_topo_case_2) | CC: 3 | Nodes: 6 | Edges: 7
12:52:59|-|: Total Time of DefId(0:6 ~ test5[dd47]::scc_topo_case_2):        134.04µs
12:52:59|-|: DefId(0:6 ~ test5[dd47]::scc_topo_case_2) contains SCC 1 stopped after 3 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:8 ~ test5[dd47]::scc_topo_case_3) | CC: 6 | Nodes: 21 | Edges: 25
12:52:59|-|: Total Time of DefId(0:8 ~ test5[dd47]::scc_topo_case_3):        1.06ms
12:52:59|-|: DefId(0:8 ~ test5[dd47]::scc_topo_case_3) contains SCC 2 stopped after 4 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:10 ~ test5[dd47]::scc_topo_case_4) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:10 ~ test5[dd47]::scc_topo_case_4):        105.88µs
12:52:59|-|: DefId(0:10 ~ test5[dd47]::scc_topo_case_4) contains SCC 4 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:12 ~ test5[dd47]::scc_topo_case_5) | CC: 3 | Nodes: 6 | Edges: 7
12:52:59|-|: Total Time of DefId(0:12 ~ test5[dd47]::scc_topo_case_5):        39.79µs
12:52:59|-|: DefId(0:12 ~ test5[dd47]::scc_topo_case_5) contains SCC 1 stopped after 5 splicing iterations in depth 2.
12:52:59|-|: [STATS] Function: DefId(0:14 ~ test5[dd47]::scc_topo_case_6) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:14 ~ test5[dd47]::scc_topo_case_6):        119.71µs
12:52:59|-|: DefId(0:14 ~ test5[dd47]::scc_topo_case_6) contains SCC 4 stopped after 5 splicing iterations in depth 2.
12:52:59|-|: [STATS] Function: DefId(0:16 ~ test5[dd47]::scc_topo_case_7) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:16 ~ test5[dd47]::scc_topo_case_7):        102.04µs
12:52:59|-|: DefId(0:16 ~ test5[dd47]::scc_topo_case_7) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:18 ~ test5[dd47]::scc_topo_case_8) | CC: 5 | Nodes: 17 | Edges: 20
12:52:59|-|: Total Time of DefId(0:18 ~ test5[dd47]::scc_topo_case_8):        5.21ms
12:52:59|-|: DefId(0:18 ~ test5[dd47]::scc_topo_case_8) contains SCC 1 stopped after 5 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:20 ~ test5[dd47]::scc_topo_case_9) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:20 ~ test5[dd47]::scc_topo_case_9):        191.92µs
12:52:59|-|: DefId(0:20 ~ test5[dd47]::scc_topo_case_9) contains SCC 3 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:22 ~ test5[dd47]::scc_topo_case_10) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:22 ~ test5[dd47]::scc_topo_case_10):        86.13µs
12:52:59|-|: DefId(0:22 ~ test5[dd47]::scc_topo_case_10) contains SCC 1 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:24 ~ test5[dd47]::scc_topo_case_11) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:24 ~ test5[dd47]::scc_topo_case_11):        147.33µs
12:52:59|-|: DefId(0:24 ~ test5[dd47]::scc_topo_case_11) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:26 ~ test5[dd47]::scc_topo_case_12) | CC: 5 | Nodes: 15 | Edges: 18
12:52:59|-|: Total Time of DefId(0:26 ~ test5[dd47]::scc_topo_case_12):        146.88µs
12:52:59|-|: DefId(0:26 ~ test5[dd47]::scc_topo_case_12) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:28 ~ test5[dd47]::scc_topo_case_13) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:28 ~ test5[dd47]::scc_topo_case_13):        92.79µs
12:52:59|-|: DefId(0:28 ~ test5[dd47]::scc_topo_case_13) contains SCC 1 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:30 ~ test5[dd47]::scc_topo_case_14) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:30 ~ test5[dd47]::scc_topo_case_14):        87.83µs
12:52:59|-|: DefId(0:30 ~ test5[dd47]::scc_topo_case_14) contains SCC 1 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:32 ~ test5[dd47]::scc_topo_case_15) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:32 ~ test5[dd47]::scc_topo_case_15):        159.79µs
12:52:59|-|: DefId(0:32 ~ test5[dd47]::scc_topo_case_15) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:34 ~ test5[dd47]::scc_topo_case_16) | CC: 2 | Nodes: 5 | Edges: 5
12:52:59|-|: [STATS] Function: DefId(0:36 ~ test5[dd47]::scc_topo_case_17) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:36 ~ test5[dd47]::scc_topo_case_17):        104.17µs
12:52:59|-|: DefId(0:36 ~ test5[dd47]::scc_topo_case_17) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:38 ~ test5[dd47]::scc_topo_case_18) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:38 ~ test5[dd47]::scc_topo_case_18):        124.00µs
12:52:59|-|: DefId(0:38 ~ test5[dd47]::scc_topo_case_18) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:40 ~ test5[dd47]::scc_topo_case_19) | CC: 5 | Nodes: 17 | Edges: 20
12:52:59|-|: Total Time of DefId(0:40 ~ test5[dd47]::scc_topo_case_19):        144.21µs
12:52:59|-|: DefId(0:40 ~ test5[dd47]::scc_topo_case_19) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:42 ~ test5[dd47]::scc_topo_case_20) | CC: 5 | Nodes: 17 | Edges: 20
12:52:59|-|: Total Time of DefId(0:42 ~ test5[dd47]::scc_topo_case_20):        99.75µs
12:52:59|-|: DefId(0:42 ~ test5[dd47]::scc_topo_case_20) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:44 ~ test5[dd47]::scc_topo_case_21) | CC: 7 | Nodes: 25 | Edges: 30
12:52:59|-|: Total Time of DefId(0:44 ~ test5[dd47]::scc_topo_case_21):        391.21µs
12:52:59|-|: DefId(0:44 ~ test5[dd47]::scc_topo_case_21) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:46 ~ test5[dd47]::scc_topo_case_22) | CC: 4 | Nodes: 12 | Edges: 14
12:52:59|-|: Total Time of DefId(0:46 ~ test5[dd47]::scc_topo_case_22):        93.83µs
12:52:59|-|: DefId(0:46 ~ test5[dd47]::scc_topo_case_22) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:48 ~ test5[dd47]::scc_topo_case_23) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:48 ~ test5[dd47]::scc_topo_case_23):        73.71µs
12:52:59|-|: DefId(0:48 ~ test5[dd47]::scc_topo_case_23) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:50 ~ test5[dd47]::scc_topo_case_24) | CC: 5 | Nodes: 17 | Edges: 20
12:52:59|-|: Total Time of DefId(0:50 ~ test5[dd47]::scc_topo_case_24):        505.33µs
12:52:59|-|: DefId(0:50 ~ test5[dd47]::scc_topo_case_24) contains SCC 9 stopped after 5 splicing iterations in depth 2.
12:52:59|-|: [STATS] Function: DefId(0:52 ~ test5[dd47]::scc_topo_case_25) | CC: 5 | Nodes: 17 | Edges: 20
12:52:59|-|: Total Time of DefId(0:52 ~ test5[dd47]::scc_topo_case_25):        1.28ms
12:52:59|-|: DefId(0:52 ~ test5[dd47]::scc_topo_case_25) contains SCC 1 stopped after 33 splicing iterations in depth 4.
12:52:59|-|: [STATS] Function: DefId(0:54 ~ test5[dd47]::scc_topo_case_26) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:54 ~ test5[dd47]::scc_topo_case_26):        327.83µs
12:52:59|-|: DefId(0:54 ~ test5[dd47]::scc_topo_case_26) contains SCC 1 stopped after 13 splicing iterations in depth 3.
12:52:59|-|: [STATS] Function: DefId(0:56 ~ test5[dd47]::scc_topo_case_27) | CC: 5 | Nodes: 17 | Edges: 20
12:52:59|-|: Total Time of DefId(0:56 ~ test5[dd47]::scc_topo_case_27):        449.88µs
12:52:59|-|: DefId(0:56 ~ test5[dd47]::scc_topo_case_27) contains SCC 1 stopped after 13 splicing iterations in depth 3.
12:52:59|-|: [STATS] Function: DefId(0:58 ~ test5[dd47]::scc_topo_case_28) | CC: 5 | Nodes: 17 | Edges: 20
12:52:59|-|: Total Time of DefId(0:58 ~ test5[dd47]::scc_topo_case_28):        780.29µs
12:52:59|-|: DefId(0:58 ~ test5[dd47]::scc_topo_case_28) contains SCC 1 stopped after 23 splicing iterations in depth 4.
12:52:59|-|: [STATS] Function: DefId(0:60 ~ test5[dd47]::scc_topo_case_29) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:60 ~ test5[dd47]::scc_topo_case_29):        83.38µs
12:52:59|-|: DefId(0:60 ~ test5[dd47]::scc_topo_case_29) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:62 ~ test5[dd47]::scc_topo_case_30) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:62 ~ test5[dd47]::scc_topo_case_30):        339.58µs
12:52:59|-|: DefId(0:62 ~ test5[dd47]::scc_topo_case_30) contains SCC 1 stopped after 14 splicing iterations in depth 4.
12:52:59|-|: [STATS] Function: DefId(0:64 ~ test5[dd47]::random_test1) | CC: 2 | Nodes: 6 | Edges: 5
12:52:59|-|: [STATS] Function: DefId(0:87 ~ test5[dd47]::random_test2) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:189 ~ test5[dd47]::{impl#1}::clone) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:193 ~ test5[dd47]::{impl#4}::eq) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:195 ~ test5[dd47]::{impl#5}::assert_receiver_is_total_eq) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:205 ~ test5[dd47]::{impl#7}::clone) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:209 ~ test5[dd47]::{impl#10}::eq) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:211 ~ test5[dd47]::{impl#11}::assert_receiver_is_total_eq) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:88 ~ test5[dd47]::random_int_test2) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:221 ~ test5[dd47]::{impl#13}::clone) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:225 ~ test5[dd47]::{impl#16}::eq) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:227 ~ test5[dd47]::{impl#17}::assert_receiver_is_total_eq) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:89 ~ test5[dd47]::random_test3) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:90 ~ test5[dd47]::random_bool_test4) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:91 ~ test5[dd47]::test_2) | CC: 2 | Nodes: 5 | Edges: 5
12:52:59|-|: Total Time of DefId(0:91 ~ test5[dd47]::test_2):        32.79µs
12:52:59|-|: DefId(0:91 ~ test5[dd47]::test_2) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:93 ~ test5[dd47]::test_4) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:93 ~ test5[dd47]::test_4):        68.54µs
12:52:59|-|: DefId(0:93 ~ test5[dd47]::test_4) contains SCC 2 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:95 ~ test5[dd47]::test_5) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:95 ~ test5[dd47]::test_5):        91.33µs
12:52:59|-|: DefId(0:95 ~ test5[dd47]::test_5) contains SCC 5 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:97 ~ test5[dd47]::test_9) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:99 ~ test5[dd47]::test_19_max_depth) | CC: 7 | Nodes: 25 | Edges: 30
12:52:59|-|: Total Time of DefId(0:99 ~ test5[dd47]::test_19_max_depth):        347.00µs
12:52:59|-|: DefId(0:99 ~ test5[dd47]::test_19_max_depth) contains SCC 6 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:101 ~ test5[dd47]::case_25_2) | CC: 2 | Nodes: 5 | Edges: 5
12:52:59|-|: Total Time of DefId(0:101 ~ test5[dd47]::case_25_2):        27.58µs
12:52:59|-|: DefId(0:101 ~ test5[dd47]::case_25_2) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:103 ~ test5[dd47]::random_bool) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:104 ~ test5[dd47]::case_1) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:104 ~ test5[dd47]::case_1):        47.92µs
12:52:59|-|: DefId(0:104 ~ test5[dd47]::case_1) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:106 ~ test5[dd47]::case_2) | CC: 4 | Nodes: 12 | Edges: 14
12:52:59|-|: Total Time of DefId(0:106 ~ test5[dd47]::case_2):        86.79µs
12:52:59|-|: DefId(0:106 ~ test5[dd47]::case_2) contains SCC 2 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:108 ~ test5[dd47]::case_3) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:108 ~ test5[dd47]::case_3):        60.21µs
12:52:59|-|: DefId(0:108 ~ test5[dd47]::case_3) contains SCC 1 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:110 ~ test5[dd47]::case_4) | CC: 4 | Nodes: 10 | Edges: 12
12:52:59|-|: Total Time of DefId(0:110 ~ test5[dd47]::case_4):        53.00µs
12:52:59|-|: DefId(0:110 ~ test5[dd47]::case_4) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:112 ~ test5[dd47]::case_5) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:112 ~ test5[dd47]::case_5):        57.38µs
12:52:59|-|: DefId(0:112 ~ test5[dd47]::case_5) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:114 ~ test5[dd47]::case_6) | CC: 3 | Nodes: 6 | Edges: 7
12:52:59|-|: Total Time of DefId(0:114 ~ test5[dd47]::case_6):        21.42µs
12:52:59|-|: DefId(0:114 ~ test5[dd47]::case_6) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:116 ~ test5[dd47]::case_7) | CC: 5 | Nodes: 17 | Edges: 20
12:52:59|-|: Total Time of DefId(0:116 ~ test5[dd47]::case_7):        127.46µs
12:52:59|-|: DefId(0:116 ~ test5[dd47]::case_7) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:118 ~ test5[dd47]::case_8) | CC: 2 | Nodes: 5 | Edges: 5
12:52:59|-|: Total Time of DefId(0:118 ~ test5[dd47]::case_8):        25.67µs
12:52:59|-|: DefId(0:118 ~ test5[dd47]::case_8) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:120 ~ test5[dd47]::case_9) | CC: 6 | Nodes: 21 | Edges: 25
12:52:59|-|: Total Time of DefId(0:120 ~ test5[dd47]::case_9):        310.17µs
12:52:59|-|: DefId(0:120 ~ test5[dd47]::case_9) contains SCC 4 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:122 ~ test5[dd47]::case_10) | CC: 2 | Nodes: 1 | Edges: 0
12:52:59|-|: [STATS] Function: DefId(0:124 ~ test5[dd47]::case_11) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:124 ~ test5[dd47]::case_11):        58.96µs
12:52:59|-|: DefId(0:124 ~ test5[dd47]::case_11) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:126 ~ test5[dd47]::case_12) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:126 ~ test5[dd47]::case_12):        62.83µs
12:52:59|-|: DefId(0:126 ~ test5[dd47]::case_12) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:128 ~ test5[dd47]::case_13) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:128 ~ test5[dd47]::case_13):        34.42µs
12:52:59|-|: DefId(0:128 ~ test5[dd47]::case_13) contains SCC 1 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:130 ~ test5[dd47]::case_14) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:130 ~ test5[dd47]::case_14):        91.42µs
12:52:59|-|: DefId(0:130 ~ test5[dd47]::case_14) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:132 ~ test5[dd47]::case_15) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:132 ~ test5[dd47]::case_15):        67.46µs
12:52:59|-|: DefId(0:132 ~ test5[dd47]::case_15) contains SCC 1 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:134 ~ test5[dd47]::case_16) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:134 ~ test5[dd47]::case_16):        343.67µs
12:52:59|-|: DefId(0:134 ~ test5[dd47]::case_16) contains SCC 1 stopped after 13 splicing iterations in depth 3.
12:52:59|-|: [STATS] Function: DefId(0:136 ~ test5[dd47]::case_17) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:136 ~ test5[dd47]::case_17):        56.42µs
12:52:59|-|: DefId(0:136 ~ test5[dd47]::case_17) contains SCC 1 stopped after 3 splicing iterations in depth 2.
12:52:59|-|: [STATS] Function: DefId(0:138 ~ test5[dd47]::case_18) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:138 ~ test5[dd47]::case_18):        128.46µs
12:52:59|-|: DefId(0:138 ~ test5[dd47]::case_18) contains SCC 1 stopped after 5 splicing iterations in depth 2.
12:52:59|-|: [STATS] Function: DefId(0:140 ~ test5[dd47]::case_19) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:140 ~ test5[dd47]::case_19):        43.33µs
12:52:59|-|: DefId(0:140 ~ test5[dd47]::case_19) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:142 ~ test5[dd47]::case_20) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:142 ~ test5[dd47]::case_20):        234.54µs
12:52:59|-|: DefId(0:142 ~ test5[dd47]::case_20) contains SCC 2 stopped after 5 splicing iterations in depth 2.
12:52:59|-|: [STATS] Function: DefId(0:144 ~ test5[dd47]::case_21) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:144 ~ test5[dd47]::case_21):        37.42µs
12:52:59|-|: DefId(0:144 ~ test5[dd47]::case_21) contains SCC 1 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:146 ~ test5[dd47]::case_22) | CC: 6 | Nodes: 21 | Edges: 25
12:52:59|-|: Total Time of DefId(0:146 ~ test5[dd47]::case_22):        6.00ms
12:52:59|-|: DefId(0:146 ~ test5[dd47]::case_22) contains SCC 1 stopped after 24 splicing iterations in depth 2.
12:52:59|-|: [STATS] Function: DefId(0:148 ~ test5[dd47]::case_23) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:148 ~ test5[dd47]::case_23):        198.67µs
12:52:59|-|: DefId(0:148 ~ test5[dd47]::case_23) contains SCC 1 stopped after 4 splicing iterations in depth 2.
12:52:59|-|: [STATS] Function: DefId(0:150 ~ test5[dd47]::case_24) | CC: 4 | Nodes: 13 | Edges: 15
12:52:59|-|: Total Time of DefId(0:150 ~ test5[dd47]::case_24):        253.88µs
12:52:59|-|: DefId(0:150 ~ test5[dd47]::case_24) contains SCC 1 stopped after 6 splicing iterations in depth 2.
12:52:59|-|: [STATS] Function: DefId(0:152 ~ test5[dd47]::case_26) | CC: 2 | Nodes: 5 | Edges: 5
12:52:59|-|: Total Time of DefId(0:152 ~ test5[dd47]::case_26):        27.42µs
12:52:59|-|: DefId(0:152 ~ test5[dd47]::case_26) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:154 ~ test5[dd47]::case_27) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:154 ~ test5[dd47]::case_27):        51.25µs
12:52:59|-|: DefId(0:154 ~ test5[dd47]::case_27) contains SCC 5 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:156 ~ test5[dd47]::case_28) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:156 ~ test5[dd47]::case_28):        45.38µs
12:52:59|-|: DefId(0:156 ~ test5[dd47]::case_28) contains SCC 1 stopped after 2 splicing iterations in depth 1.
12:52:59|-|: [STATS] Function: DefId(0:158 ~ test5[dd47]::case_29) | CC: 3 | Nodes: 9 | Edges: 10
12:52:59|-|: Total Time of DefId(0:158 ~ test5[dd47]::case_29):        31.42µs
12:52:59|-|: DefId(0:158 ~ test5[dd47]::case_29) contains SCC 1 stopped after 1 splicing iterations in depth 0.
12:52:59|-|: [STATS] Function: DefId(0:160 ~ test5[dd47]::case_30) | CC: 5 | Nodes: 16 | Edges: 19
12:52:59|-|: Total Time of DefId(0:160 ~ test5[dd47]::case_30):        124.54µs
12:52:59|-|: DefId(0:160 ~ test5[dd47]::case_30) contains SCC 2 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:290 ~ test6[80bb]::{impl#1}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:293 ~ test6[80bb]::{impl#3}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:306 ~ test6[80bb]::{impl#6}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:309 ~ test6[80bb]::{impl#8}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:15 ~ test6[80bb]::scc_path_case_1) | CC: 6 | Nodes: 21 | Edges: 25
13:08:14|-|: Total Time of DefId(0:15 ~ test6[80bb]::scc_path_case_1):       1.13ms
13:08:14|-|: DefId(0:15 ~ test6[80bb]::scc_path_case_1) contains SCC 1 stopped after 5 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:17 ~ test6[80bb]::scc_path_case_2) | CC: 5 | Nodes: 14 | Edges: 17
13:08:14|-|: Total Time of DefId(0:17 ~ test6[80bb]::scc_path_case_2):       367.92µs
13:08:14|-|: DefId(0:17 ~ test6[80bb]::scc_path_case_2) contains SCC 1 stopped after 5 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:19 ~ test6[80bb]::scc_path_case_3) | CC: 6 | Nodes: 19 | Edges: 23
13:08:14|-|: Total Time of DefId(0:19 ~ test6[80bb]::scc_path_case_3):       884.29µs
13:08:14|-|: DefId(0:19 ~ test6[80bb]::scc_path_case_3) contains SCC 2 stopped after 4 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:21 ~ test6[80bb]::scc_path_case_4) | CC: 5 | Nodes: 14 | Edges: 17
13:08:14|-|: Total Time of DefId(0:21 ~ test6[80bb]::scc_path_case_4):       150.75µs
13:08:14|-|: DefId(0:21 ~ test6[80bb]::scc_path_case_4) contains SCC 3 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:23 ~ test6[80bb]::scc_path_case_5) | CC: 5 | Nodes: 18 | Edges: 21
13:08:14|-|: Total Time of DefId(0:23 ~ test6[80bb]::scc_path_case_5):       1.07ms
13:08:14|-|: DefId(0:23 ~ test6[80bb]::scc_path_case_5) contains SCC 1 stopped after 7 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:25 ~ test6[80bb]::scc_path_case_6) | CC: 6 | Nodes: 19 | Edges: 23
13:08:14|-|: Total Time of DefId(0:25 ~ test6[80bb]::scc_path_case_6):       510.38µs
13:08:14|-|: DefId(0:25 ~ test6[80bb]::scc_path_case_6) contains SCC 3 stopped after 5 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:27 ~ test6[80bb]::scc_path_case_7) | CC: 4 | Nodes: 11 | Edges: 13
13:08:14|-|: Total Time of DefId(0:27 ~ test6[80bb]::scc_path_case_7):       109.54µs
13:08:14|-|: DefId(0:27 ~ test6[80bb]::scc_path_case_7) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:29 ~ test6[80bb]::scc_path_case_8) | CC: 4 | Nodes: 10 | Edges: 12
13:08:14|-|: Total Time of DefId(0:29 ~ test6[80bb]::scc_path_case_8):       110.75µs
13:08:14|-|: DefId(0:29 ~ test6[80bb]::scc_path_case_8) contains SCC 1 stopped after 4 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:31 ~ test6[80bb]::scc_path_case_9) | CC: 7 | Nodes: 21 | Edges: 26
13:08:14|-|: Total Time of DefId(0:31 ~ test6[80bb]::scc_path_case_9):       754.17µs
13:08:14|-|: DefId(0:31 ~ test6[80bb]::scc_path_case_9) contains SCC 3 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:33 ~ test6[80bb]::scc_path_case_10) | CC: 3 | Nodes: 7 | Edges: 8
13:08:14|-|: [STATS] Function: DefId(0:35 ~ test6[80bb]::scc_path_case_11) | CC: 3 | Nodes: 8 | Edges: 9
13:08:14|-|: Total Time of DefId(0:35 ~ test6[80bb]::scc_path_case_11):       69.54µs
13:08:14|-|: DefId(0:35 ~ test6[80bb]::scc_path_case_11) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:37 ~ test6[80bb]::scc_path_case_12) | CC: 6 | Nodes: 15 | Edges: 19
13:08:14|-|: [STATS] Function: DefId(0:39 ~ test6[80bb]::scc_path_case_13) | CC: 2 | Nodes: 4 | Edges: 4
13:08:14|-|: [STATS] Function: DefId(0:41 ~ test6[80bb]::scc_path_case_14) | CC: 3 | Nodes: 7 | Edges: 8
13:08:14|-|: [STATS] Function: DefId(0:43 ~ test6[80bb]::scc_path_case_15) | CC: 4 | Nodes: 8 | Edges: 10
13:08:14|-|: [STATS] Function: DefId(0:45 ~ test6[80bb]::scc_path_case_16) | CC: 2 | Nodes: 4 | Edges: 4
13:08:14|-|: [STATS] Function: DefId(0:47 ~ test6[80bb]::scc_path_case_17) | CC: 3 | Nodes: 8 | Edges: 9
13:08:14|-|: Total Time of DefId(0:47 ~ test6[80bb]::scc_path_case_17):       86.92µs
13:08:14|-|: DefId(0:47 ~ test6[80bb]::scc_path_case_17) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:49 ~ test6[80bb]::scc_path_case_18) | CC: 3 | Nodes: 6 | Edges: 7
13:08:14|-|: [STATS] Function: DefId(0:51 ~ test6[80bb]::scc_path_case_19) | CC: 3 | Nodes: 7 | Edges: 8
13:08:14|-|: [STATS] Function: DefId(0:53 ~ test6[80bb]::scc_path_case_20) | CC: 3 | Nodes: 7 | Edges: 8
13:08:14|-|: [STATS] Function: DefId(0:55 ~ test6[80bb]::scc_path_case_21) | CC: 4 | Nodes: 10 | Edges: 12
13:08:14|-|: [STATS] Function: DefId(0:57 ~ test6[80bb]::scc_path_case_22) | CC: 2 | Nodes: 4 | Edges: 4
13:08:14|-|: [STATS] Function: DefId(0:59 ~ test6[80bb]::scc_path_case_23) | CC: 2 | Nodes: 4 | Edges: 4
13:08:14|-|: [STATS] Function: DefId(0:61 ~ test6[80bb]::scc_path_case_24) | CC: 4 | Nodes: 10 | Edges: 12
13:08:14|-|: [STATS] Function: DefId(0:63 ~ test6[80bb]::scc_path_case_25) | CC: 5 | Nodes: 7 | Edges: 10
13:08:14|-|: [STATS] Function: DefId(0:65 ~ test6[80bb]::scc_path_case_26) | CC: 3 | Nodes: 7 | Edges: 8
13:08:14|-|: [STATS] Function: DefId(0:67 ~ test6[80bb]::scc_path_case_27) | CC: 4 | Nodes: 10 | Edges: 12
13:08:14|-|: [STATS] Function: DefId(0:69 ~ test6[80bb]::scc_path_case_28) | CC: 4 | Nodes: 10 | Edges: 12
13:08:14|-|: [STATS] Function: DefId(0:71 ~ test6[80bb]::scc_path_case_29) | CC: 4 | Nodes: 10 | Edges: 12
13:08:14|-|: [STATS] Function: DefId(0:73 ~ test6[80bb]::scc_path_case_30) | CC: 4 | Nodes: 6 | Edges: 8
13:08:14|-|: [STATS] Function: DefId(0:75 ~ test6[80bb]::random_test1) | CC: 2 | Nodes: 6 | Edges: 5
13:08:14|-|: [STATS] Function: DefId(0:98 ~ test6[80bb]::random_test2) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:322 ~ test6[80bb]::{impl#11}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:326 ~ test6[80bb]::{impl#14}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:328 ~ test6[80bb]::{impl#15}::assert_receiver_is_total_eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:338 ~ test6[80bb]::{impl#17}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:342 ~ test6[80bb]::{impl#20}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:344 ~ test6[80bb]::{impl#21}::assert_receiver_is_total_eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:99 ~ test6[80bb]::random_int_test2) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:354 ~ test6[80bb]::{impl#23}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:358 ~ test6[80bb]::{impl#26}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:360 ~ test6[80bb]::{impl#27}::assert_receiver_is_total_eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:100 ~ test6[80bb]::random_test3) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:101 ~ test6[80bb]::random_bool_test4) | CC: 2 | Nodes: 1 | Edges: 0
13:08:14|-|: [STATS] Function: DefId(0:102 ~ test6[80bb]::test2) | CC: 5 | Nodes: 11 | Edges: 14
13:08:14|-|: Total Time of DefId(0:102 ~ test6[80bb]::test2):       112.42µs
13:08:14|-|: DefId(0:102 ~ test6[80bb]::test2) contains SCC 1 stopped after 3 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:104 ~ test6[80bb]::test3) | CC: 7 | Nodes: 28 | Edges: 33
13:08:14|-|: Total Time of DefId(0:104 ~ test6[80bb]::test3):       462.17µs
13:08:14|-|: DefId(0:104 ~ test6[80bb]::test3) contains SCC 1 stopped after 3 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:105 ~ test6[80bb]::test_demo) | CC: 7 | Nodes: 21 | Edges: 26
13:08:14|-|: Total Time of DefId(0:105 ~ test6[80bb]::test_demo):       340.88µs
13:08:14|-|: DefId(0:105 ~ test6[80bb]::test_demo) contains SCC 1 stopped after 3 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:106 ~ test6[80bb]::test_nested_scc) | CC: 7 | Nodes: 19 | Edges: 24
13:08:14|-|: Total Time of DefId(0:106 ~ test6[80bb]::test_nested_scc):       311.08µs
13:08:14|-|: DefId(0:106 ~ test6[80bb]::test_nested_scc) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:108 ~ test6[80bb]::test4) | CC: 7 | Nodes: 28 | Edges: 33
13:08:14|-|: Total Time of DefId(0:108 ~ test6[80bb]::test4):       1.58ms
13:08:14|-|: DefId(0:108 ~ test6[80bb]::test4) contains SCC 1 stopped after 11 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:109 ~ test6[80bb]::case_a1) | CC: 5 | Nodes: 12 | Edges: 15
13:08:14|-|: Total Time of DefId(0:109 ~ test6[80bb]::case_a1):       126.13µs
13:08:14|-|: DefId(0:109 ~ test6[80bb]::case_a1) contains SCC 1 stopped after 3 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:111 ~ test6[80bb]::case_a2) | CC: 7 | Nodes: 17 | Edges: 22
13:08:14|-|: Total Time of DefId(0:111 ~ test6[80bb]::case_a2):       375.67µs
13:08:14|-|: DefId(0:111 ~ test6[80bb]::case_a2) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:113 ~ test6[80bb]::case_constraint_number) | CC: 4 | Nodes: 11 | Edges: 13
13:08:14|-|: Total Time of DefId(0:113 ~ test6[80bb]::case_constraint_number):       155.21µs
13:08:14|-|: DefId(0:113 ~ test6[80bb]::case_constraint_number) contains SCC 1 stopped after 6 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:115 ~ test6[80bb]::case_cross_path_contamination) | CC: 3 | Nodes: 8 | Edges: 9
13:08:14|-|: Total Time of DefId(0:115 ~ test6[80bb]::case_cross_path_contamination):       54.75µs
13:08:14|-|: DefId(0:115 ~ test6[80bb]::case_cross_path_contamination) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:117 ~ test6[80bb]::test_1) | CC: 3 | Nodes: 7 | Edges: 8
13:08:14|-|: [STATS] Function: DefId(0:119 ~ test6[80bb]::test_3) | CC: 4 | Nodes: 11 | Edges: 13
13:08:14|-|: Total Time of DefId(0:119 ~ test6[80bb]::test_3):       75.63µs
13:08:14|-|: DefId(0:119 ~ test6[80bb]::test_3) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:121 ~ test6[80bb]::test_16_2) | CC: 7 | Nodes: 15 | Edges: 20
13:08:14|-|: Total Time of DefId(0:121 ~ test6[80bb]::test_16_2):       148.08µs
13:08:14|-|: DefId(0:121 ~ test6[80bb]::test_16_2) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:123 ~ test6[80bb]::test_7_2) | CC: 3 | Nodes: 8 | Edges: 9
13:08:14|-|: [STATS] Function: DefId(0:125 ~ test6[80bb]::test_8) | CC: 3 | Nodes: 8 | Edges: 9
13:08:14|-|: Total Time of DefId(0:125 ~ test6[80bb]::test_8):       69.08µs
13:08:14|-|: DefId(0:125 ~ test6[80bb]::test_8) contains SCC 1 stopped after 4 splicing iterations in depth 3.
13:08:14|-|: [STATS] Function: DefId(0:127 ~ test6[80bb]::test_10_2) | CC: 3 | Nodes: 8 | Edges: 9
13:08:14|-|: Total Time of DefId(0:127 ~ test6[80bb]::test_10_2):       42.83µs
13:08:14|-|: DefId(0:127 ~ test6[80bb]::test_10_2) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:129 ~ test6[80bb]::test_11_2) | CC: 2 | Nodes: 4 | Edges: 4
13:08:14|-|: [STATS] Function: DefId(0:131 ~ test6[80bb]::test_12) | CC: 3 | Nodes: 8 | Edges: 9
13:08:14|-|: Total Time of DefId(0:131 ~ test6[80bb]::test_12):       58.88µs
13:08:14|-|: DefId(0:131 ~ test6[80bb]::test_12) contains SCC 1 stopped after 4 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:133 ~ test6[80bb]::test_13_2) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:133 ~ test6[80bb]::test_13_2):       83.33µs
13:08:14|-|: DefId(0:133 ~ test6[80bb]::test_13_2) contains SCC 1 stopped after 5 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:135 ~ test6[80bb]::test_14_2) | CC: 2 | Nodes: 4 | Edges: 4
13:08:14|-|: [STATS] Function: DefId(0:137 ~ test6[80bb]::test_15) | CC: 6 | Nodes: 17 | Edges: 21
13:08:14|-|: [STATS] Function: DefId(0:139 ~ test6[80bb]::test_17) | CC: 4 | Nodes: 13 | Edges: 15
13:08:14|-|: Total Time of DefId(0:139 ~ test6[80bb]::test_17):       64.71µs
13:08:14|-|: DefId(0:139 ~ test6[80bb]::test_17) contains SCC 5 stopped after 1 splicing iterations in depth 0.
13:08:14|-|: [STATS] Function: DefId(0:141 ~ test6[80bb]::test_18) | CC: 5 | Nodes: 11 | Edges: 14
13:08:14|-|: [STATS] Function: DefId(0:143 ~ test6[80bb]::test_19) | CC: 4 | Nodes: 11 | Edges: 13
13:08:14|-|: Total Time of DefId(0:143 ~ test6[80bb]::test_19):       90.58µs
13:08:14|-|: DefId(0:143 ~ test6[80bb]::test_19) contains SCC 1 stopped after 4 splicing iterations in depth 3.
13:08:14|-|: [STATS] Function: DefId(0:145 ~ test6[80bb]::test_20) | CC: 7 | Nodes: 20 | Edges: 25
13:08:14|-|: Total Time of DefId(0:145 ~ test6[80bb]::test_20):       348.71µs
13:08:14|-|: DefId(0:145 ~ test6[80bb]::test_20) contains SCC 4 stopped after 3 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:147 ~ test6[80bb]::test_1_correlated_siblings) | CC: 5 | Nodes: 15 | Edges: 18
13:08:14|-|: Total Time of DefId(0:147 ~ test6[80bb]::test_1_correlated_siblings):       174.58µs
13:08:14|-|: DefId(0:147 ~ test6[80bb]::test_1_correlated_siblings) contains SCC 1 stopped after 4 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:149 ~ test6[80bb]::test_2_loop_carried_phase) | CC: 3 | Nodes: 8 | Edges: 9
13:08:14|-|: Total Time of DefId(0:149 ~ test6[80bb]::test_2_loop_carried_phase):       54.92µs
13:08:14|-|: DefId(0:149 ~ test6[80bb]::test_2_loop_carried_phase) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:151 ~ test6[80bb]::test_3_nested_infeasible) | CC: 4 | Nodes: 11 | Edges: 13
13:08:14|-|: Total Time of DefId(0:151 ~ test6[80bb]::test_3_nested_infeasible):       46.96µs
13:08:14|-|: DefId(0:151 ~ test6[80bb]::test_3_nested_infeasible) contains SCC 3 stopped after 1 splicing iterations in depth 0.
13:08:14|-|: [STATS] Function: DefId(0:153 ~ test6[80bb]::test_4_ping_pong) | CC: 2 | Nodes: 5 | Edges: 5
13:08:14|-|: Total Time of DefId(0:153 ~ test6[80bb]::test_4_ping_pong):       35.13µs
13:08:14|-|: DefId(0:153 ~ test6[80bb]::test_4_ping_pong) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:155 ~ test6[80bb]::test_5_multi_exit_accumulator) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:155 ~ test6[80bb]::test_5_multi_exit_accumulator):       62.17µs
13:08:14|-|: DefId(0:155 ~ test6[80bb]::test_5_multi_exit_accumulator) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:157 ~ test6[80bb]::test_2_correlated_delay) | CC: 6 | Nodes: 16 | Edges: 20
13:08:14|-|: Total Time of DefId(0:157 ~ test6[80bb]::test_2_correlated_delay):       230.04µs
13:08:14|-|: DefId(0:157 ~ test6[80bb]::test_2_correlated_delay) contains SCC 5 stopped after 3 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:159 ~ test6[80bb]::test_3_sibling_loops) | CC: 6 | Nodes: 20 | Edges: 24
13:08:14|-|: Total Time of DefId(0:159 ~ test6[80bb]::test_3_sibling_loops):       237.50µs
13:08:14|-|: DefId(0:159 ~ test6[80bb]::test_3_sibling_loops) contains SCC 9 stopped after 4 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:161 ~ test6[80bb]::test_5_ping_pong) | CC: 2 | Nodes: 5 | Edges: 5
13:08:14|-|: Total Time of DefId(0:161 ~ test6[80bb]::test_5_ping_pong):       35.00µs
13:08:14|-|: DefId(0:161 ~ test6[80bb]::test_5_ping_pong) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:163 ~ test6[80bb]::test_6_infeasible_path) | CC: 6 | Nodes: 15 | Edges: 19
13:08:14|-|: Total Time of DefId(0:163 ~ test6[80bb]::test_6_infeasible_path):       232.63µs
13:08:14|-|: DefId(0:163 ~ test6[80bb]::test_6_infeasible_path) contains SCC 1 stopped after 6 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:165 ~ test6[80bb]::test_7_multi_exit) | CC: 5 | Nodes: 16 | Edges: 19
13:08:14|-|: Total Time of DefId(0:165 ~ test6[80bb]::test_7_multi_exit):       523.50µs
13:08:14|-|: DefId(0:165 ~ test6[80bb]::test_7_multi_exit) contains SCC 1 stopped after 9 splicing iterations in depth 4.
13:08:14|-|: [STATS] Function: DefId(0:167 ~ test6[80bb]::test_9_deep_nest_flag) | CC: 7 | Nodes: 23 | Edges: 28
13:08:14|-|: Total Time of DefId(0:167 ~ test6[80bb]::test_9_deep_nest_flag):       1.03ms
13:08:14|-|: DefId(0:167 ~ test6[80bb]::test_9_deep_nest_flag) contains SCC 1 stopped after 4 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:169 ~ test6[80bb]::test_10_switchboard) | CC: 7 | Nodes: 14 | Edges: 19
13:08:14|-|: Total Time of DefId(0:169 ~ test6[80bb]::test_10_switchboard):       377.00µs
13:08:14|-|: DefId(0:169 ~ test6[80bb]::test_10_switchboard) contains SCC 1 stopped after 7 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:171 ~ test6[80bb]::test_11_correlated_exit) | CC: 4 | Nodes: 12 | Edges: 14
13:08:14|-|: Total Time of DefId(0:171 ~ test6[80bb]::test_11_correlated_exit):       82.29µs
13:08:14|-|: DefId(0:171 ~ test6[80bb]::test_11_correlated_exit) contains SCC 1 stopped after 4 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:173 ~ test6[80bb]::test_12_tuple_simulation) | CC: 2 | Nodes: 5 | Edges: 5
13:08:14|-|: Total Time of DefId(0:173 ~ test6[80bb]::test_12_tuple_simulation):       44.83µs
13:08:14|-|: DefId(0:173 ~ test6[80bb]::test_12_tuple_simulation) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:175 ~ test6[80bb]::test_14_nesting_shadow) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:175 ~ test6[80bb]::test_14_nesting_shadow):       96.83µs
13:08:14|-|: DefId(0:175 ~ test6[80bb]::test_14_nesting_shadow) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:177 ~ test6[80bb]::test_15_latch) | CC: 5 | Nodes: 13 | Edges: 16
13:08:14|-|: Total Time of DefId(0:177 ~ test6[80bb]::test_15_latch):       146.71µs
13:08:14|-|: DefId(0:177 ~ test6[80bb]::test_15_latch) contains SCC 1 stopped after 5 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:179 ~ test6[80bb]::test_16_mixer) | CC: 4 | Nodes: 16 | Edges: 18
13:08:14|-|: Total Time of DefId(0:179 ~ test6[80bb]::test_16_mixer):       213.75µs
13:08:14|-|: DefId(0:179 ~ test6[80bb]::test_16_mixer) contains SCC 2 stopped after 5 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:181 ~ test6[80bb]::test_18_flag_conflict) | CC: 6 | Nodes: 17 | Edges: 21
13:08:14|-|: Total Time of DefId(0:181 ~ test6[80bb]::test_18_flag_conflict):       144.83µs
13:08:14|-|: DefId(0:181 ~ test6[80bb]::test_18_flag_conflict) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:183 ~ test6[80bb]::test_20_grand_finale) | CC: 8 | Nodes: 20 | Edges: 26
13:08:14|-|: Total Time of DefId(0:183 ~ test6[80bb]::test_20_grand_finale):       2.42ms
13:08:14|-|: DefId(0:183 ~ test6[80bb]::test_20_grand_finale) contains SCC 1 stopped after 9 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:185 ~ test6[80bb]::test_3_2) | CC: 8 | Nodes: 25 | Edges: 31
13:08:14|-|: Total Time of DefId(0:185 ~ test6[80bb]::test_3_2):       661.79µs
13:08:14|-|: DefId(0:185 ~ test6[80bb]::test_3_2) contains SCC 5 stopped after 4 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:187 ~ test6[80bb]::test_4) | CC: 5 | Nodes: 15 | Edges: 18
13:08:14|-|: Total Time of DefId(0:187 ~ test6[80bb]::test_4):       1.62ms
13:08:14|-|: DefId(0:187 ~ test6[80bb]::test_4) contains SCC 1 stopped after 21 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:189 ~ test6[80bb]::test_5) | CC: 4 | Nodes: 13 | Edges: 15
13:08:14|-|: Total Time of DefId(0:189 ~ test6[80bb]::test_5):       137.88µs
13:08:14|-|: DefId(0:189 ~ test6[80bb]::test_5) contains SCC 2 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:191 ~ test6[80bb]::test_6_2) | CC: 5 | Nodes: 16 | Edges: 19
13:08:14|-|: Total Time of DefId(0:191 ~ test6[80bb]::test_6_2):       971.92µs
13:08:14|-|: DefId(0:191 ~ test6[80bb]::test_6_2) contains SCC 1 stopped after 25 splicing iterations in depth 3.
13:08:14|-|: [STATS] Function: DefId(0:193 ~ test6[80bb]::test_7) | CC: 6 | Nodes: 19 | Edges: 23
13:08:14|-|: Total Time of DefId(0:193 ~ test6[80bb]::test_7):       384.04µs
13:08:14|-|: DefId(0:193 ~ test6[80bb]::test_7) contains SCC 1 stopped after 10 splicing iterations in depth 3.
13:08:14|-|: [STATS] Function: DefId(0:195 ~ test6[80bb]::test_10) | CC: 5 | Nodes: 15 | Edges: 18
13:08:14|-|: Total Time of DefId(0:195 ~ test6[80bb]::test_10):       966.71µs
13:08:14|-|: DefId(0:195 ~ test6[80bb]::test_10) contains SCC 1 stopped after 22 splicing iterations in depth 4.
13:08:14|-|: [STATS] Function: DefId(0:197 ~ test6[80bb]::test_11) | CC: 5 | Nodes: 15 | Edges: 18
13:08:14|-|: Total Time of DefId(0:197 ~ test6[80bb]::test_11):       364.50µs
13:08:14|-|: DefId(0:197 ~ test6[80bb]::test_11) contains SCC 1 stopped after 10 splicing iterations in depth 3.
13:08:14|-|: [STATS] Function: DefId(0:199 ~ test6[80bb]::test_13) | CC: 4 | Nodes: 12 | Edges: 14
13:08:14|-|: Total Time of DefId(0:199 ~ test6[80bb]::test_13):       96.29µs
13:08:14|-|: DefId(0:199 ~ test6[80bb]::test_13) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:201 ~ test6[80bb]::test_14) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:201 ~ test6[80bb]::test_14):       250.29µs
13:08:14|-|: DefId(0:201 ~ test6[80bb]::test_14) contains SCC 1 stopped after 12 splicing iterations in depth 5.
13:08:14|-|: [STATS] Function: DefId(0:203 ~ test6[80bb]::test_15_2) | CC: 4 | Nodes: 11 | Edges: 13
13:08:14|-|: Total Time of DefId(0:203 ~ test6[80bb]::test_15_2):       109.21µs
13:08:14|-|: DefId(0:203 ~ test6[80bb]::test_15_2) contains SCC 1 stopped after 4 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:205 ~ test6[80bb]::case_1) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:205 ~ test6[80bb]::case_1):       43.58µs
13:08:14|-|: DefId(0:205 ~ test6[80bb]::case_1) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:207 ~ test6[80bb]::case_2) | CC: 3 | Nodes: 8 | Edges: 9
13:08:14|-|: Total Time of DefId(0:207 ~ test6[80bb]::case_2):       42.08µs
13:08:14|-|: DefId(0:207 ~ test6[80bb]::case_2) contains SCC 2 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:209 ~ test6[80bb]::case_3) | CC: 4 | Nodes: 13 | Edges: 15
13:08:14|-|: Total Time of DefId(0:209 ~ test6[80bb]::case_3):       69.75µs
13:08:14|-|: DefId(0:209 ~ test6[80bb]::case_3) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:14|-|: [STATS] Function: DefId(0:211 ~ test6[80bb]::case_4) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:211 ~ test6[80bb]::case_4):       51.04µs
13:08:14|-|: DefId(0:211 ~ test6[80bb]::case_4) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:213 ~ test6[80bb]::case_5) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:213 ~ test6[80bb]::case_5):       63.17µs
13:08:14|-|: DefId(0:213 ~ test6[80bb]::case_5) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:215 ~ test6[80bb]::case_6) | CC: 5 | Nodes: 17 | Edges: 20
13:08:14|-|: Total Time of DefId(0:215 ~ test6[80bb]::case_6):       750.13µs
13:08:14|-|: DefId(0:215 ~ test6[80bb]::case_6) contains SCC 2 stopped after 4 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:217 ~ test6[80bb]::case_7) | CC: 5 | Nodes: 17 | Edges: 20
13:08:14|-|: Total Time of DefId(0:217 ~ test6[80bb]::case_7):       136.75µs
13:08:14|-|: DefId(0:217 ~ test6[80bb]::case_7) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:219 ~ test6[80bb]::case_8) | CC: 2 | Nodes: 5 | Edges: 5
13:08:14|-|: Total Time of DefId(0:219 ~ test6[80bb]::case_8):       27.88µs
13:08:14|-|: DefId(0:219 ~ test6[80bb]::case_8) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:221 ~ test6[80bb]::case_9) | CC: 5 | Nodes: 17 | Edges: 20
13:08:14|-|: Total Time of DefId(0:221 ~ test6[80bb]::case_9):       200.92µs
13:08:14|-|: DefId(0:221 ~ test6[80bb]::case_9) contains SCC 4 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:223 ~ test6[80bb]::case_10) | CC: 6 | Nodes: 21 | Edges: 25
13:08:14|-|: Total Time of DefId(0:223 ~ test6[80bb]::case_10):       160.29µs
13:08:14|-|: DefId(0:223 ~ test6[80bb]::case_10) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:225 ~ test6[80bb]::case_11) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:225 ~ test6[80bb]::case_11):       61.92µs
13:08:14|-|: DefId(0:225 ~ test6[80bb]::case_11) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:227 ~ test6[80bb]::case_12) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:227 ~ test6[80bb]::case_12):       45.96µs
13:08:14|-|: DefId(0:227 ~ test6[80bb]::case_12) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:14|-|: [STATS] Function: DefId(0:229 ~ test6[80bb]::case_13) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:229 ~ test6[80bb]::case_13):       34.00µs
13:08:14|-|: DefId(0:229 ~ test6[80bb]::case_13) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:14|-|: [STATS] Function: DefId(0:231 ~ test6[80bb]::case_14) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:231 ~ test6[80bb]::case_14):       61.17µs
13:08:14|-|: DefId(0:231 ~ test6[80bb]::case_14) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:233 ~ test6[80bb]::case_15) | CC: 4 | Nodes: 13 | Edges: 15
13:08:14|-|: Total Time of DefId(0:233 ~ test6[80bb]::case_15):       76.00µs
13:08:14|-|: DefId(0:233 ~ test6[80bb]::case_15) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:14|-|: [STATS] Function: DefId(0:235 ~ test6[80bb]::case_16) | CC: 5 | Nodes: 13 | Edges: 16
13:08:14|-|: Total Time of DefId(0:235 ~ test6[80bb]::case_16):       204.00µs
13:08:14|-|: DefId(0:235 ~ test6[80bb]::case_16) contains SCC 1 stopped after 5 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:237 ~ test6[80bb]::case_17) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:237 ~ test6[80bb]::case_17):       57.13µs
13:08:14|-|: DefId(0:237 ~ test6[80bb]::case_17) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:239 ~ test6[80bb]::case_18) | CC: 4 | Nodes: 13 | Edges: 15
13:08:14|-|: Total Time of DefId(0:239 ~ test6[80bb]::case_18):       137.75µs
13:08:14|-|: DefId(0:239 ~ test6[80bb]::case_18) contains SCC 1 stopped after 5 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:241 ~ test6[80bb]::case_19) | CC: 2 | Nodes: 4 | Edges: 4
13:08:14|-|: [STATS] Function: DefId(0:243 ~ test6[80bb]::case_20) | CC: 4 | Nodes: 13 | Edges: 15
13:08:14|-|: Total Time of DefId(0:243 ~ test6[80bb]::case_20):       246.79µs
13:08:14|-|: DefId(0:243 ~ test6[80bb]::case_20) contains SCC 2 stopped after 5 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:245 ~ test6[80bb]::case_21) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:245 ~ test6[80bb]::case_21):       37.38µs
13:08:14|-|: DefId(0:245 ~ test6[80bb]::case_21) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:14|-|: [STATS] Function: DefId(0:247 ~ test6[80bb]::case_22) | CC: 6 | Nodes: 21 | Edges: 25
13:08:14|-|: Total Time of DefId(0:247 ~ test6[80bb]::case_22):       4.57ms
13:08:14|-|: DefId(0:247 ~ test6[80bb]::case_22) contains SCC 1 stopped after 24 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:249 ~ test6[80bb]::case_23) | CC: 5 | Nodes: 17 | Edges: 20
13:08:14|-|: Total Time of DefId(0:249 ~ test6[80bb]::case_23):       330.08µs
13:08:14|-|: DefId(0:249 ~ test6[80bb]::case_23) contains SCC 1 stopped after 4 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:251 ~ test6[80bb]::case_24) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:251 ~ test6[80bb]::case_24):       154.46µs
13:08:14|-|: DefId(0:251 ~ test6[80bb]::case_24) contains SCC 1 stopped after 5 splicing iterations in depth 2.
13:08:14|-|: [STATS] Function: DefId(0:253 ~ test6[80bb]::case_26) | CC: 2 | Nodes: 5 | Edges: 5
13:08:14|-|: Total Time of DefId(0:253 ~ test6[80bb]::case_26):       24.88µs
13:08:14|-|: DefId(0:253 ~ test6[80bb]::case_26) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:255 ~ test6[80bb]::case_27) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:255 ~ test6[80bb]::case_27):       102.42µs
13:08:14|-|: DefId(0:255 ~ test6[80bb]::case_27) contains SCC 5 stopped after 1 splicing iterations in depth 0.
13:08:14|-|: [STATS] Function: DefId(0:257 ~ test6[80bb]::case_28) | CC: 3 | Nodes: 9 | Edges: 10
13:08:14|-|: Total Time of DefId(0:257 ~ test6[80bb]::case_28):       110.46µs
13:08:14|-|: DefId(0:257 ~ test6[80bb]::case_28) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:14|-|: [STATS] Function: DefId(0:259 ~ test6[80bb]::case_29) | CC: 4 | Nodes: 12 | Edges: 14
13:08:14|-|: Total Time of DefId(0:259 ~ test6[80bb]::case_29):       60.50µs
13:08:14|-|: DefId(0:259 ~ test6[80bb]::case_29) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:14|-|: [STATS] Function: DefId(0:261 ~ test6[80bb]::case_30) | CC: 5 | Nodes: 16 | Edges: 19
13:08:14|-|: Total Time of DefId(0:261 ~ test6[80bb]::case_30):       142.50µs
13:08:14|-|: DefId(0:261 ~ test6[80bb]::case_30) contains SCC 3 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:215 ~ test7[1d05]::{impl#1}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:218 ~ test7[1d05]::{impl#3}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:231 ~ test7[1d05]::{impl#6}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:234 ~ test7[1d05]::{impl#8}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:3 ~ test7[1d05]::scc_temporal_case_1) | CC: 9 | Nodes: 30 | Edges: 37
13:08:42|-|: Total Time of DefId(0:3 ~ test7[1d05]::scc_temporal_case_1):       5.48ms
13:08:42|-|: DefId(0:3 ~ test7[1d05]::scc_temporal_case_1) contains SCC 1 stopped after 8 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:5 ~ test7[1d05]::scc_temporal_case_2) | CC: 5 | Nodes: 14 | Edges: 17
13:08:42|-|: Total Time of DefId(0:5 ~ test7[1d05]::scc_temporal_case_2):       451.71µs
13:08:42|-|: DefId(0:5 ~ test7[1d05]::scc_temporal_case_2) contains SCC 3 stopped after 4 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:7 ~ test7[1d05]::scc_temporal_case_3) | CC: 8 | Nodes: 25 | Edges: 31
13:08:42|-|: Total Time of DefId(0:7 ~ test7[1d05]::scc_temporal_case_3):       1.79ms
13:08:42|-|: DefId(0:7 ~ test7[1d05]::scc_temporal_case_3) contains SCC 2 stopped after 4 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:9 ~ test7[1d05]::scc_temporal_case_4) | CC: 4 | Nodes: 12 | Edges: 14
13:08:42|-|: Total Time of DefId(0:9 ~ test7[1d05]::scc_temporal_case_4):       262.42µs
13:08:42|-|: DefId(0:9 ~ test7[1d05]::scc_temporal_case_4) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:11 ~ test7[1d05]::scc_temporal_case_5) | CC: 6 | Nodes: 19 | Edges: 23
13:08:42|-|: Total Time of DefId(0:11 ~ test7[1d05]::scc_temporal_case_5):       1.97ms
13:08:42|-|: DefId(0:11 ~ test7[1d05]::scc_temporal_case_5) contains SCC 1 stopped after 11 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:13 ~ test7[1d05]::scc_temporal_case_6) | CC: 6 | Nodes: 18 | Edges: 22
13:08:42|-|: Total Time of DefId(0:13 ~ test7[1d05]::scc_temporal_case_6):       713.38µs
13:08:42|-|: DefId(0:13 ~ test7[1d05]::scc_temporal_case_6) contains SCC 4 stopped after 5 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:15 ~ test7[1d05]::scc_temporal_case_7) | CC: 4 | Nodes: 12 | Edges: 14
13:08:42|-|: Total Time of DefId(0:15 ~ test7[1d05]::scc_temporal_case_7):       147.21µs
13:08:42|-|: DefId(0:15 ~ test7[1d05]::scc_temporal_case_7) contains SCC 1 stopped after 4 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:17 ~ test7[1d05]::scc_temporal_case_8) | CC: 4 | Nodes: 11 | Edges: 13
13:08:42|-|: Total Time of DefId(0:17 ~ test7[1d05]::scc_temporal_case_8):       161.38µs
13:08:42|-|: DefId(0:17 ~ test7[1d05]::scc_temporal_case_8) contains SCC 1 stopped after 5 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:19 ~ test7[1d05]::scc_temporal_case_9) | CC: 7 | Nodes: 21 | Edges: 26
13:08:42|-|: Total Time of DefId(0:19 ~ test7[1d05]::scc_temporal_case_9):       732.29µs
13:08:42|-|: DefId(0:19 ~ test7[1d05]::scc_temporal_case_9) contains SCC 3 stopped after 3 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:21 ~ test7[1d05]::scc_temporal_case_10) | CC: 4 | Nodes: 11 | Edges: 13
13:08:42|-|: Total Time of DefId(0:21 ~ test7[1d05]::scc_temporal_case_10):       83.33µs
13:08:42|-|: DefId(0:21 ~ test7[1d05]::scc_temporal_case_10) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:23 ~ test7[1d05]::scc_temporal_case_11) | CC: 4 | Nodes: 11 | Edges: 13
13:08:42|-|: Total Time of DefId(0:23 ~ test7[1d05]::scc_temporal_case_11):       103.08µs
13:08:42|-|: DefId(0:23 ~ test7[1d05]::scc_temporal_case_11) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:25 ~ test7[1d05]::scc_temporal_case_12) | CC: 5 | Nodes: 13 | Edges: 16
13:08:42|-|: Total Time of DefId(0:25 ~ test7[1d05]::scc_temporal_case_12):       69.38µs
13:08:42|-|: DefId(0:25 ~ test7[1d05]::scc_temporal_case_12) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:42|-|: [STATS] Function: DefId(0:27 ~ test7[1d05]::scc_temporal_case_13) | CC: 3 | Nodes: 7 | Edges: 8
13:08:42|-|: Total Time of DefId(0:27 ~ test7[1d05]::scc_temporal_case_13):       31.71µs
13:08:42|-|: DefId(0:27 ~ test7[1d05]::scc_temporal_case_13) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:29 ~ test7[1d05]::scc_temporal_case_14) | CC: 3 | Nodes: 8 | Edges: 9
13:08:42|-|: Total Time of DefId(0:29 ~ test7[1d05]::scc_temporal_case_14):       38.46µs
13:08:42|-|: DefId(0:29 ~ test7[1d05]::scc_temporal_case_14) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:31 ~ test7[1d05]::scc_temporal_case_15) | CC: 5 | Nodes: 12 | Edges: 15
13:08:42|-|: Total Time of DefId(0:31 ~ test7[1d05]::scc_temporal_case_15):       65.63µs
13:08:42|-|: DefId(0:31 ~ test7[1d05]::scc_temporal_case_15) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:42|-|: [STATS] Function: DefId(0:33 ~ test7[1d05]::scc_temporal_case_16) | CC: 2 | Nodes: 4 | Edges: 4
13:08:42|-|: Total Time of DefId(0:33 ~ test7[1d05]::scc_temporal_case_16):       11.96µs
13:08:42|-|: DefId(0:33 ~ test7[1d05]::scc_temporal_case_16) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:42|-|: [STATS] Function: DefId(0:35 ~ test7[1d05]::scc_temporal_case_17) | CC: 2 | Nodes: 5 | Edges: 5
13:08:42|-|: Total Time of DefId(0:35 ~ test7[1d05]::scc_temporal_case_17):       36.71µs
13:08:42|-|: DefId(0:35 ~ test7[1d05]::scc_temporal_case_17) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:37 ~ test7[1d05]::scc_temporal_case_18) | CC: 3 | Nodes: 6 | Edges: 7
13:08:42|-|: [STATS] Function: DefId(0:39 ~ test7[1d05]::scc_temporal_case_19) | CC: 3 | Nodes: 8 | Edges: 9
13:08:42|-|: [STATS] Function: DefId(0:41 ~ test7[1d05]::scc_temporal_case_20) | CC: 5 | Nodes: 14 | Edges: 17
13:08:42|-|: Total Time of DefId(0:41 ~ test7[1d05]::scc_temporal_case_20):       126.17µs
13:08:42|-|: DefId(0:41 ~ test7[1d05]::scc_temporal_case_20) contains SCC 4 stopped after 4 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:43 ~ test7[1d05]::scc_temporal_case_21) | CC: 4 | Nodes: 12 | Edges: 14
13:08:42|-|: [STATS] Function: DefId(0:45 ~ test7[1d05]::scc_temporal_case_22) | CC: 3 | Nodes: 7 | Edges: 8
13:08:42|-|: [STATS] Function: DefId(0:47 ~ test7[1d05]::scc_temporal_case_23) | CC: 4 | Nodes: 10 | Edges: 12
13:08:42|-|: Total Time of DefId(0:47 ~ test7[1d05]::scc_temporal_case_23):       64.04µs
13:08:42|-|: DefId(0:47 ~ test7[1d05]::scc_temporal_case_23) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:49 ~ test7[1d05]::scc_temporal_case_24) | CC: 4 | Nodes: 10 | Edges: 12
13:08:42|-|: [STATS] Function: DefId(0:51 ~ test7[1d05]::scc_temporal_case_25) | CC: 6 | Nodes: 12 | Edges: 16
13:08:42|-|: Total Time of DefId(0:51 ~ test7[1d05]::scc_temporal_case_25):       1.27ms
13:08:42|-|: DefId(0:51 ~ test7[1d05]::scc_temporal_case_25) contains SCC 1 stopped after 34 splicing iterations in depth 4.
13:08:42|-|: [STATS] Function: DefId(0:53 ~ test7[1d05]::scc_temporal_case_26) | CC: 5 | Nodes: 14 | Edges: 17
13:08:42|-|: Total Time of DefId(0:53 ~ test7[1d05]::scc_temporal_case_26):       166.50µs
13:08:42|-|: DefId(0:53 ~ test7[1d05]::scc_temporal_case_26) contains SCC 1 stopped after 6 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:55 ~ test7[1d05]::scc_temporal_case_27) | CC: 5 | Nodes: 14 | Edges: 17
13:08:42|-|: Total Time of DefId(0:55 ~ test7[1d05]::scc_temporal_case_27):       288.75µs
13:08:42|-|: DefId(0:55 ~ test7[1d05]::scc_temporal_case_27) contains SCC 1 stopped after 10 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:57 ~ test7[1d05]::scc_temporal_case_28) | CC: 5 | Nodes: 14 | Edges: 17
13:08:42|-|: Total Time of DefId(0:57 ~ test7[1d05]::scc_temporal_case_28):       710.42µs
13:08:42|-|: DefId(0:57 ~ test7[1d05]::scc_temporal_case_28) contains SCC 1 stopped after 23 splicing iterations in depth 4.
13:08:42|-|: [STATS] Function: DefId(0:59 ~ test7[1d05]::scc_temporal_case_29) | CC: 4 | Nodes: 10 | Edges: 12
13:08:42|-|: Total Time of DefId(0:59 ~ test7[1d05]::scc_temporal_case_29):       119.75µs
13:08:42|-|: DefId(0:59 ~ test7[1d05]::scc_temporal_case_29) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:61 ~ test7[1d05]::scc_temporal_case_30) | CC: 5 | Nodes: 10 | Edges: 13
13:08:42|-|: Total Time of DefId(0:61 ~ test7[1d05]::scc_temporal_case_30):       301.79µs
13:08:42|-|: DefId(0:61 ~ test7[1d05]::scc_temporal_case_30) contains SCC 1 stopped after 11 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:63 ~ test7[1d05]::random_test1) | CC: 2 | Nodes: 6 | Edges: 5
13:08:42|-|: [STATS] Function: DefId(0:86 ~ test7[1d05]::random_test2) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:247 ~ test7[1d05]::{impl#11}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:251 ~ test7[1d05]::{impl#14}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:253 ~ test7[1d05]::{impl#15}::assert_receiver_is_total_eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:263 ~ test7[1d05]::{impl#17}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:267 ~ test7[1d05]::{impl#20}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:269 ~ test7[1d05]::{impl#21}::assert_receiver_is_total_eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:87 ~ test7[1d05]::random_int_test2) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:279 ~ test7[1d05]::{impl#23}::clone) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:283 ~ test7[1d05]::{impl#26}::eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:285 ~ test7[1d05]::{impl#27}::assert_receiver_is_total_eq) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:88 ~ test7[1d05]::random_test3) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:89 ~ test7[1d05]::test1) | CC: 3 | Nodes: 6 | Edges: 7
13:08:42|-|: Total Time of DefId(0:89 ~ test7[1d05]::test1):       87.88µs
13:08:42|-|: DefId(0:89 ~ test7[1d05]::test1) contains SCC 1 stopped after 5 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:91 ~ test7[1d05]::test5) | CC: 2 | Nodes: 4 | Edges: 4
13:08:42|-|: Total Time of DefId(0:91 ~ test7[1d05]::test5):       21.21µs
13:08:42|-|: DefId(0:91 ~ test7[1d05]::test5) contains SCC 1 stopped after 1 splicing iterations in depth 0.
13:08:42|-|: [STATS] Function: DefId(0:93 ~ test7[1d05]::pipeline_propagation) | CC: 2 | Nodes: 7 | Edges: 7
13:08:42|-|: Total Time of DefId(0:93 ~ test7[1d05]::pipeline_propagation):       98.33µs
13:08:42|-|: DefId(0:93 ~ test7[1d05]::pipeline_propagation) contains SCC 2 stopped after 3 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:95 ~ test7[1d05]::test_pipeline_correlation) | CC: 6 | Nodes: 16 | Edges: 20
13:08:42|-|: Total Time of DefId(0:95 ~ test7[1d05]::test_pipeline_correlation):       699.33µs
13:08:42|-|: DefId(0:95 ~ test7[1d05]::test_pipeline_correlation) contains SCC 1 stopped after 9 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:97 ~ test7[1d05]::case_unroll_pipeline) | CC: 2 | Nodes: 5 | Edges: 5
13:08:42|-|: Total Time of DefId(0:97 ~ test7[1d05]::case_unroll_pipeline):       135.71µs
13:08:42|-|: DefId(0:97 ~ test7[1d05]::case_unroll_pipeline) contains SCC 1 stopped after 3 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:99 ~ test7[1d05]::test_16) | CC: 3 | Nodes: 9 | Edges: 10
13:08:42|-|: Total Time of DefId(0:99 ~ test7[1d05]::test_16):       80.33µs
13:08:42|-|: DefId(0:99 ~ test7[1d05]::test_16) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:101 ~ test7[1d05]::test_1_pipeline) | CC: 2 | Nodes: 5 | Edges: 5
13:08:42|-|: Total Time of DefId(0:101 ~ test7[1d05]::test_1_pipeline):       80.58µs
13:08:42|-|: DefId(0:101 ~ test7[1d05]::test_1_pipeline) contains SCC 1 stopped after 5 splicing iterations in depth 4.
13:08:42|-|: [STATS] Function: DefId(0:103 ~ test7[1d05]::test_4_nested_depth_3) | CC: 6 | Nodes: 20 | Edges: 24
13:08:42|-|: Total Time of DefId(0:103 ~ test7[1d05]::test_4_nested_depth_3):       65.76ms
13:08:42|-|: DefId(0:103 ~ test7[1d05]::test_4_nested_depth_3) contains SCC 1 stopped after 41 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:105 ~ test7[1d05]::test_13_state_machine) | CC: 4 | Nodes: 9 | Edges: 11
13:08:42|-|: Total Time of DefId(0:105 ~ test7[1d05]::test_13_state_machine):       248.71µs
13:08:42|-|: DefId(0:105 ~ test7[1d05]::test_13_state_machine) contains SCC 1 stopped after 13 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:107 ~ test7[1d05]::test_17_ptr_chase) | CC: 3 | Nodes: 9 | Edges: 10
13:08:42|-|: Total Time of DefId(0:107 ~ test7[1d05]::test_17_ptr_chase):       105.92µs
13:08:42|-|: DefId(0:107 ~ test7[1d05]::test_17_ptr_chase) contains SCC 1 stopped after 4 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:109 ~ test7[1d05]::test_1) | CC: 7 | Nodes: 21 | Edges: 26
13:08:42|-|: Total Time of DefId(0:109 ~ test7[1d05]::test_1):       489.46µs
13:08:42|-|: DefId(0:109 ~ test7[1d05]::test_1) contains SCC 1 stopped after 10 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:111 ~ test7[1d05]::test_2) | CC: 6 | Nodes: 17 | Edges: 21
13:08:42|-|: Total Time of DefId(0:111 ~ test7[1d05]::test_2):       1.07ms
13:08:42|-|: DefId(0:111 ~ test7[1d05]::test_2) contains SCC 1 stopped after 13 splicing iterations in depth 4.
13:08:42|-|: [STATS] Function: DefId(0:113 ~ test7[1d05]::test_8) | CC: 2 | Nodes: 5 | Edges: 5
13:08:42|-|: Total Time of DefId(0:113 ~ test7[1d05]::test_8):       49.00µs
13:08:42|-|: DefId(0:113 ~ test7[1d05]::test_8) contains SCC 1 stopped after 4 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:115 ~ test7[1d05]::test_9) | CC: 8 | Nodes: 17 | Edges: 23
13:08:42|-|: Total Time of DefId(0:115 ~ test7[1d05]::test_9):       230.00µs
13:08:42|-|: DefId(0:115 ~ test7[1d05]::test_9) contains SCC 1 stopped after 4 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:117 ~ test7[1d05]::test_12) | CC: 5 | Nodes: 14 | Edges: 17
13:08:42|-|: Total Time of DefId(0:117 ~ test7[1d05]::test_12):       1.40ms
13:08:42|-|: DefId(0:117 ~ test7[1d05]::test_12) contains SCC 1 stopped after 25 splicing iterations in depth 5.
13:08:42|-|: [STATS] Function: DefId(0:119 ~ test7[1d05]::test_16_2) | CC: 8 | Nodes: 26 | Edges: 32
13:08:42|-|: Total Time of DefId(0:119 ~ test7[1d05]::test_16_2):       7.89ms
13:08:42|-|: DefId(0:119 ~ test7[1d05]::test_16_2) contains SCC 3 stopped after 5 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:121 ~ test7[1d05]::test_17) | CC: 4 | Nodes: 14 | Edges: 16
13:08:42|-|: Total Time of DefId(0:121 ~ test7[1d05]::test_17):       1.52ms
13:08:42|-|: DefId(0:121 ~ test7[1d05]::test_17) contains SCC 1 stopped after 37 splicing iterations in depth 4.
13:08:42|-|: [STATS] Function: DefId(0:123 ~ test7[1d05]::test_18) | CC: 4 | Nodes: 12 | Edges: 14
13:08:42|-|: Total Time of DefId(0:123 ~ test7[1d05]::test_18):       638.04µs
13:08:42|-|: DefId(0:123 ~ test7[1d05]::test_18) contains SCC 1 stopped after 20 splicing iterations in depth 5.
13:08:42|-|: [STATS] Function: DefId(0:125 ~ test7[1d05]::test_19) | CC: 5 | Nodes: 15 | Edges: 18
13:08:42|-|: Total Time of DefId(0:125 ~ test7[1d05]::test_19):       1.24ms
13:08:42|-|: DefId(0:125 ~ test7[1d05]::test_19) contains SCC 1 stopped after 20 splicing iterations in depth 5.
13:08:42|-|: [STATS] Function: DefId(0:127 ~ test7[1d05]::test_20) | CC: 7 | Nodes: 19 | Edges: 24
13:08:42|-|: Total Time of DefId(0:127 ~ test7[1d05]::test_20):       749.75µs
13:08:42|-|: DefId(0:127 ~ test7[1d05]::test_20) contains SCC 1 stopped after 12 splicing iterations in depth 4.
13:08:42|-|: [STATS] Function: DefId(0:129 ~ test7[1d05]::random_bool_test4) | CC: 2 | Nodes: 1 | Edges: 0
13:08:42|-|: [STATS] Function: DefId(0:130 ~ test7[1d05]::case_1) | CC: 5 | Nodes: 15 | Edges: 18
13:08:42|-|: Total Time of DefId(0:130 ~ test7[1d05]::case_1):       262.58µs
13:08:42|-|: DefId(0:130 ~ test7[1d05]::case_1) contains SCC 1 stopped after 7 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:132 ~ test7[1d05]::case_2) | CC: 5 | Nodes: 15 | Edges: 18
13:08:42|-|: Total Time of DefId(0:132 ~ test7[1d05]::case_2):       161.67µs
13:08:42|-|: DefId(0:132 ~ test7[1d05]::case_2) contains SCC 2 stopped after 5 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:134 ~ test7[1d05]::case_3) | CC: 5 | Nodes: 16 | Edges: 19
13:08:42|-|: Total Time of DefId(0:134 ~ test7[1d05]::case_3):       78.54µs
13:08:42|-|: DefId(0:134 ~ test7[1d05]::case_3) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:136 ~ test7[1d05]::case_4) | CC: 5 | Nodes: 15 | Edges: 18
13:08:42|-|: Total Time of DefId(0:136 ~ test7[1d05]::case_4):       227.54µs
13:08:42|-|: DefId(0:136 ~ test7[1d05]::case_4) contains SCC 1 stopped after 5 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:138 ~ test7[1d05]::case_5) | CC: 4 | Nodes: 12 | Edges: 14
13:08:42|-|: Total Time of DefId(0:138 ~ test7[1d05]::case_5):       108.67µs
13:08:42|-|: DefId(0:138 ~ test7[1d05]::case_5) contains SCC 1 stopped after 3 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:140 ~ test7[1d05]::case_6) | CC: 7 | Nodes: 23 | Edges: 28
13:08:42|-|: Total Time of DefId(0:140 ~ test7[1d05]::case_6):       2.42ms
13:08:42|-|: DefId(0:140 ~ test7[1d05]::case_6) contains SCC 2 stopped after 7 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:142 ~ test7[1d05]::case_7) | CC: 7 | Nodes: 22 | Edges: 27
13:08:42|-|: Total Time of DefId(0:142 ~ test7[1d05]::case_7):       687.08µs
13:08:42|-|: DefId(0:142 ~ test7[1d05]::case_7) contains SCC 1 stopped after 7 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:144 ~ test7[1d05]::case_8) | CC: 2 | Nodes: 5 | Edges: 5
13:08:42|-|: Total Time of DefId(0:144 ~ test7[1d05]::case_8):       29.38µs
13:08:42|-|: DefId(0:144 ~ test7[1d05]::case_8) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:146 ~ test7[1d05]::case_9) | CC: 11 | Nodes: 35 | Edges: 44
13:08:42|-|: Total Time of DefId(0:146 ~ test7[1d05]::case_9):       10.04ms
13:08:42|-|: DefId(0:146 ~ test7[1d05]::case_9) contains SCC 4 stopped after 5 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:148 ~ test7[1d05]::case_10) | CC: 5 | Nodes: 14 | Edges: 17
13:08:42|-|: Total Time of DefId(0:148 ~ test7[1d05]::case_10):       94.17µs
13:08:42|-|: DefId(0:148 ~ test7[1d05]::case_10) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:150 ~ test7[1d05]::case_11) | CC: 3 | Nodes: 9 | Edges: 10
13:08:42|-|: Total Time of DefId(0:150 ~ test7[1d05]::case_11):       65.08µs
13:08:42|-|: DefId(0:150 ~ test7[1d05]::case_11) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:152 ~ test7[1d05]::case_12) | CC: 3 | Nodes: 8 | Edges: 9
13:08:42|-|: Total Time of DefId(0:152 ~ test7[1d05]::case_12):       60.71µs
13:08:42|-|: DefId(0:152 ~ test7[1d05]::case_12) contains SCC 2 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:154 ~ test7[1d05]::case_13) | CC: 3 | Nodes: 9 | Edges: 10
13:08:42|-|: Total Time of DefId(0:154 ~ test7[1d05]::case_13):       42.21µs
13:08:42|-|: DefId(0:154 ~ test7[1d05]::case_13) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:156 ~ test7[1d05]::case_14) | CC: 3 | Nodes: 8 | Edges: 9
13:08:42|-|: Total Time of DefId(0:156 ~ test7[1d05]::case_14):       42.00µs
13:08:42|-|: DefId(0:156 ~ test7[1d05]::case_14) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:158 ~ test7[1d05]::case_15) | CC: 4 | Nodes: 12 | Edges: 14
13:08:42|-|: Total Time of DefId(0:158 ~ test7[1d05]::case_15):       85.21µs
13:08:42|-|: DefId(0:158 ~ test7[1d05]::case_15) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:160 ~ test7[1d05]::case_16) | CC: 5 | Nodes: 13 | Edges: 16
13:08:42|-|: Total Time of DefId(0:160 ~ test7[1d05]::case_16):       572.71µs
13:08:42|-|: DefId(0:160 ~ test7[1d05]::case_16) contains SCC 1 stopped after 20 splicing iterations in depth 4.
13:08:42|-|: [STATS] Function: DefId(0:162 ~ test7[1d05]::case_17) | CC: 4 | Nodes: 13 | Edges: 15
13:08:42|-|: Total Time of DefId(0:162 ~ test7[1d05]::case_17):       257.42µs
13:08:42|-|: DefId(0:162 ~ test7[1d05]::case_17) contains SCC 1 stopped after 11 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:164 ~ test7[1d05]::case_18) | CC: 4 | Nodes: 11 | Edges: 13
13:08:42|-|: Total Time of DefId(0:164 ~ test7[1d05]::case_18):       150.38µs
13:08:42|-|: DefId(0:164 ~ test7[1d05]::case_18) contains SCC 1 stopped after 6 splicing iterations in depth 3.
13:08:42|-|: [STATS] Function: DefId(0:166 ~ test7[1d05]::case_19) | CC: 3 | Nodes: 8 | Edges: 9
13:08:42|-|: Total Time of DefId(0:166 ~ test7[1d05]::case_19):       57.08µs
13:08:42|-|: DefId(0:166 ~ test7[1d05]::case_19) contains SCC 1 stopped after 3 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:168 ~ test7[1d05]::case_20) | CC: 4 | Nodes: 12 | Edges: 14
13:08:42|-|: Total Time of DefId(0:168 ~ test7[1d05]::case_20):       132.88µs
13:08:42|-|: DefId(0:168 ~ test7[1d05]::case_20) contains SCC 2 stopped after 5 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:170 ~ test7[1d05]::case_21) | CC: 3 | Nodes: 8 | Edges: 9
13:08:42|-|: Total Time of DefId(0:170 ~ test7[1d05]::case_21):       43.25µs
13:08:42|-|: DefId(0:170 ~ test7[1d05]::case_21) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:172 ~ test7[1d05]::case_22) | CC: 6 | Nodes: 17 | Edges: 21
13:08:42|-|: Total Time of DefId(0:172 ~ test7[1d05]::case_22):       3.34ms
13:08:42|-|: DefId(0:172 ~ test7[1d05]::case_22) contains SCC 1 stopped after 34 splicing iterations in depth 5.
13:08:42|-|: [STATS] Function: DefId(0:174 ~ test7[1d05]::case_23) | CC: 4 | Nodes: 15 | Edges: 17
13:08:42|-|: Total Time of DefId(0:174 ~ test7[1d05]::case_23):       318.38µs
13:08:42|-|: DefId(0:174 ~ test7[1d05]::case_23) contains SCC 1 stopped after 5 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:176 ~ test7[1d05]::case_24) | CC: 4 | Nodes: 11 | Edges: 13
13:08:42|-|: Total Time of DefId(0:176 ~ test7[1d05]::case_24):       291.92µs
13:08:42|-|: DefId(0:176 ~ test7[1d05]::case_24) contains SCC 1 stopped after 7 splicing iterations in depth 2.
13:08:42|-|: [STATS] Function: DefId(0:178 ~ test7[1d05]::case_26) | CC: 2 | Nodes: 5 | Edges: 5
13:08:42|-|: Total Time of DefId(0:178 ~ test7[1d05]::case_26):       25.21µs
13:08:42|-|: DefId(0:178 ~ test7[1d05]::case_26) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:180 ~ test7[1d05]::case_27) | CC: 4 | Nodes: 12 | Edges: 14
13:08:42|-|: Total Time of DefId(0:180 ~ test7[1d05]::case_27):       111.54µs
13:08:42|-|: DefId(0:180 ~ test7[1d05]::case_27) contains SCC 5 stopped after 3 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:182 ~ test7[1d05]::case_28) | CC: 3 | Nodes: 8 | Edges: 9
13:08:42|-|: Total Time of DefId(0:182 ~ test7[1d05]::case_28):       49.08µs
13:08:42|-|: DefId(0:182 ~ test7[1d05]::case_28) contains SCC 1 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:184 ~ test7[1d05]::case_29) | CC: 4 | Nodes: 12 | Edges: 14
13:08:42|-|: Total Time of DefId(0:184 ~ test7[1d05]::case_29):       61.79µs
13:08:42|-|: DefId(0:184 ~ test7[1d05]::case_29) contains SCC 7 stopped after 2 splicing iterations in depth 1.
13:08:42|-|: [STATS] Function: DefId(0:186 ~ test7[1d05]::case_30) | CC: 6 | Nodes: 19 | Edges: 23
13:08:42|-|: Total Time of DefId(0:186 ~ test7[1d05]::case_30):       447.08µs
13:08:42|-|: DefId(0:186 ~ test7[1d05]::case_30) contains SCC 1 stopped after 5 splicing iterations in depth 2.
"""

if __name__ == "__main__":
    # parse_and_aggregate(raw_log)
    parse_and_analyze(raw_log)