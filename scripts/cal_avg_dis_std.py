import re

log_data1 = """
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:4 ~ test5[dd47]::scc_topo_case_1):       362.46µs
17:33:51|-|: 1. Decomposition: 35.79µs
17:33:51|-|: 2. Constraint:    9.73µs
17:33:51|-|: 3. Path Synthesis:124.00µs
17:33:51|-|: 4. Alias Comp:    132.47µs
17:33:51|-|: 5. Traversal/Misc:60.46µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:6 ~ test5[dd47]::scc_topo_case_2):       44.75µs
17:33:51|-|: 1. Decomposition: 7.33µs
17:33:51|-|: 2. Constraint:    582.00ns
17:33:51|-|: 3. Path Synthesis:17.38µs
17:33:51|-|: 4. Alias Comp:    11.96µs
17:33:51|-|: 5. Traversal/Misc:7.50µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:8 ~ test5[dd47]::scc_topo_case_3):       866.92µs
17:33:51|-|: 1. Decomposition: 19.63µs
17:33:51|-|: 2. Constraint:    26.84µs
17:33:51|-|: 3. Path Synthesis:409.96µs
17:33:51|-|: 4. Alias Comp:    358.99µs
17:33:51|-|: 5. Traversal/Misc:51.50µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:10 ~ test5[dd47]::scc_topo_case_4):       97.13µs
17:33:51|-|: 1. Decomposition: 10.54µs
17:33:51|-|: 2. Constraint:    2.25µs
17:33:51|-|: 3. Path Synthesis:31.54µs
17:33:51|-|: 4. Alias Comp:    33.80µs
17:33:51|-|: 5. Traversal/Misc:19.00µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:12 ~ test5[dd47]::scc_topo_case_5):       41.08µs
17:33:51|-|: 1. Decomposition: 5.25µs
17:33:51|-|: 2. Constraint:    1.13µs
17:33:51|-|: 3. Path Synthesis:10.12µs
17:33:51|-|: 4. Alias Comp:    12.76µs
17:33:51|-|: 5. Traversal/Misc:11.83µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:14 ~ test5[dd47]::scc_topo_case_6):       124.63µs
17:33:51|-|: 1. Decomposition: 11.92µs
17:33:51|-|: 2. Constraint:    2.92µs
17:33:51|-|: 3. Path Synthesis:26.75µs
17:33:51|-|: 4. Alias Comp:    41.87µs
17:33:51|-|: 5. Traversal/Misc:41.17µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:16 ~ test5[dd47]::scc_topo_case_7):       82.92µs
17:33:51|-|: 1. Decomposition: 12.67µs
17:33:51|-|: 2. Constraint:    1.33µs
17:33:51|-|: 3. Path Synthesis:27.66µs
17:33:51|-|: 4. Alias Comp:    23.17µs
17:33:51|-|: 5. Traversal/Misc:18.08µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:18 ~ test5[dd47]::scc_topo_case_8):       564.33µs
17:33:51|-|: 1. Decomposition: 12.96µs
17:33:51|-|: 2. Constraint:    17.33µs
17:33:51|-|: 3. Path Synthesis:240.54µs
17:33:51|-|: 4. Alias Comp:    243.09µs
17:33:51|-|: 5. Traversal/Misc:50.42µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:20 ~ test5[dd47]::scc_topo_case_9):       100.58µs
17:33:51|-|: 1. Decomposition: 11.75µs
17:33:51|-|: 2. Constraint:    1.46µs
17:33:51|-|: 3. Path Synthesis:44.71µs
17:33:51|-|: 4. Alias Comp:    29.04µs
17:33:51|-|: 5. Traversal/Misc:13.62µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:22 ~ test5[dd47]::scc_topo_case_10):       37.38µs
17:33:51|-|: 1. Decomposition: 6.00µs
17:33:51|-|: 2. Constraint:    666.00ns
17:33:51|-|: 3. Path Synthesis:3.54µs
17:33:51|-|: 4. Alias Comp:    11.58µs
17:33:51|-|: 5. Traversal/Misc:15.58µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:24 ~ test5[dd47]::scc_topo_case_11):       78.88µs
17:33:51|-|: 1. Decomposition: 5.96µs
17:33:51|-|: 2. Constraint:    832.00ns
17:33:51|-|: 3. Path Synthesis:3.83µs
17:33:51|-|: 4. Alias Comp:    26.29µs
17:33:51|-|: 5. Traversal/Misc:41.96µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:26 ~ test5[dd47]::scc_topo_case_12):       86.88µs
17:33:51|-|: 1. Decomposition: 8.50µs
17:33:51|-|: 2. Constraint:    2.09µs
17:33:51|-|: 3. Path Synthesis:9.00µs
17:33:51|-|: 4. Alias Comp:    27.66µs
17:33:51|-|: 5. Traversal/Misc:39.63µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:28 ~ test5[dd47]::scc_topo_case_13):       64.67µs
17:33:51|-|: 1. Decomposition: 38.83µs
17:33:51|-|: 2. Constraint:    458.00ns
17:33:51|-|: 3. Path Synthesis:3.21µs
17:33:51|-|: 4. Alias Comp:    9.38µs
17:33:51|-|: 5. Traversal/Misc:12.79µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:30 ~ test5[dd47]::scc_topo_case_14):       34.13µs
17:33:51|-|: 1. Decomposition: 5.38µs
17:33:51|-|: 2. Constraint:    417.00ns
17:33:51|-|: 3. Path Synthesis:3.21µs
17:33:51|-|: 4. Alias Comp:    10.38µs
17:33:51|-|: 5. Traversal/Misc:14.75µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:32 ~ test5[dd47]::scc_topo_case_15):       80.08µs
17:33:51|-|: 1. Decomposition: 7.08µs
17:33:51|-|: 2. Constraint:    1.38µs
17:33:51|-|: 3. Path Synthesis:8.71µs
17:33:51|-|: 4. Alias Comp:    28.21µs
17:33:51|-|: 5. Traversal/Misc:34.71µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:34 ~ test5[dd47]::scc_topo_case_16):       17.79µs
17:33:51|-|: 1. Decomposition: 2.71µs
17:33:51|-|: 2. Constraint:    208.00ns
17:33:51|-|: 3. Path Synthesis:0.00ns
17:33:51|-|: 4. Alias Comp:    6.25µs
17:33:51|-|: 5. Traversal/Misc:8.63µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:36 ~ test5[dd47]::scc_topo_case_17):       64.21µs
17:33:51|-|: 1. Decomposition: 6.50µs
17:33:51|-|: 2. Constraint:    956.00ns
17:33:51|-|: 3. Path Synthesis:6.67µs
17:33:51|-|: 4. Alias Comp:    23.21µs
17:33:51|-|: 5. Traversal/Misc:26.87µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:38 ~ test5[dd47]::scc_topo_case_18):       51.54µs
17:33:51|-|: 1. Decomposition: 5.38µs
17:33:51|-|: 2. Constraint:    789.00ns
17:33:51|-|: 3. Path Synthesis:5.83µs
17:33:51|-|: 4. Alias Comp:    17.96µs
17:33:51|-|: 5. Traversal/Misc:21.58µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:40 ~ test5[dd47]::scc_topo_case_19):       217.21µs
17:33:51|-|: 1. Decomposition: 77.42µs
17:33:51|-|: 2. Constraint:    4.46µs
17:33:51|-|: 3. Path Synthesis:26.75µs
17:33:51|-|: 4. Alias Comp:    55.37µs
17:33:51|-|: 5. Traversal/Misc:53.20µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:42 ~ test5[dd47]::scc_topo_case_20):       91.08µs
17:33:51|-|: 1. Decomposition: 12.63µs
17:33:51|-|: 2. Constraint:    2.71µs
17:33:51|-|: 3. Path Synthesis:15.71µs
17:33:51|-|: 4. Alias Comp:    32.33µs
17:33:51|-|: 5. Traversal/Misc:27.71µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:44 ~ test5[dd47]::scc_topo_case_21):       359.42µs
17:33:51|-|: 1. Decomposition: 15.04µs
17:33:51|-|: 2. Constraint:    8.92µs
17:33:51|-|: 3. Path Synthesis:63.49µs
17:33:51|-|: 4. Alias Comp:    121.17µs
17:33:51|-|: 5. Traversal/Misc:150.79µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:46 ~ test5[dd47]::scc_topo_case_22):       76.79µs
17:33:51|-|: 1. Decomposition: 9.88µs
17:33:51|-|: 2. Constraint:    961.00ns
17:33:51|-|: 3. Path Synthesis:7.96µs
17:33:51|-|: 4. Alias Comp:    23.46µs
17:33:51|-|: 5. Traversal/Misc:34.54µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:48 ~ test5[dd47]::scc_topo_case_23):       75.58µs
17:33:51|-|: 1. Decomposition: 8.63µs
17:33:51|-|: 2. Constraint:    960.00ns
17:33:51|-|: 3. Path Synthesis:6.50µs
17:33:51|-|: 4. Alias Comp:    21.04µs
17:33:51|-|: 5. Traversal/Misc:38.45µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:50 ~ test5[dd47]::scc_topo_case_24):       397.75µs
17:33:51|-|: 1. Decomposition: 13.75µs
17:33:51|-|: 2. Constraint:    29.50µs
17:33:51|-|: 3. Path Synthesis:56.38µs
17:33:51|-|: 4. Alias Comp:    194.42µs
17:33:51|-|: 5. Traversal/Misc:103.71µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:52 ~ test5[dd47]::scc_topo_case_25):       1.28ms
17:33:51|-|: 1. Decomposition: 11.08µs
17:33:51|-|: 2. Constraint:    64.72µs
17:33:51|-|: 3. Path Synthesis:314.53µs
17:33:51|-|: 4. Alias Comp:    678.75µs
17:33:51|-|: 5. Traversal/Misc:213.43µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:54 ~ test5[dd47]::scc_topo_case_26):       370.67µs
17:33:51|-|: 1. Decomposition: 9.08µs
17:33:51|-|: 2. Constraint:    14.63µs
17:33:51|-|: 3. Path Synthesis:79.24µs
17:33:51|-|: 4. Alias Comp:    169.17µs
17:33:51|-|: 5. Traversal/Misc:98.54µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:56 ~ test5[dd47]::scc_topo_case_27):       452.92µs
17:33:51|-|: 1. Decomposition: 11.33µs
17:33:51|-|: 2. Constraint:    22.59µs
17:33:51|-|: 3. Path Synthesis:111.71µs
17:33:51|-|: 4. Alias Comp:    228.96µs
17:33:51|-|: 5. Traversal/Misc:78.34µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:58 ~ test5[dd47]::scc_topo_case_28):       774.92µs
17:33:51|-|: 1. Decomposition: 12.04µs
17:33:51|-|: 2. Constraint:    48.00µs
17:33:51|-|: 3. Path Synthesis:198.14µs
17:33:51|-|: 4. Alias Comp:    398.61µs
17:33:51|-|: 5. Traversal/Misc:118.12µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:60 ~ test5[dd47]::scc_topo_case_29):       78.67µs
17:33:51|-|: 1. Decomposition: 8.29µs
17:33:51|-|: 2. Constraint:    1.71µs
17:33:51|-|: 3. Path Synthesis:9.04µs
17:33:51|-|: 4. Alias Comp:    27.37µs
17:33:51|-|: 5. Traversal/Misc:32.25µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:62 ~ test5[dd47]::scc_topo_case_30):       319.08µs
17:33:51|-|: 1. Decomposition: 7.63µs
17:33:51|-|: 2. Constraint:    15.88µs
17:33:51|-|: 3. Path Synthesis:82.02µs
17:33:51|-|: 4. Alias Comp:    165.27µs
17:33:51|-|: 5. Traversal/Misc:48.29µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:64 ~ test5[dd47]::random_test1):       20.88µs
17:33:51|-|: 1. Decomposition: 3.08µs
17:33:51|-|: 2. Constraint:    125.00ns
17:33:51|-|: 3. Path Synthesis:0.00ns
17:33:51|-|: 4. Alias Comp:    5.13µs
17:33:51|-|: 5. Traversal/Misc:12.54µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:87 ~ test5[dd47]::random_test2):       2.71µs
17:33:51|-|: 1. Decomposition: 1.00µs
17:33:51|-|: 2. Constraint:    0.00ns
17:33:51|-|: 3. Path Synthesis:0.00ns
17:33:51|-|: 4. Alias Comp:    1.00µs
17:33:51|-|: 5. Traversal/Misc:708.00ns
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:88 ~ test5[dd47]::random_int_test2):       2.54µs
17:33:51|-|: 1. Decomposition: 1.00µs
17:33:51|-|: 2. Constraint:    0.00ns
17:33:51|-|: 3. Path Synthesis:0.00ns
17:33:51|-|: 4. Alias Comp:    917.00ns
17:33:51|-|: 5. Traversal/Misc:624.00ns
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:89 ~ test5[dd47]::random_test3):       2.13µs
17:33:51|-|: 1. Decomposition: 666.00ns
17:33:51|-|: 2. Constraint:    0.00ns
17:33:51|-|: 3. Path Synthesis:0.00ns
17:33:51|-|: 4. Alias Comp:    833.00ns
17:33:51|-|: 5. Traversal/Misc:626.00ns
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:90 ~ test5[dd47]::random_bool_test4):       2.33µs
17:33:51|-|: 1. Decomposition: 916.00ns
17:33:51|-|: 2. Constraint:    0.00ns
17:33:51|-|: 3. Path Synthesis:0.00ns
17:33:51|-|: 4. Alias Comp:    875.00ns
17:33:51|-|: 5. Traversal/Misc:542.00ns
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:91 ~ test5[dd47]::test_2):       28.71µs
17:33:51|-|: 1. Decomposition: 4.29µs
17:33:51|-|: 2. Constraint:    375.00ns
17:33:51|-|: 3. Path Synthesis:4.00µs
17:33:51|-|: 4. Alias Comp:    9.96µs
17:33:51|-|: 5. Traversal/Misc:10.09µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:93 ~ test5[dd47]::test_4):       69.25µs
17:33:51|-|: 1. Decomposition: 8.88µs
17:33:51|-|: 2. Constraint:    1.04µs
17:33:51|-|: 3. Path Synthesis:24.41µs
17:33:51|-|: 4. Alias Comp:    22.38µs
17:33:51|-|: 5. Traversal/Misc:12.54µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:95 ~ test5[dd47]::test_5):       89.58µs
17:33:51|-|: 1. Decomposition: 7.79µs
17:33:51|-|: 2. Constraint:    1.17µs
17:33:51|-|: 3. Path Synthesis:7.42µs
17:33:51|-|: 4. Alias Comp:    23.66µs
17:33:51|-|: 5. Traversal/Misc:49.54µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:97 ~ test5[dd47]::test_9):       4.83µs
17:33:51|-|: 1. Decomposition: 916.00ns
17:33:51|-|: 2. Constraint:    0.00ns
17:33:51|-|: 3. Path Synthesis:0.00ns
17:33:51|-|: 4. Alias Comp:    3.08µs
17:33:51|-|: 5. Traversal/Misc:834.00ns
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:99 ~ test5[dd47]::test_19_max_depth):       388.38µs
17:33:51|-|: 1. Decomposition: 34.33µs
17:33:51|-|: 2. Constraint:    4.71µs
17:33:51|-|: 3. Path Synthesis:222.80µs
17:33:51|-|: 4. Alias Comp:    94.79µs
17:33:51|-|: 5. Traversal/Misc:31.75µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:101 ~ test5[dd47]::case_25_2):       26.54µs
17:33:51|-|: 1. Decomposition: 4.13µs
17:33:51|-|: 2. Constraint:    375.00ns
17:33:51|-|: 3. Path Synthesis:4.00µs
17:33:51|-|: 4. Alias Comp:    9.50µs
17:33:51|-|: 5. Traversal/Misc:8.54µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:104 ~ test5[dd47]::case_1):       43.63µs
17:33:51|-|: 1. Decomposition: 6.21µs
17:33:51|-|: 2. Constraint:    1.33µs
17:33:51|-|: 3. Path Synthesis:8.25µs
17:33:51|-|: 4. Alias Comp:    15.62µs
17:33:51|-|: 5. Traversal/Misc:12.21µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:106 ~ test5[dd47]::case_2):       67.08µs
17:33:51|-|: 1. Decomposition: 6.54µs
17:33:51|-|: 2. Constraint:    1.29µs
17:33:51|-|: 3. Path Synthesis:8.42µs
17:33:51|-|: 4. Alias Comp:    22.79µs
17:33:51|-|: 5. Traversal/Misc:28.04µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:108 ~ test5[dd47]::case_3):       59.25µs
17:33:51|-|: 1. Decomposition: 8.54µs
17:33:51|-|: 2. Constraint:    792.00ns
17:33:51|-|: 3. Path Synthesis:6.00µs
17:33:51|-|: 4. Alias Comp:    15.92µs
17:33:51|-|: 5. Traversal/Misc:28.00µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:110 ~ test5[dd47]::case_4):       47.96µs
17:33:51|-|: 1. Decomposition: 8.00µs
17:33:51|-|: 2. Constraint:    1.00µs
17:33:51|-|: 3. Path Synthesis:20.92µs
17:33:51|-|: 4. Alias Comp:    11.62µs
17:33:51|-|: 5. Traversal/Misc:6.42µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:112 ~ test5[dd47]::case_5):       66.46µs
17:33:51|-|: 1. Decomposition: 7.00µs
17:33:51|-|: 2. Constraint:    1.04µs
17:33:51|-|: 3. Path Synthesis:6.71µs
17:33:51|-|: 4. Alias Comp:    23.08µs
17:33:51|-|: 5. Traversal/Misc:28.63µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:114 ~ test5[dd47]::case_6):       20.42µs
17:33:51|-|: 1. Decomposition: 4.38µs
17:33:51|-|: 2. Constraint:    586.00ns
17:33:51|-|: 3. Path Synthesis:4.38µs
17:33:51|-|: 4. Alias Comp:    5.25µs
17:33:51|-|: 5. Traversal/Misc:5.83µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:116 ~ test5[dd47]::case_7):       98.88µs
17:33:51|-|: 1. Decomposition: 11.67µs
17:33:51|-|: 2. Constraint:    1.87µs
17:33:51|-|: 3. Path Synthesis:31.08µs
17:33:51|-|: 4. Alias Comp:    28.42µs
17:33:51|-|: 5. Traversal/Misc:25.83µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:118 ~ test5[dd47]::case_8):       23.38µs
17:33:51|-|: 1. Decomposition: 3.17µs
17:33:51|-|: 2. Constraint:    418.00ns
17:33:51|-|: 3. Path Synthesis:3.17µs
17:33:51|-|: 4. Alias Comp:    7.96µs
17:33:51|-|: 5. Traversal/Misc:8.67µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:120 ~ test5[dd47]::case_9):       300.04µs
17:33:51|-|: 1. Decomposition: 21.29µs
17:33:51|-|: 2. Constraint:    6.96µs
17:33:51|-|: 3. Path Synthesis:149.87µs
17:33:51|-|: 4. Alias Comp:    94.67µs
17:33:51|-|: 5. Traversal/Misc:27.25µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:122 ~ test5[dd47]::case_10):       4.46µs
17:33:51|-|: 1. Decomposition: 792.00ns
17:33:51|-|: 2. Constraint:    0.00ns
17:33:51|-|: 3. Path Synthesis:0.00ns
17:33:51|-|: 4. Alias Comp:    2.88µs
17:33:51|-|: 5. Traversal/Misc:792.00ns
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:124 ~ test5[dd47]::case_11):       47.00µs
17:33:51|-|: 1. Decomposition: 7.83µs
17:33:51|-|: 2. Constraint:    665.00ns
17:33:51|-|: 3. Path Synthesis:20.75µs
17:33:51|-|: 4. Alias Comp:    11.42µs
17:33:51|-|: 5. Traversal/Misc:6.33µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:126 ~ test5[dd47]::case_12):       47.00µs
17:33:51|-|: 1. Decomposition: 7.04µs
17:33:51|-|: 2. Constraint:    750.00ns
17:33:51|-|: 3. Path Synthesis:20.88µs
17:33:51|-|: 4. Alias Comp:    12.08µs
17:33:51|-|: 5. Traversal/Misc:6.25µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:128 ~ test5[dd47]::case_13):       32.75µs
17:33:51|-|: 1. Decomposition: 5.13µs
17:33:51|-|: 2. Constraint:    460.00ns
17:33:51|-|: 3. Path Synthesis:3.46µs
17:33:51|-|: 4. Alias Comp:    9.33µs
17:33:51|-|: 5. Traversal/Misc:14.37µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:130 ~ test5[dd47]::case_14):       64.13µs
17:33:51|-|: 1. Decomposition: 6.08µs
17:33:51|-|: 2. Constraint:    960.00ns
17:33:51|-|: 3. Path Synthesis:6.83µs
17:33:51|-|: 4. Alias Comp:    22.42µs
17:33:51|-|: 5. Traversal/Misc:27.83µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:132 ~ test5[dd47]::case_15):       75.71µs
17:33:51|-|: 1. Decomposition: 7.33µs
17:33:51|-|: 2. Constraint:    667.00ns
17:33:51|-|: 3. Path Synthesis:4.71µs
17:33:51|-|: 4. Alias Comp:    21.75µs
17:33:51|-|: 5. Traversal/Misc:41.25µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:134 ~ test5[dd47]::case_16):       330.25µs
17:33:51|-|: 1. Decomposition: 7.17µs
17:33:51|-|: 2. Constraint:    17.13µs
17:33:51|-|: 3. Path Synthesis:80.75µs
17:33:51|-|: 4. Alias Comp:    169.66µs
17:33:51|-|: 5. Traversal/Misc:55.55µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:136 ~ test5[dd47]::case_17):       56.58µs
17:33:51|-|: 1. Decomposition: 5.50µs
17:33:51|-|: 2. Constraint:    2.13µs
17:33:51|-|: 3. Path Synthesis:11.54µs
17:33:51|-|: 4. Alias Comp:    23.21µs
17:33:51|-|: 5. Traversal/Misc:14.21µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:138 ~ test5[dd47]::case_18):       130.83µs
17:33:51|-|: 1. Decomposition: 7.00µs
17:33:51|-|: 2. Constraint:    5.79µs
17:33:51|-|: 3. Path Synthesis:31.96µs
17:33:51|-|: 4. Alias Comp:    60.38µs
17:33:51|-|: 5. Traversal/Misc:25.71µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:140 ~ test5[dd47]::case_19):       47.79µs
17:33:51|-|: 1. Decomposition: 6.46µs
17:33:51|-|: 2. Constraint:    1.21µs
17:33:51|-|: 3. Path Synthesis:8.75µs
17:33:51|-|: 4. Alias Comp:    17.54µs
17:33:51|-|: 5. Traversal/Misc:13.83µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:142 ~ test5[dd47]::case_20):       261.00µs
17:33:51|-|: 1. Decomposition: 10.88µs
17:33:51|-|: 2. Constraint:    7.01µs
17:33:51|-|: 3. Path Synthesis:104.37µs
17:33:51|-|: 4. Alias Comp:    111.71µs
17:33:51|-|: 5. Traversal/Misc:27.04µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:144 ~ test5[dd47]::case_21):       42.58µs
17:33:51|-|: 1. Decomposition: 5.67µs
17:33:51|-|: 2. Constraint:    501.00ns
17:33:51|-|: 3. Path Synthesis:2.37µs
17:33:51|-|: 4. Alias Comp:    11.46µs
17:33:51|-|: 5. Traversal/Misc:22.58µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:146 ~ test5[dd47]::case_22):       4.46ms
17:33:51|-|: 1. Decomposition: 13.17µs
17:33:51|-|: 2. Constraint:    297.81µs
17:33:51|-|: 3. Path Synthesis:1.07ms
17:33:51|-|: 4. Alias Comp:    2.59ms
17:33:51|-|: 5. Traversal/Misc:485.24µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:148 ~ test5[dd47]::case_23):       326.33µs
17:33:51|-|: 1. Decomposition: 9.92µs
17:33:51|-|: 2. Constraint:    6.30µs
17:33:51|-|: 3. Path Synthesis:56.92µs
17:33:51|-|: 4. Alias Comp:    106.83µs
17:33:51|-|: 5. Traversal/Misc:146.37µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:150 ~ test5[dd47]::case_24):       245.00µs
17:33:51|-|: 1. Decomposition: 8.83µs
17:33:51|-|: 2. Constraint:    9.95µs
17:33:51|-|: 3. Path Synthesis:56.77µs
17:33:51|-|: 4. Alias Comp:    117.94µs
17:33:51|-|: 5. Traversal/Misc:51.50µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:152 ~ test5[dd47]::case_26):       29.33µs
17:33:51|-|: 1. Decomposition: 4.08µs
17:33:51|-|: 2. Constraint:    419.00ns
17:33:51|-|: 3. Path Synthesis:4.04µs
17:33:51|-|: 4. Alias Comp:    11.50µs
17:33:51|-|: 5. Traversal/Misc:9.29µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:154 ~ test5[dd47]::case_27):       64.58µs
17:33:51|-|: 1. Decomposition: 14.00µs
17:33:51|-|: 2. Constraint:    794.00ns
17:33:51|-|: 3. Path Synthesis:4.58µs
17:33:51|-|: 4. Alias Comp:    16.96µs
17:33:51|-|: 5. Traversal/Misc:28.25µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:156 ~ test5[dd47]::case_28):       46.50µs
17:33:51|-|: 1. Decomposition: 5.21µs
17:33:51|-|: 2. Constraint:    914.00ns
17:33:51|-|: 3. Path Synthesis:5.75µs
17:33:51|-|: 4. Alias Comp:    16.88µs
17:33:51|-|: 5. Traversal/Misc:17.75µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:158 ~ test5[dd47]::case_29):       35.08µs
17:33:51|-|: 1. Decomposition: 6.21µs
17:33:51|-|: 2. Constraint:    501.00ns
17:33:51|-|: 3. Path Synthesis:4.67µs
17:33:51|-|: 4. Alias Comp:    9.04µs
17:33:51|-|: 5. Traversal/Misc:14.66µs
17:33:51|-|: ===========================
17:33:51|-|: === Performance Profiling ===
17:33:51|-|: Total Time of DefId(0:160 ~ test5[dd47]::case_30):       137.08µs
17:33:51|-|: 1. Decomposition: 10.21µs
17:33:51|-|: 2. Constraint:    2.33µs
17:33:51|-|: 3. Path Synthesis:11.34µs
17:33:51|-|: 4. Alias Comp:    44.00µs
17:33:51|-|: 5. Traversal/Misc:69.21µs
17:33:51|-|: ===========================
"""

log_data2 = """
17:43:15|-|: Total Time of DefId(0:15 ~ test6[80bb]::scc_path_case_1):       1.28ms
17:43:15|-|: 1. Decomposition: 235.50µs
17:43:15|-|: 2. Constraint:    22.33µs
17:43:15|-|: 3. Path Synthesis:282.71µs
17:43:15|-|: 4. Alias Comp:    489.80µs
17:43:15|-|: 5. Traversal/Misc:249.92µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:17 ~ test6[80bb]::scc_path_case_2):       341.50µs
17:43:15|-|: 1. Decomposition: 13.63µs
17:43:15|-|: 2. Constraint:    10.49µs
17:43:15|-|: 3. Path Synthesis:142.34µs
17:43:15|-|: 4. Alias Comp:    141.76µs
17:43:15|-|: 5. Traversal/Misc:33.29µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:19 ~ test6[80bb]::scc_path_case_3):       826.13µs
17:43:15|-|: 1. Decomposition: 18.71µs
17:43:15|-|: 2. Constraint:    22.51µs
17:43:15|-|: 3. Path Synthesis:401.90µs
17:43:15|-|: 4. Alias Comp:    328.60µs
17:43:15|-|: 5. Traversal/Misc:54.41µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:21 ~ test6[80bb]::scc_path_case_4):       140.33µs
17:43:15|-|: 1. Decomposition: 10.63µs
17:43:15|-|: 2. Constraint:    3.00µs
17:43:15|-|: 3. Path Synthesis:36.45µs
17:43:15|-|: 4. Alias Comp:    51.72µs
17:43:15|-|: 5. Traversal/Misc:38.54µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:23 ~ test6[80bb]::scc_path_case_5):       1.01ms
17:43:15|-|: 1. Decomposition: 14.25µs
17:43:15|-|: 2. Constraint:    33.63µs
17:43:15|-|: 3. Path Synthesis:377.81µs
17:43:15|-|: 4. Alias Comp:    500.11µs
17:43:15|-|: 5. Traversal/Misc:84.66µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:25 ~ test6[80bb]::scc_path_case_6):       502.54µs
17:43:15|-|: 1. Decomposition: 17.50µs
17:43:15|-|: 2. Constraint:    13.49µs
17:43:15|-|: 3. Path Synthesis:140.88µs
17:43:15|-|: 4. Alias Comp:    232.34µs
17:43:15|-|: 5. Traversal/Misc:98.33µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:27 ~ test6[80bb]::scc_path_case_7):       103.29µs
17:43:15|-|: 1. Decomposition: 7.50µs
17:43:15|-|: 2. Constraint:    1.33µs
17:43:15|-|: 3. Path Synthesis:7.33µs
17:43:15|-|: 4. Alias Comp:    34.88µs
17:43:15|-|: 5. Traversal/Misc:52.25µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:29 ~ test6[80bb]::scc_path_case_8):       106.25µs
17:43:15|-|: 1. Decomposition: 8.71µs
17:43:15|-|: 2. Constraint:    4.83µs
17:43:15|-|: 3. Path Synthesis:25.08µs
17:43:15|-|: 4. Alias Comp:    45.42µs
17:43:15|-|: 5. Traversal/Misc:22.21µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:31 ~ test6[80bb]::scc_path_case_9):       699.50µs
17:43:15|-|: 1. Decomposition: 19.67µs
17:43:15|-|: 2. Constraint:    26.12µs
17:43:15|-|: 3. Path Synthesis:351.29µs
17:43:15|-|: 4. Alias Comp:    268.25µs
17:43:15|-|: 5. Traversal/Misc:34.17µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:33 ~ test6[80bb]::scc_path_case_10):       53.25µs
17:43:15|-|: 1. Decomposition: 3.58µs
17:43:15|-|: 2. Constraint:    791.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    20.54µs
17:43:15|-|: 5. Traversal/Misc:28.33µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:35 ~ test6[80bb]::scc_path_case_11):       82.75µs
17:43:15|-|: 1. Decomposition: 5.38µs
17:43:15|-|: 2. Constraint:    709.00ns
17:43:15|-|: 3. Path Synthesis:4.42µs
17:43:15|-|: 4. Alias Comp:    28.00µs
17:43:15|-|: 5. Traversal/Misc:44.25µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:37 ~ test6[80bb]::scc_path_case_12):       113.88µs
17:43:15|-|: 1. Decomposition: 5.54µs
17:43:15|-|: 2. Constraint:    1.17µs
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    28.41µs
17:43:15|-|: 5. Traversal/Misc:78.75µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:39 ~ test6[80bb]::scc_path_case_13):       17.42µs
17:43:15|-|: 1. Decomposition: 2.13µs
17:43:15|-|: 2. Constraint:    292.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    7.96µs
17:43:15|-|: 5. Traversal/Misc:7.04µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:41 ~ test6[80bb]::scc_path_case_14):       19.75µs
17:43:15|-|: 1. Decomposition: 3.38µs
17:43:15|-|: 2. Constraint:    333.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    6.42µs
17:43:15|-|: 5. Traversal/Misc:9.63µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:43 ~ test6[80bb]::scc_path_case_15):       47.63µs
17:43:15|-|: 1. Decomposition: 3.08µs
17:43:15|-|: 2. Constraint:    542.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    18.58µs
17:43:15|-|: 5. Traversal/Misc:25.42µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:45 ~ test6[80bb]::scc_path_case_16):       13.04µs
17:43:15|-|: 1. Decomposition: 1.75µs
17:43:15|-|: 2. Constraint:    250.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    4.79µs
17:43:15|-|: 5. Traversal/Misc:6.25µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:47 ~ test6[80bb]::scc_path_case_17):       57.92µs
17:43:15|-|: 1. Decomposition: 4.67µs
17:43:15|-|: 2. Constraint:    918.00ns
17:43:15|-|: 3. Path Synthesis:5.42µs
17:43:15|-|: 4. Alias Comp:    23.25µs
17:43:15|-|: 5. Traversal/Misc:23.67µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:49 ~ test6[80bb]::scc_path_case_18):       35.63µs
17:43:15|-|: 1. Decomposition: 2.13µs
17:43:15|-|: 2. Constraint:    500.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    13.71µs
17:43:15|-|: 5. Traversal/Misc:19.29µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:51 ~ test6[80bb]::scc_path_case_19):       43.88µs
17:43:15|-|: 1. Decomposition: 2.88µs
17:43:15|-|: 2. Constraint:    709.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    14.08µs
17:43:15|-|: 5. Traversal/Misc:26.21µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:53 ~ test6[80bb]::scc_path_case_20):       36.71µs
17:43:15|-|: 1. Decomposition: 2.63µs
17:43:15|-|: 2. Constraint:    543.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    13.21µs
17:43:15|-|: 5. Traversal/Misc:20.33µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:55 ~ test6[80bb]::scc_path_case_21):       96.33µs
17:43:15|-|: 1. Decomposition: 3.88µs
17:43:15|-|: 2. Constraint:    1.34µs
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    28.96µs
17:43:15|-|: 5. Traversal/Misc:62.16µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:57 ~ test6[80bb]::scc_path_case_22):       18.67µs
17:43:15|-|: 1. Decomposition: 1.58µs
17:43:15|-|: 2. Constraint:    417.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    8.17µs
17:43:15|-|: 5. Traversal/Misc:8.50µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:59 ~ test6[80bb]::scc_path_case_23):       22.63µs
17:43:15|-|: 1. Decomposition: 2.17µs
17:43:15|-|: 2. Constraint:    458.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    9.38µs
17:43:15|-|: 5. Traversal/Misc:10.63µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:61 ~ test6[80bb]::scc_path_case_24):       72.71µs
17:43:15|-|: 1. Decomposition: 3.50µs
17:43:15|-|: 2. Constraint:    956.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    22.54µs
17:43:15|-|: 5. Traversal/Misc:45.71µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:63 ~ test6[80bb]::scc_path_case_25):       45.96µs
17:43:15|-|: 1. Decomposition: 2.58µs
17:43:15|-|: 2. Constraint:    750.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    18.92µs
17:43:15|-|: 5. Traversal/Misc:23.71µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:65 ~ test6[80bb]::scc_path_case_26):       37.67µs
17:43:15|-|: 1. Decomposition: 2.46µs
17:43:15|-|: 2. Constraint:    500.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    14.75µs
17:43:15|-|: 5. Traversal/Misc:19.96µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:67 ~ test6[80bb]::scc_path_case_27):       58.83µs
17:43:15|-|: 1. Decomposition: 3.33µs
17:43:15|-|: 2. Constraint:    835.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    18.46µs
17:43:15|-|: 5. Traversal/Misc:36.21µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:69 ~ test6[80bb]::scc_path_case_28):       63.25µs
17:43:15|-|: 1. Decomposition: 3.17µs
17:43:15|-|: 2. Constraint:    750.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    20.38µs
17:43:15|-|: 5. Traversal/Misc:38.95µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:71 ~ test6[80bb]::scc_path_case_29):       71.88µs
17:43:15|-|: 1. Decomposition: 4.50µs
17:43:15|-|: 2. Constraint:    708.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    22.63µs
17:43:15|-|: 5. Traversal/Misc:44.04µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:73 ~ test6[80bb]::scc_path_case_30):       47.42µs
17:43:15|-|: 1. Decomposition: 2.71µs
17:43:15|-|: 2. Constraint:    708.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    21.58µs
17:43:15|-|: 5. Traversal/Misc:22.42µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:75 ~ test6[80bb]::random_test1):       22.54µs
17:43:15|-|: 1. Decomposition: 3.21µs
17:43:15|-|: 2. Constraint:    124.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    5.38µs
17:43:15|-|: 5. Traversal/Misc:13.83µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:98 ~ test6[80bb]::random_test2):       2.50µs
17:43:15|-|: 1. Decomposition: 875.00ns
17:43:15|-|: 2. Constraint:    0.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    916.00ns
17:43:15|-|: 5. Traversal/Misc:709.00ns
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:99 ~ test6[80bb]::random_int_test2):       1.83µs
17:43:15|-|: 1. Decomposition: 666.00ns
17:43:15|-|: 2. Constraint:    0.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    667.00ns
17:43:15|-|: 5. Traversal/Misc:500.00ns
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:100 ~ test6[80bb]::random_test3):       1.88µs
17:43:15|-|: 1. Decomposition: 666.00ns
17:43:15|-|: 2. Constraint:    0.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    708.00ns
17:43:15|-|: 5. Traversal/Misc:501.00ns
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:101 ~ test6[80bb]::random_bool_test4):       1.54µs
17:43:15|-|: 1. Decomposition: 625.00ns
17:43:15|-|: 2. Constraint:    0.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    500.00ns
17:43:15|-|: 5. Traversal/Misc:416.00ns
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:102 ~ test6[80bb]::test2):       96.54µs
17:43:15|-|: 1. Decomposition: 6.96µs
17:43:15|-|: 2. Constraint:    3.62µs
17:43:15|-|: 3. Path Synthesis:18.66µs
17:43:15|-|: 4. Alias Comp:    42.55µs
17:43:15|-|: 5. Traversal/Misc:24.75µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:104 ~ test6[80bb]::test3):       463.83µs
17:43:15|-|: 1. Decomposition: 17.88µs
17:43:15|-|: 2. Constraint:    11.16µs
17:43:15|-|: 3. Path Synthesis:119.33µs
17:43:15|-|: 4. Alias Comp:    203.80µs
17:43:15|-|: 5. Traversal/Misc:111.66µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:105 ~ test6[80bb]::test_demo):       351.17µs
17:43:15|-|: 1. Decomposition: 13.67µs
17:43:15|-|: 2. Constraint:    9.63µs
17:43:15|-|: 3. Path Synthesis:107.75µs
17:43:15|-|: 4. Alias Comp:    141.75µs
17:43:15|-|: 5. Traversal/Misc:78.37µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:106 ~ test6[80bb]::test_nested_scc):       256.71µs
17:43:15|-|: 1. Decomposition: 12.88µs
17:43:15|-|: 2. Constraint:    6.20µs
17:43:15|-|: 3. Path Synthesis:78.88µs
17:43:15|-|: 4. Alias Comp:    89.29µs
17:43:15|-|: 5. Traversal/Misc:69.46µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:108 ~ test6[80bb]::test4):       1.58ms
17:43:15|-|: 1. Decomposition: 19.63µs
17:43:15|-|: 2. Constraint:    43.62µs
17:43:15|-|: 3. Path Synthesis:483.84µs
17:43:15|-|: 4. Alias Comp:    747.45µs
17:43:15|-|: 5. Traversal/Misc:289.47µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:109 ~ test6[80bb]::case_a1):       122.08µs
17:43:15|-|: 1. Decomposition: 8.29µs
17:43:15|-|: 2. Constraint:    4.20µs
17:43:15|-|: 3. Path Synthesis:25.97µs
17:43:15|-|: 4. Alias Comp:    58.79µs
17:43:15|-|: 5. Traversal/Misc:24.83µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:111 ~ test6[80bb]::case_a2):       323.96µs
17:43:15|-|: 1. Decomposition: 12.58µs
17:43:15|-|: 2. Constraint:    6.88µs
17:43:15|-|: 3. Path Synthesis:120.27µs
17:43:15|-|: 4. Alias Comp:    145.06µs
17:43:15|-|: 5. Traversal/Misc:39.17µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:113 ~ test6[80bb]::case_constraint_number):       138.17µs
17:43:15|-|: 1. Decomposition: 7.08µs
17:43:15|-|: 2. Constraint:    7.58µs
17:43:15|-|: 3. Path Synthesis:34.17µs
17:43:15|-|: 4. Alias Comp:    63.88µs
17:43:15|-|: 5. Traversal/Misc:25.46µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:115 ~ test6[80bb]::case_cross_path_contamination):       49.83µs
17:43:15|-|: 1. Decomposition: 4.83µs
17:43:15|-|: 2. Constraint:    751.00ns
17:43:15|-|: 3. Path Synthesis:5.46µs
17:43:15|-|: 4. Alias Comp:    17.25µs
17:43:15|-|: 5. Traversal/Misc:21.54µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:117 ~ test6[80bb]::test_1):       43.29µs
17:43:15|-|: 1. Decomposition: 3.00µs
17:43:15|-|: 2. Constraint:    793.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    13.87µs
17:43:15|-|: 5. Traversal/Misc:25.63µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:119 ~ test6[80bb]::test_3):       69.71µs
17:43:15|-|: 1. Decomposition: 6.13µs
17:43:15|-|: 2. Constraint:    2.33µs
17:43:15|-|: 3. Path Synthesis:10.04µs
17:43:15|-|: 4. Alias Comp:    25.34µs
17:43:15|-|: 5. Traversal/Misc:25.87µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:121 ~ test6[80bb]::test_16_2):       158.83µs
17:43:15|-|: 1. Decomposition: 9.88µs
17:43:15|-|: 2. Constraint:    4.17µs
17:43:15|-|: 3. Path Synthesis:24.92µs
17:43:15|-|: 4. Alias Comp:    64.87µs
17:43:15|-|: 5. Traversal/Misc:55.00µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:123 ~ test6[80bb]::test_7_2):       45.50µs
17:43:15|-|: 1. Decomposition: 3.63µs
17:43:15|-|: 2. Constraint:    750.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    16.08µs
17:43:15|-|: 5. Traversal/Misc:25.04µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:125 ~ test6[80bb]::test_8):       70.21µs
17:43:15|-|: 1. Decomposition: 5.08µs
17:43:15|-|: 2. Constraint:    1.92µs
17:43:15|-|: 3. Path Synthesis:15.37µs
17:43:15|-|: 4. Alias Comp:    30.17µs
17:43:15|-|: 5. Traversal/Misc:17.67µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:127 ~ test6[80bb]::test_10_2):       43.08µs
17:43:15|-|: 1. Decomposition: 4.79µs
17:43:15|-|: 2. Constraint:    1.33µs
17:43:15|-|: 3. Path Synthesis:8.30µs
17:43:15|-|: 4. Alias Comp:    16.17µs
17:43:15|-|: 5. Traversal/Misc:12.50µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:129 ~ test6[80bb]::test_11_2):       18.63µs
17:43:15|-|: 1. Decomposition: 1.71µs
17:43:15|-|: 2. Constraint:    250.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    7.75µs
17:43:15|-|: 5. Traversal/Misc:8.92µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:131 ~ test6[80bb]::test_12):       54.00µs
17:43:15|-|: 1. Decomposition: 5.08µs
17:43:15|-|: 2. Constraint:    1.67µs
17:43:15|-|: 3. Path Synthesis:10.25µs
17:43:15|-|: 4. Alias Comp:    20.04µs
17:43:15|-|: 5. Traversal/Misc:16.96µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:133 ~ test6[80bb]::test_13_2):       84.00µs
17:43:15|-|: 1. Decomposition: 5.33µs
17:43:15|-|: 2. Constraint:    2.92µs
17:43:15|-|: 3. Path Synthesis:18.62µs
17:43:15|-|: 4. Alias Comp:    38.33µs
17:43:15|-|: 5. Traversal/Misc:18.79µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:135 ~ test6[80bb]::test_14_2):       16.46µs
17:43:15|-|: 1. Decomposition: 1.75µs
17:43:15|-|: 2. Constraint:    333.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    6.54µs
17:43:15|-|: 5. Traversal/Misc:7.83µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:137 ~ test6[80bb]::test_15):       186.79µs
17:43:15|-|: 1. Decomposition: 5.92µs
17:43:15|-|: 2. Constraint:    1.95µs
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    38.04µs
17:43:15|-|: 5. Traversal/Misc:140.88µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:139 ~ test6[80bb]::test_17):       49.50µs
17:43:15|-|: 1. Decomposition: 9.21µs
17:43:15|-|: 2. Constraint:    710.00ns
17:43:15|-|: 3. Path Synthesis:13.25µs
17:43:15|-|: 4. Alias Comp:    10.92µs
17:43:15|-|: 5. Traversal/Misc:15.42µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:141 ~ test6[80bb]::test_18):       101.17µs
17:43:15|-|: 1. Decomposition: 3.67µs
17:43:15|-|: 2. Constraint:    1.79µs
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    27.59µs
17:43:15|-|: 5. Traversal/Misc:68.12µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:143 ~ test6[80bb]::test_19):       100.83µs
17:43:15|-|: 1. Decomposition: 6.08µs
17:43:15|-|: 2. Constraint:    3.21µs
17:43:15|-|: 3. Path Synthesis:17.04µs
17:43:15|-|: 4. Alias Comp:    39.21µs
17:43:15|-|: 5. Traversal/Misc:35.29µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:145 ~ test6[80bb]::test_20):       337.17µs
17:43:15|-|: 1. Decomposition: 9.46µs
17:43:15|-|: 2. Constraint:    13.38µs
17:43:15|-|: 3. Path Synthesis:54.85µs
17:43:15|-|: 4. Alias Comp:    125.61µs
17:43:15|-|: 5. Traversal/Misc:133.88µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:147 ~ test6[80bb]::test_1_correlated_siblings):       173.38µs
17:43:15|-|: 1. Decomposition: 7.50µs
17:43:15|-|: 2. Constraint:    3.96µs
17:43:15|-|: 3. Path Synthesis:19.12µs
17:43:15|-|: 4. Alias Comp:    56.88µs
17:43:15|-|: 5. Traversal/Misc:85.92µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:149 ~ test6[80bb]::test_2_loop_carried_phase):       44.13µs
17:43:15|-|: 1. Decomposition: 5.25µs
17:43:15|-|: 2. Constraint:    915.00ns
17:43:15|-|: 3. Path Synthesis:8.41µs
17:43:15|-|: 4. Alias Comp:    15.04µs
17:43:15|-|: 5. Traversal/Misc:14.51µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:151 ~ test6[80bb]::test_3_nested_infeasible):       42.21µs
17:43:15|-|: 1. Decomposition: 5.83µs
17:43:15|-|: 2. Constraint:    626.00ns
17:43:15|-|: 3. Path Synthesis:4.33µs
17:43:15|-|: 4. Alias Comp:    11.29µs
17:43:15|-|: 5. Traversal/Misc:20.13µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:153 ~ test6[80bb]::test_4_ping_pong):       40.13µs
17:43:15|-|: 1. Decomposition: 4.92µs
17:43:15|-|: 2. Constraint:    668.00ns
17:43:15|-|: 3. Path Synthesis:5.92µs
17:43:15|-|: 4. Alias Comp:    15.16µs
17:43:15|-|: 5. Traversal/Misc:13.46µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:155 ~ test6[80bb]::test_5_multi_exit_accumulator):       60.92µs
17:43:15|-|: 1. Decomposition: 5.29µs
17:43:15|-|: 2. Constraint:    917.00ns
17:43:15|-|: 3. Path Synthesis:5.71µs
17:43:15|-|: 4. Alias Comp:    21.91µs
17:43:15|-|: 5. Traversal/Misc:27.09µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:157 ~ test6[80bb]::test_2_correlated_delay):       228.71µs
17:43:15|-|: 1. Decomposition: 8.79µs
17:43:15|-|: 2. Constraint:    5.80µs
17:43:15|-|: 3. Path Synthesis:37.75µs
17:43:15|-|: 4. Alias Comp:    85.57µs
17:43:15|-|: 5. Traversal/Misc:90.79µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:159 ~ test6[80bb]::test_3_sibling_loops):       248.25µs
17:43:15|-|: 1. Decomposition: 11.25µs
17:43:15|-|: 2. Constraint:    8.96µs
17:43:15|-|: 3. Path Synthesis:59.12µs
17:43:15|-|: 4. Alias Comp:    99.29µs
17:43:15|-|: 5. Traversal/Misc:69.63µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:161 ~ test6[80bb]::test_5_ping_pong):       31.88µs
17:43:15|-|: 1. Decomposition: 3.38µs
17:43:15|-|: 2. Constraint:    417.00ns
17:43:15|-|: 3. Path Synthesis:5.08µs
17:43:15|-|: 4. Alias Comp:    12.42µs
17:43:15|-|: 5. Traversal/Misc:10.58µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:163 ~ test6[80bb]::test_6_infeasible_path):       205.71µs
17:43:15|-|: 1. Decomposition: 11.46µs
17:43:15|-|: 2. Constraint:    6.38µs
17:43:15|-|: 3. Path Synthesis:71.45µs
17:43:15|-|: 4. Alias Comp:    82.59µs
17:43:15|-|: 5. Traversal/Misc:33.84µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:165 ~ test6[80bb]::test_7_multi_exit):       437.00µs
17:43:15|-|: 1. Decomposition: 9.04µs
17:43:15|-|: 2. Constraint:    16.82µs
17:43:15|-|: 3. Path Synthesis:85.11µs
17:43:15|-|: 4. Alias Comp:    216.23µs
17:43:15|-|: 5. Traversal/Misc:109.80µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:167 ~ test6[80bb]::test_9_deep_nest_flag):       980.75µs
17:43:15|-|: 1. Decomposition: 22.21µs
17:43:15|-|: 2. Constraint:    24.66µs
17:43:15|-|: 3. Path Synthesis:542.55µs
17:43:15|-|: 4. Alias Comp:    355.59µs
17:43:15|-|: 5. Traversal/Misc:35.75µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:169 ~ test6[80bb]::test_10_switchboard):       382.58µs
17:43:15|-|: 1. Decomposition: 8.54µs
17:43:15|-|: 2. Constraint:    13.79µs
17:43:15|-|: 3. Path Synthesis:73.04µs
17:43:15|-|: 4. Alias Comp:    220.47µs
17:43:15|-|: 5. Traversal/Misc:66.74µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:171 ~ test6[80bb]::test_11_correlated_exit):       90.58µs
17:43:15|-|: 1. Decomposition: 6.71µs
17:43:15|-|: 2. Constraint:    2.25µs
17:43:15|-|: 3. Path Synthesis:14.22µs
17:43:15|-|: 4. Alias Comp:    33.45µs
17:43:15|-|: 5. Traversal/Misc:33.96µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:173 ~ test6[80bb]::test_12_tuple_simulation):       38.17µs
17:43:15|-|: 1. Decomposition: 3.54µs
17:43:15|-|: 2. Constraint:    500.00ns
17:43:15|-|: 3. Path Synthesis:4.87µs
17:43:15|-|: 4. Alias Comp:    19.34µs
17:43:15|-|: 5. Traversal/Misc:9.92µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:175 ~ test6[80bb]::test_14_nesting_shadow):       80.38µs
17:43:15|-|: 1. Decomposition: 6.83µs
17:43:15|-|: 2. Constraint:    1.04µs
17:43:15|-|: 3. Path Synthesis:26.88µs
17:43:15|-|: 4. Alias Comp:    31.04µs
17:43:15|-|: 5. Traversal/Misc:14.58µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:177 ~ test6[80bb]::test_15_latch):       153.50µs
17:43:15|-|: 1. Decomposition: 7.08µs
17:43:15|-|: 2. Constraint:    8.43µs
17:43:15|-|: 3. Path Synthesis:50.20µs
17:43:15|-|: 4. Alias Comp:    65.50µs
17:43:15|-|: 5. Traversal/Misc:22.29µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:179 ~ test6[80bb]::test_16_mixer):       205.33µs
17:43:15|-|: 1. Decomposition: 11.79µs
17:43:15|-|: 2. Constraint:    6.33µs
17:43:15|-|: 3. Path Synthesis:78.17µs
17:43:15|-|: 4. Alias Comp:    92.04µs
17:43:15|-|: 5. Traversal/Misc:17.00µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:181 ~ test6[80bb]::test_18_flag_conflict):       124.88µs
17:43:15|-|: 1. Decomposition: 9.42µs
17:43:15|-|: 2. Constraint:    7.04µs
17:43:15|-|: 3. Path Synthesis:42.29µs
17:43:15|-|: 4. Alias Comp:    47.09µs
17:43:15|-|: 5. Traversal/Misc:19.04µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:183 ~ test6[80bb]::test_20_grand_finale):       2.27ms
17:43:15|-|: 1. Decomposition: 12.33µs
17:43:15|-|: 2. Constraint:    65.64µs
17:43:15|-|: 3. Path Synthesis:958.04µs
17:43:15|-|: 4. Alias Comp:    1.10ms
17:43:15|-|: 5. Traversal/Misc:142.58µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:185 ~ test6[80bb]::test_3_2):       565.67µs
17:43:15|-|: 1. Decomposition: 10.25µs
17:43:15|-|: 2. Constraint:    24.97µs
17:43:15|-|: 3. Path Synthesis:116.11µs
17:43:15|-|: 4. Alias Comp:    226.33µs
17:43:15|-|: 5. Traversal/Misc:188.01µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:187 ~ test6[80bb]::test_4):       1.07ms
17:43:15|-|: 1. Decomposition: 8.38µs
17:43:15|-|: 2. Constraint:    60.33µs
17:43:15|-|: 3. Path Synthesis:259.71µs
17:43:15|-|: 4. Alias Comp:    594.97µs
17:43:15|-|: 5. Traversal/Misc:145.79µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:189 ~ test6[80bb]::test_5):       110.17µs
17:43:15|-|: 1. Decomposition: 12.00µs
17:43:15|-|: 2. Constraint:    2.46µs
17:43:15|-|: 3. Path Synthesis:38.96µs
17:43:15|-|: 4. Alias Comp:    36.67µs
17:43:15|-|: 5. Traversal/Misc:20.08µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:191 ~ test6[80bb]::test_6_2):       959.25µs
17:43:15|-|: 1. Decomposition: 9.63µs
17:43:15|-|: 2. Constraint:    58.06µs
17:43:15|-|: 3. Path Synthesis:236.14µs
17:43:15|-|: 4. Alias Comp:    511.23µs
17:43:15|-|: 5. Traversal/Misc:144.20µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:193 ~ test6[80bb]::test_7):       361.25µs
17:43:15|-|: 1. Decomposition: 11.42µs
17:43:15|-|: 2. Constraint:    19.96µs
17:43:15|-|: 3. Path Synthesis:101.05µs
17:43:15|-|: 4. Alias Comp:    176.49µs
17:43:15|-|: 5. Traversal/Misc:52.34µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:195 ~ test6[80bb]::test_10):       958.13µs
17:43:15|-|: 1. Decomposition: 9.21µs
17:43:15|-|: 2. Constraint:    50.61µs
17:43:15|-|: 3. Path Synthesis:213.66µs
17:43:15|-|: 4. Alias Comp:    511.31µs
17:43:15|-|: 5. Traversal/Misc:173.33µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:197 ~ test6[80bb]::test_11):       350.92µs
17:43:15|-|: 1. Decomposition: 8.88µs
17:43:15|-|: 2. Constraint:    14.95µs
17:43:15|-|: 3. Path Synthesis:63.72µs
17:43:15|-|: 4. Alias Comp:    162.17µs
17:43:15|-|: 5. Traversal/Misc:101.21µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:199 ~ test6[80bb]::test_13):       79.71µs
17:43:15|-|: 1. Decomposition: 7.29µs
17:43:15|-|: 2. Constraint:    1.08µs
17:43:15|-|: 3. Path Synthesis:6.25µs
17:43:15|-|: 4. Alias Comp:    27.12µs
17:43:15|-|: 5. Traversal/Misc:37.96µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:201 ~ test6[80bb]::test_14):       255.83µs
17:43:15|-|: 1. Decomposition: 6.29µs
17:43:15|-|: 2. Constraint:    7.00µs
17:43:15|-|: 3. Path Synthesis:43.52µs
17:43:15|-|: 4. Alias Comp:    128.58µs
17:43:15|-|: 5. Traversal/Misc:70.45µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:203 ~ test6[80bb]::test_15_2):       115.71µs
17:43:15|-|: 1. Decomposition: 6.88µs
17:43:15|-|: 2. Constraint:    2.55µs
17:43:15|-|: 3. Path Synthesis:14.83µs
17:43:15|-|: 4. Alias Comp:    42.87µs
17:43:15|-|: 5. Traversal/Misc:48.58µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:205 ~ test6[80bb]::case_1):       46.42µs
17:43:15|-|: 1. Decomposition: 6.38µs
17:43:15|-|: 2. Constraint:    1.59µs
17:43:15|-|: 3. Path Synthesis:8.71µs
17:43:15|-|: 4. Alias Comp:    16.63µs
17:43:15|-|: 5. Traversal/Misc:13.13µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:207 ~ test6[80bb]::case_2):       42.92µs
17:43:15|-|: 1. Decomposition: 5.08µs
17:43:15|-|: 2. Constraint:    626.00ns
17:43:15|-|: 3. Path Synthesis:4.00µs
17:43:15|-|: 4. Alias Comp:    14.00µs
17:43:15|-|: 5. Traversal/Misc:19.21µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:209 ~ test6[80bb]::case_3):       55.92µs
17:43:15|-|: 1. Decomposition: 8.17µs
17:43:15|-|: 2. Constraint:    499.00ns
17:43:15|-|: 3. Path Synthesis:6.25µs
17:43:15|-|: 4. Alias Comp:    14.88µs
17:43:15|-|: 5. Traversal/Misc:26.13µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:211 ~ test6[80bb]::case_4):       48.88µs
17:43:15|-|: 1. Decomposition: 7.83µs
17:43:15|-|: 2. Constraint:    667.00ns
17:43:15|-|: 3. Path Synthesis:16.58µs
17:43:15|-|: 4. Alias Comp:    13.92µs
17:43:15|-|: 5. Traversal/Misc:9.87µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:213 ~ test6[80bb]::case_5):       52.96µs
17:43:15|-|: 1. Decomposition: 5.83µs
17:43:15|-|: 2. Constraint:    667.00ns
17:43:15|-|: 3. Path Synthesis:5.88µs
17:43:15|-|: 4. Alias Comp:    18.42µs
17:43:15|-|: 5. Traversal/Misc:22.17µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:215 ~ test6[80bb]::case_6):       715.50µs
17:43:15|-|: 1. Decomposition: 16.50µs
17:43:15|-|: 2. Constraint:    16.83µs
17:43:15|-|: 3. Path Synthesis:348.24µs
17:43:15|-|: 4. Alias Comp:    307.09µs
17:43:15|-|: 5. Traversal/Misc:26.83µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:217 ~ test6[80bb]::case_7):       103.46µs
17:43:15|-|: 1. Decomposition: 11.71µs
17:43:15|-|: 2. Constraint:    2.00µs
17:43:15|-|: 3. Path Synthesis:32.41µs
17:43:15|-|: 4. Alias Comp:    30.34µs
17:43:15|-|: 5. Traversal/Misc:27.00µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:219 ~ test6[80bb]::case_8):       29.75µs
17:43:15|-|: 1. Decomposition: 4.58µs
17:43:15|-|: 2. Constraint:    416.00ns
17:43:15|-|: 3. Path Synthesis:4.08µs
17:43:15|-|: 4. Alias Comp:    9.92µs
17:43:15|-|: 5. Traversal/Misc:10.75µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:221 ~ test6[80bb]::case_9):       178.79µs
17:43:15|-|: 1. Decomposition: 19.83µs
17:43:15|-|: 2. Constraint:    2.34µs
17:43:15|-|: 3. Path Synthesis:85.20µs
17:43:15|-|: 4. Alias Comp:    50.59µs
17:43:15|-|: 5. Traversal/Misc:20.84µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:223 ~ test6[80bb]::case_10):       160.50µs
17:43:15|-|: 1. Decomposition: 17.17µs
17:43:15|-|: 2. Constraint:    2.84µs
17:43:15|-|: 3. Path Synthesis:56.58µs
17:43:15|-|: 4. Alias Comp:    48.87µs
17:43:15|-|: 5. Traversal/Misc:35.05µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:225 ~ test6[80bb]::case_11):       46.29µs
17:43:15|-|: 1. Decomposition: 7.54µs
17:43:15|-|: 2. Constraint:    751.00ns
17:43:15|-|: 3. Path Synthesis:20.67µs
17:43:15|-|: 4. Alias Comp:    11.33µs
17:43:15|-|: 5. Traversal/Misc:6.00µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:227 ~ test6[80bb]::case_12):       41.83µs
17:43:15|-|: 1. Decomposition: 6.04µs
17:43:15|-|: 2. Constraint:    624.00ns
17:43:15|-|: 3. Path Synthesis:3.75µs
17:43:15|-|: 4. Alias Comp:    14.13µs
17:43:15|-|: 5. Traversal/Misc:17.29µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:229 ~ test6[80bb]::case_13):       31.71µs
17:43:15|-|: 1. Decomposition: 5.08µs
17:43:15|-|: 2. Constraint:    290.00ns
17:43:15|-|: 3. Path Synthesis:3.59µs
17:43:15|-|: 4. Alias Comp:    9.04µs
17:43:15|-|: 5. Traversal/Misc:13.71µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:231 ~ test6[80bb]::case_14):       61.54µs
17:43:15|-|: 1. Decomposition: 6.50µs
17:43:15|-|: 2. Constraint:    747.00ns
17:43:15|-|: 3. Path Synthesis:6.71µs
17:43:15|-|: 4. Alias Comp:    21.12µs
17:43:15|-|: 5. Traversal/Misc:26.46µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:233 ~ test6[80bb]::case_15):       77.50µs
17:43:15|-|: 1. Decomposition: 7.58µs
17:43:15|-|: 2. Constraint:    705.00ns
17:43:15|-|: 3. Path Synthesis:4.71µs
17:43:15|-|: 4. Alias Comp:    21.91µs
17:43:15|-|: 5. Traversal/Misc:42.58µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:235 ~ test6[80bb]::case_16):       195.50µs
17:43:15|-|: 1. Decomposition: 8.38µs
17:43:15|-|: 2. Constraint:    8.92µs
17:43:15|-|: 3. Path Synthesis:52.29µs
17:43:15|-|: 4. Alias Comp:    97.29µs
17:43:15|-|: 5. Traversal/Misc:28.63µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:237 ~ test6[80bb]::case_17):       61.33µs
17:43:15|-|: 1. Decomposition: 6.25µs
17:43:15|-|: 2. Constraint:    1.96µs
17:43:15|-|: 3. Path Synthesis:11.71µs
17:43:15|-|: 4. Alias Comp:    25.87µs
17:43:15|-|: 5. Traversal/Misc:15.54µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:239 ~ test6[80bb]::case_18):       140.38µs
17:43:15|-|: 1. Decomposition: 7.54µs
17:43:15|-|: 2. Constraint:    5.75µs
17:43:15|-|: 3. Path Synthesis:31.78µs
17:43:15|-|: 4. Alias Comp:    64.55µs
17:43:15|-|: 5. Traversal/Misc:30.75µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:241 ~ test6[80bb]::case_19):       11.00µs
17:43:15|-|: 1. Decomposition: 2.08µs
17:43:15|-|: 2. Constraint:    209.00ns
17:43:15|-|: 3. Path Synthesis:0.00ns
17:43:15|-|: 4. Alias Comp:    3.63µs
17:43:15|-|: 5. Traversal/Misc:5.08µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:243 ~ test6[80bb]::case_20):       252.42µs
17:43:15|-|: 1. Decomposition: 10.38µs
17:43:15|-|: 2. Constraint:    6.17µs
17:43:15|-|: 3. Path Synthesis:100.86µs
17:43:15|-|: 4. Alias Comp:    108.80µs
17:43:15|-|: 5. Traversal/Misc:26.21µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:245 ~ test6[80bb]::case_21):       38.58µs
17:43:15|-|: 1. Decomposition: 4.92µs
17:43:15|-|: 2. Constraint:    415.00ns
17:43:15|-|: 3. Path Synthesis:2.08µs
17:43:15|-|: 4. Alias Comp:    10.59µs
17:43:15|-|: 5. Traversal/Misc:20.58µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:247 ~ test6[80bb]::case_22):       4.04ms
17:43:15|-|: 1. Decomposition: 11.75µs
17:43:15|-|: 2. Constraint:    284.48µs
17:43:15|-|: 3. Path Synthesis:972.79µs
17:43:15|-|: 4. Alias Comp:    2.33ms
17:43:15|-|: 5. Traversal/Misc:437.48µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:249 ~ test6[80bb]::case_23):       309.67µs
17:43:15|-|: 1. Decomposition: 9.54µs
17:43:15|-|: 2. Constraint:    7.84µs
17:43:15|-|: 3. Path Synthesis:36.58µs
17:43:15|-|: 4. Alias Comp:    117.87µs
17:43:15|-|: 5. Traversal/Misc:137.84µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:251 ~ test6[80bb]::case_24):       109.58µs
17:43:15|-|: 1. Decomposition: 6.13µs
17:43:15|-|: 2. Constraint:    2.84µs
17:43:15|-|: 3. Path Synthesis:20.62µs
17:43:15|-|: 4. Alias Comp:    50.71µs
17:43:15|-|: 5. Traversal/Misc:29.29µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:253 ~ test6[80bb]::case_26):       25.58µs
17:43:15|-|: 1. Decomposition: 3.50µs
17:43:15|-|: 2. Constraint:    374.00ns
17:43:15|-|: 3. Path Synthesis:3.29µs
17:43:15|-|: 4. Alias Comp:    10.46µs
17:43:15|-|: 5. Traversal/Misc:7.96µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:255 ~ test6[80bb]::case_27):       62.17µs
17:43:15|-|: 1. Decomposition: 5.50µs
17:43:15|-|: 2. Constraint:    458.00ns
17:43:15|-|: 3. Path Synthesis:4.54µs
17:43:15|-|: 4. Alias Comp:    24.17µs
17:43:15|-|: 5. Traversal/Misc:27.50µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:257 ~ test6[80bb]::case_28):       45.88µs
17:43:15|-|: 1. Decomposition: 5.38µs
17:43:15|-|: 2. Constraint:    710.00ns
17:43:15|-|: 3. Path Synthesis:5.84µs
17:43:15|-|: 4. Alias Comp:    16.04µs
17:43:15|-|: 5. Traversal/Misc:17.92µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:259 ~ test6[80bb]::case_29):       50.88µs
17:43:15|-|: 1. Decomposition: 5.96µs
17:43:15|-|: 2. Constraint:    626.00ns
17:43:15|-|: 3. Path Synthesis:4.00µs
17:43:15|-|: 4. Alias Comp:    13.92µs
17:43:15|-|: 5. Traversal/Misc:26.38µs
17:43:15|-|: ===========================
17:43:15|-|: === Performance Profiling ===
17:43:15|-|: Total Time of DefId(0:261 ~ test6[80bb]::case_30):       107.92µs
17:43:15|-|: 1. Decomposition: 9.50µs
17:43:15|-|: 2. Constraint:    1.25µs
17:43:15|-|: 3. Path Synthesis:17.29µs
17:43:15|-|: 4. Alias Comp:    29.88µs
17:43:15|-|: 5. Traversal/Misc:50.00µs
17:43:15|-|: ===========================
"""

log_data3 = """
17:48:54|-|: Total Time of DefId(0:3 ~ test7[1d05]::scc_temporal_case_1):       6.52ms
17:48:54|-|: 1. Decomposition: 231.42µs
17:48:54|-|: 2. Constraint:    195.46µs
17:48:54|-|: 3. Path Synthesis:2.08ms
17:48:54|-|: 4. Alias Comp:    3.05ms
17:48:54|-|: 5. Traversal/Misc:968.34µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:5 ~ test7[1d05]::scc_temporal_case_2):       375.71µs
17:48:54|-|: 1. Decomposition: 18.46µs
17:48:54|-|: 2. Constraint:    14.37µs
17:48:54|-|: 3. Path Synthesis:155.06µs
17:48:54|-|: 4. Alias Comp:    159.29µs
17:48:54|-|: 5. Traversal/Misc:28.54µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:7 ~ test7[1d05]::scc_temporal_case_3):       1.65ms
17:48:54|-|: 1. Decomposition: 22.38µs
17:48:54|-|: 2. Constraint:    50.46µs
17:48:54|-|: 3. Path Synthesis:797.07µs
17:48:54|-|: 4. Alias Comp:    688.36µs
17:48:54|-|: 5. Traversal/Misc:87.04µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:9 ~ test7[1d05]::scc_temporal_case_4):       127.42µs
17:48:54|-|: 1. Decomposition: 9.79µs
17:48:54|-|: 2. Constraint:    2.21µs
17:48:54|-|: 3. Path Synthesis:43.83µs
17:48:54|-|: 4. Alias Comp:    49.46µs
17:48:54|-|: 5. Traversal/Misc:22.12µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:11 ~ test7[1d05]::scc_temporal_case_5):       1.92ms
17:48:54|-|: 1. Decomposition: 15.08µs
17:48:54|-|: 2. Constraint:    64.08µs
17:48:54|-|: 3. Path Synthesis:708.98µs
17:48:54|-|: 4. Alias Comp:    965.76µs
17:48:54|-|: 5. Traversal/Misc:171.05µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:13 ~ test7[1d05]::scc_temporal_case_6):       477.75µs
17:48:54|-|: 1. Decomposition: 14.58µs
17:48:54|-|: 2. Constraint:    16.34µs
17:48:54|-|: 3. Path Synthesis:178.27µs
17:48:54|-|: 4. Alias Comp:    222.85µs
17:48:54|-|: 5. Traversal/Misc:45.71µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:15 ~ test7[1d05]::scc_temporal_case_7):       147.50µs
17:48:54|-|: 1. Decomposition: 10.04µs
17:48:54|-|: 2. Constraint:    2.99µs
17:48:54|-|: 3. Path Synthesis:17.41µs
17:48:54|-|: 4. Alias Comp:    57.89µs
17:48:54|-|: 5. Traversal/Misc:59.16µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:17 ~ test7[1d05]::scc_temporal_case_8):       167.21µs
17:48:54|-|: 1. Decomposition: 8.29µs
17:48:54|-|: 2. Constraint:    8.26µs
17:48:54|-|: 3. Path Synthesis:38.54µs
17:48:54|-|: 4. Alias Comp:    82.13µs
17:48:54|-|: 5. Traversal/Misc:30.00µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:19 ~ test7[1d05]::scc_temporal_case_9):       712.17µs
17:48:54|-|: 1. Decomposition: 20.96µs
17:48:54|-|: 2. Constraint:    26.28µs
17:48:54|-|: 3. Path Synthesis:365.00µs
17:48:54|-|: 4. Alias Comp:    263.72µs
17:48:54|-|: 5. Traversal/Misc:36.21µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:21 ~ test7[1d05]::scc_temporal_case_10):       82.29µs
17:48:54|-|: 1. Decomposition: 7.00µs
17:48:54|-|: 2. Constraint:    1.29µs
17:48:54|-|: 3. Path Synthesis:6.00µs
17:48:54|-|: 4. Alias Comp:    27.96µs
17:48:54|-|: 5. Traversal/Misc:40.05µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:23 ~ test7[1d05]::scc_temporal_case_11):       97.21µs
17:48:54|-|: 1. Decomposition: 6.29µs
17:48:54|-|: 2. Constraint:    1.20µs
17:48:54|-|: 3. Path Synthesis:3.79µs
17:48:54|-|: 4. Alias Comp:    28.59µs
17:48:54|-|: 5. Traversal/Misc:57.33µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:25 ~ test7[1d05]::scc_temporal_case_12):       75.83µs
17:48:54|-|: 1. Decomposition: 7.54µs
17:48:54|-|: 2. Constraint:    1.25µs
17:48:54|-|: 3. Path Synthesis:4.04µs
17:48:54|-|: 4. Alias Comp:    19.79µs
17:48:54|-|: 5. Traversal/Misc:43.21µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:27 ~ test7[1d05]::scc_temporal_case_13):       35.83µs
17:48:54|-|: 1. Decomposition: 4.75µs
17:48:54|-|: 2. Constraint:    709.00ns
17:48:54|-|: 3. Path Synthesis:2.84µs
17:48:54|-|: 4. Alias Comp:    10.66µs
17:48:54|-|: 5. Traversal/Misc:16.88µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:29 ~ test7[1d05]::scc_temporal_case_14):       43.25µs
17:48:54|-|: 1. Decomposition: 5.54µs
17:48:54|-|: 2. Constraint:    956.00ns
17:48:54|-|: 3. Path Synthesis:5.55µs
17:48:54|-|: 4. Alias Comp:    14.08µs
17:48:54|-|: 5. Traversal/Misc:17.13µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:31 ~ test7[1d05]::scc_temporal_case_15):       72.96µs
17:48:54|-|: 1. Decomposition: 6.92µs
17:48:54|-|: 2. Constraint:    1.25µs
17:48:54|-|: 3. Path Synthesis:5.08µs
17:48:54|-|: 4. Alias Comp:    25.00µs
17:48:54|-|: 5. Traversal/Misc:34.71µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:33 ~ test7[1d05]::scc_temporal_case_16):       14.08µs
17:48:54|-|: 1. Decomposition: 3.63µs
17:48:54|-|: 2. Constraint:    291.00ns
17:48:54|-|: 3. Path Synthesis:1.88µs
17:48:54|-|: 4. Alias Comp:    3.38µs
17:48:54|-|: 5. Traversal/Misc:4.92µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:35 ~ test7[1d05]::scc_temporal_case_17):       29.38µs
17:48:54|-|: 1. Decomposition: 4.04µs
17:48:54|-|: 2. Constraint:    375.00ns
17:48:54|-|: 3. Path Synthesis:3.87µs
17:48:54|-|: 4. Alias Comp:    11.38µs
17:48:54|-|: 5. Traversal/Misc:9.71µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:37 ~ test7[1d05]::scc_temporal_case_18):       40.29µs
17:48:54|-|: 1. Decomposition: 2.75µs
17:48:54|-|: 2. Constraint:    585.00ns
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    16.29µs
17:48:54|-|: 5. Traversal/Misc:20.66µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:39 ~ test7[1d05]::scc_temporal_case_19):       69.71µs
17:48:54|-|: 1. Decomposition: 4.04µs
17:48:54|-|: 2. Constraint:    751.00ns
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    25.66µs
17:48:54|-|: 5. Traversal/Misc:39.25µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:41 ~ test7[1d05]::scc_temporal_case_20):       133.96µs
17:48:54|-|: 1. Decomposition: 10.75µs
17:48:54|-|: 2. Constraint:    4.58µs
17:48:54|-|: 3. Path Synthesis:22.67µs
17:48:54|-|: 4. Alias Comp:    53.29µs
17:48:54|-|: 5. Traversal/Misc:42.67µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:43 ~ test7[1d05]::scc_temporal_case_21):       99.25µs
17:48:54|-|: 1. Decomposition: 5.08µs
17:48:54|-|: 2. Constraint:    1.42µs
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    29.04µs
17:48:54|-|: 5. Traversal/Misc:63.71µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:45 ~ test7[1d05]::scc_temporal_case_22):       32.75µs
17:48:54|-|: 1. Decomposition: 3.17µs
17:48:54|-|: 2. Constraint:    542.00ns
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    11.79µs
17:48:54|-|: 5. Traversal/Misc:17.25µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:47 ~ test7[1d05]::scc_temporal_case_23):       61.92µs
17:48:54|-|: 1. Decomposition: 6.08µs
17:48:54|-|: 2. Constraint:    792.00ns
17:48:54|-|: 3. Path Synthesis:4.29µs
17:48:54|-|: 4. Alias Comp:    19.21µs
17:48:54|-|: 5. Traversal/Misc:31.54µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:49 ~ test7[1d05]::scc_temporal_case_24):       64.04µs
17:48:54|-|: 1. Decomposition: 4.13µs
17:48:54|-|: 2. Constraint:    709.00ns
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    19.96µs
17:48:54|-|: 5. Traversal/Misc:39.25µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:51 ~ test7[1d05]::scc_temporal_case_25):       1.29ms
17:48:54|-|: 1. Decomposition: 7.92µs
17:48:54|-|: 2. Constraint:    50.79µs
17:48:54|-|: 3. Path Synthesis:305.42µs
17:48:54|-|: 4. Alias Comp:    688.57µs
17:48:54|-|: 5. Traversal/Misc:237.05µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:53 ~ test7[1d05]::scc_temporal_case_26):       164.92µs
17:48:54|-|: 1. Decomposition: 9.17µs
17:48:54|-|: 2. Constraint:    7.59µs
17:48:54|-|: 3. Path Synthesis:41.67µs
17:48:54|-|: 4. Alias Comp:    73.13µs
17:48:54|-|: 5. Traversal/Misc:33.37µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:55 ~ test7[1d05]::scc_temporal_case_27):       298.25µs
17:48:54|-|: 1. Decomposition: 9.33µs
17:48:54|-|: 2. Constraint:    14.59µs
17:48:54|-|: 3. Path Synthesis:70.58µs
17:48:54|-|: 4. Alias Comp:    148.63µs
17:48:54|-|: 5. Traversal/Misc:55.12µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:57 ~ test7[1d05]::scc_temporal_case_28):       685.33µs
17:48:54|-|: 1. Decomposition: 10.17µs
17:48:54|-|: 2. Constraint:    39.21µs
17:48:54|-|: 3. Path Synthesis:171.45µs
17:48:54|-|: 4. Alias Comp:    355.92µs
17:48:54|-|: 5. Traversal/Misc:108.59µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:59 ~ test7[1d05]::scc_temporal_case_29):       111.25µs
17:48:54|-|: 1. Decomposition: 6.13µs
17:48:54|-|: 2. Constraint:    1.08µs
17:48:54|-|: 3. Path Synthesis:4.29µs
17:48:54|-|: 4. Alias Comp:    35.21µs
17:48:54|-|: 5. Traversal/Misc:64.54µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:61 ~ test7[1d05]::scc_temporal_case_30):       275.46µs
17:48:54|-|: 1. Decomposition: 8.58µs
17:48:54|-|: 2. Constraint:    9.83µs
17:48:54|-|: 3. Path Synthesis:64.66µs
17:48:54|-|: 4. Alias Comp:    146.30µs
17:48:54|-|: 5. Traversal/Misc:46.08µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:63 ~ test7[1d05]::random_test1):       28.75µs
17:48:54|-|: 1. Decomposition: 5.71µs
17:48:54|-|: 2. Constraint:    250.00ns
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    8.33µs
17:48:54|-|: 5. Traversal/Misc:14.46µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:86 ~ test7[1d05]::random_test2):       3.04µs
17:48:54|-|: 1. Decomposition: 1.08µs
17:48:54|-|: 2. Constraint:    0.00ns
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    1.17µs
17:48:54|-|: 5. Traversal/Misc:791.00ns
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:87 ~ test7[1d05]::random_int_test2):       2.42µs
17:48:54|-|: 1. Decomposition: 916.00ns
17:48:54|-|: 2. Constraint:    0.00ns
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    876.00ns
17:48:54|-|: 5. Traversal/Misc:625.00ns
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:88 ~ test7[1d05]::random_test3):       1.92µs
17:48:54|-|: 1. Decomposition: 625.00ns
17:48:54|-|: 2. Constraint:    0.00ns
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    791.00ns
17:48:54|-|: 5. Traversal/Misc:500.00ns
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:89 ~ test7[1d05]::test1):       86.54µs
17:48:54|-|: 1. Decomposition: 5.54µs
17:48:54|-|: 2. Constraint:    1.79µs
17:48:54|-|: 3. Path Synthesis:13.75µs
17:48:54|-|: 4. Alias Comp:    39.50µs
17:48:54|-|: 5. Traversal/Misc:25.96µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:91 ~ test7[1d05]::test5):       23.04µs
17:48:54|-|: 1. Decomposition: 3.96µs
17:48:54|-|: 2. Constraint:    208.00ns
17:48:54|-|: 3. Path Synthesis:2.50µs
17:48:54|-|: 4. Alias Comp:    8.38µs
17:48:54|-|: 5. Traversal/Misc:8.00µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:93 ~ test7[1d05]::pipeline_propagation):       85.67µs
17:48:54|-|: 1. Decomposition: 4.88µs
17:48:54|-|: 2. Constraint:    750.00ns
17:48:54|-|: 3. Path Synthesis:8.04µs
17:48:54|-|: 4. Alias Comp:    39.96µs
17:48:54|-|: 5. Traversal/Misc:32.04µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:95 ~ test7[1d05]::test_pipeline_correlation):       585.75µs
17:48:54|-|: 1. Decomposition: 13.25µs
17:48:54|-|: 2. Constraint:    14.49µs
17:48:54|-|: 3. Path Synthesis:229.46µs
17:48:54|-|: 4. Alias Comp:    259.22µs
17:48:54|-|: 5. Traversal/Misc:69.33µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:97 ~ test7[1d05]::case_unroll_pipeline):       31.46µs
17:48:54|-|: 1. Decomposition: 3.63µs
17:48:54|-|: 2. Constraint:    543.00ns
17:48:54|-|: 3. Path Synthesis:4.83µs
17:48:54|-|: 4. Alias Comp:    12.50µs
17:48:54|-|: 5. Traversal/Misc:9.96µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:99 ~ test7[1d05]::test_16):       51.75µs
17:48:54|-|: 1. Decomposition: 5.29µs
17:48:54|-|: 2. Constraint:    916.00ns
17:48:54|-|: 3. Path Synthesis:5.67µs
17:48:54|-|: 4. Alias Comp:    18.29µs
17:48:54|-|: 5. Traversal/Misc:21.58µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:101 ~ test7[1d05]::test_1_pipeline):       81.92µs
17:48:54|-|: 1. Decomposition: 4.67µs
17:48:54|-|: 2. Constraint:    792.00ns
17:48:54|-|: 3. Path Synthesis:10.46µs
17:48:54|-|: 4. Alias Comp:    38.79µs
17:48:54|-|: 5. Traversal/Misc:27.21µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:103 ~ test7[1d05]::test_4_nested_depth_3):       55.74ms
17:48:54|-|: 1. Decomposition: 19.58µs
17:48:54|-|: 2. Constraint:    1.01ms
17:48:54|-|: 3. Path Synthesis:28.07ms
17:48:54|-|: 4. Alias Comp:    24.09ms
17:48:54|-|: 5. Traversal/Misc:2.55ms
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:105 ~ test7[1d05]::test_13_state_machine):       277.04µs
17:48:54|-|: 1. Decomposition: 10.63µs
17:48:54|-|: 2. Constraint:    6.84µs
17:48:54|-|: 3. Path Synthesis:51.13µs
17:48:54|-|: 4. Alias Comp:    133.58µs
17:48:54|-|: 5. Traversal/Misc:74.87µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:107 ~ test7[1d05]::test_17_ptr_chase):       120.21µs
17:48:54|-|: 1. Decomposition: 7.33µs
17:48:54|-|: 2. Constraint:    1.83µs
17:48:54|-|: 3. Path Synthesis:11.54µs
17:48:54|-|: 4. Alias Comp:    48.84µs
17:48:54|-|: 5. Traversal/Misc:50.67µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:109 ~ test7[1d05]::test_1):       620.17µs
17:48:54|-|: 1. Decomposition: 12.25µs
17:48:54|-|: 2. Constraint:    33.09µs
17:48:54|-|: 3. Path Synthesis:186.27µs
17:48:54|-|: 4. Alias Comp:    328.59µs
17:48:54|-|: 5. Traversal/Misc:59.96µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:111 ~ test7[1d05]::test_2):       1.07ms
17:48:54|-|: 1. Decomposition: 11.00µs
17:48:54|-|: 2. Constraint:    51.64µs
17:48:54|-|: 3. Path Synthesis:199.91µs
17:48:54|-|: 4. Alias Comp:    552.83µs
17:48:54|-|: 5. Traversal/Misc:250.99µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:113 ~ test7[1d05]::test_8):       56.25µs
17:48:54|-|: 1. Decomposition: 4.38µs
17:48:54|-|: 2. Constraint:    792.00ns
17:48:54|-|: 3. Path Synthesis:7.88µs
17:48:54|-|: 4. Alias Comp:    25.62µs
17:48:54|-|: 5. Traversal/Misc:17.58µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:115 ~ test7[1d05]::test_9):       250.83µs
17:48:54|-|: 1. Decomposition: 10.96µs
17:48:54|-|: 2. Constraint:    9.62µs
17:48:54|-|: 3. Path Synthesis:90.63µs
17:48:54|-|: 4. Alias Comp:    105.83µs
17:48:54|-|: 5. Traversal/Misc:33.80µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:117 ~ test7[1d05]::test_12):       1.36ms
17:48:54|-|: 1. Decomposition: 9.04µs
17:48:54|-|: 2. Constraint:    67.54µs
17:48:54|-|: 3. Path Synthesis:333.39µs
17:48:54|-|: 4. Alias Comp:    733.04µs
17:48:54|-|: 5. Traversal/Misc:216.20µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:119 ~ test7[1d05]::test_16_2):       4.20ms
17:48:54|-|: 1. Decomposition: 22.42µs
17:48:54|-|: 2. Constraint:    143.61µs
17:48:54|-|: 3. Path Synthesis:2.30ms
17:48:54|-|: 4. Alias Comp:    1.63ms
17:48:54|-|: 5. Traversal/Misc:107.84µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:121 ~ test7[1d05]::test_17):       1.44ms
17:48:54|-|: 1. Decomposition: 10.08µs
17:48:54|-|: 2. Constraint:    68.00µs
17:48:54|-|: 3. Path Synthesis:292.02µs
17:48:54|-|: 4. Alias Comp:    834.51µs
17:48:54|-|: 5. Traversal/Misc:234.55µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:123 ~ test7[1d05]::test_18):       584.83µs
17:48:54|-|: 1. Decomposition: 9.54µs
17:48:54|-|: 2. Constraint:    21.56µs
17:48:54|-|: 3. Path Synthesis:118.14µs
17:48:54|-|: 4. Alias Comp:    322.46µs
17:48:54|-|: 5. Traversal/Misc:113.13µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:125 ~ test7[1d05]::test_19):       1.10ms
17:48:54|-|: 1. Decomposition: 8.79µs
17:48:54|-|: 2. Constraint:    37.58µs
17:48:54|-|: 3. Path Synthesis:181.83µs
17:48:54|-|: 4. Alias Comp:    592.47µs
17:48:54|-|: 5. Traversal/Misc:282.16µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:127 ~ test7[1d05]::test_20):       655.13µs
17:48:54|-|: 1. Decomposition: 9.96µs
17:48:54|-|: 2. Constraint:    20.95µs
17:48:54|-|: 3. Path Synthesis:123.06µs
17:48:54|-|: 4. Alias Comp:    299.96µs
17:48:54|-|: 5. Traversal/Misc:201.20µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:129 ~ test7[1d05]::random_bool_test4):       2.38µs
17:48:54|-|: 1. Decomposition: 875.00ns
17:48:54|-|: 2. Constraint:    0.00ns
17:48:54|-|: 3. Path Synthesis:0.00ns
17:48:54|-|: 4. Alias Comp:    917.00ns
17:48:54|-|: 5. Traversal/Misc:583.00ns
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:130 ~ test7[1d05]::case_1):       220.04µs
17:48:54|-|: 1. Decomposition: 8.13µs
17:48:54|-|: 2. Constraint:    13.97µs
17:48:54|-|: 3. Path Synthesis:58.59µs
17:48:54|-|: 4. Alias Comp:    103.26µs
17:48:54|-|: 5. Traversal/Misc:36.09µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:132 ~ test7[1d05]::case_2):       134.50µs
17:48:54|-|: 1. Decomposition: 8.04µs
17:48:54|-|: 2. Constraint:    5.87µs
17:48:54|-|: 3. Path Synthesis:25.45µs
17:48:54|-|: 4. Alias Comp:    55.59µs
17:48:54|-|: 5. Traversal/Misc:39.54µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:134 ~ test7[1d05]::case_3):       65.75µs
17:48:54|-|: 1. Decomposition: 8.58µs
17:48:54|-|: 2. Constraint:    1.04µs
17:48:54|-|: 3. Path Synthesis:9.12µs
17:48:54|-|: 4. Alias Comp:    17.75µs
17:48:54|-|: 5. Traversal/Misc:29.25µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:136 ~ test7[1d05]::case_4):       198.88µs
17:48:54|-|: 1. Decomposition: 9.92µs
17:48:54|-|: 2. Constraint:    7.18µs
17:48:54|-|: 3. Path Synthesis:83.46µs
17:48:54|-|: 4. Alias Comp:    73.82µs
17:48:54|-|: 5. Traversal/Misc:24.50µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:138 ~ test7[1d05]::case_5):       90.21µs
17:48:54|-|: 1. Decomposition: 6.21µs
17:48:54|-|: 2. Constraint:    2.25µs
17:48:54|-|: 3. Path Synthesis:13.16µs
17:48:54|-|: 4. Alias Comp:    35.01µs
17:48:54|-|: 5. Traversal/Misc:33.58µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:140 ~ test7[1d05]::case_6):       2.29ms
17:48:54|-|: 1. Decomposition: 18.13µs
17:48:54|-|: 2. Constraint:    91.90µs
17:48:54|-|: 3. Path Synthesis:1.09ms
17:48:54|-|: 4. Alias Comp:    1.07ms
17:48:54|-|: 5. Traversal/Misc:24.17µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:142 ~ test7[1d05]::case_7):       552.96µs
17:48:54|-|: 1. Decomposition: 12.92µs
17:48:54|-|: 2. Constraint:    22.67µs
17:48:54|-|: 3. Path Synthesis:227.18µs
17:48:54|-|: 4. Alias Comp:    226.27µs
17:48:54|-|: 5. Traversal/Misc:63.92µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:144 ~ test7[1d05]::case_8):       24.13µs
17:48:54|-|: 1. Decomposition: 3.29µs
17:48:54|-|: 2. Constraint:    334.00ns
17:48:54|-|: 3. Path Synthesis:3.58µs
17:48:54|-|: 4. Alias Comp:    8.25µs
17:48:54|-|: 5. Traversal/Misc:8.67µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:146 ~ test7[1d05]::case_9):       8.58ms
17:48:54|-|: 1. Decomposition: 28.00µs
17:48:54|-|: 2. Constraint:    454.41µs
17:48:54|-|: 3. Path Synthesis:4.33ms
17:48:54|-|: 4. Alias Comp:    3.72ms
17:48:54|-|: 5. Traversal/Misc:49.42µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:148 ~ test7[1d05]::case_10):       75.79µs
17:48:54|-|: 1. Decomposition: 7.75µs
17:48:54|-|: 2. Constraint:    1.75µs
17:48:54|-|: 3. Path Synthesis:14.92µs
17:48:54|-|: 4. Alias Comp:    27.63µs
17:48:54|-|: 5. Traversal/Misc:23.75µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:150 ~ test7[1d05]::case_11):       44.75µs
17:48:54|-|: 1. Decomposition: 6.79µs
17:48:54|-|: 2. Constraint:    1.01µs
17:48:54|-|: 3. Path Synthesis:19.58µs
17:48:54|-|: 4. Alias Comp:    11.38µs
17:48:54|-|: 5. Traversal/Misc:6.00µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:152 ~ test7[1d05]::case_12):       46.42µs
17:48:54|-|: 1. Decomposition: 5.96µs
17:48:54|-|: 2. Constraint:    1.29µs
17:48:54|-|: 3. Path Synthesis:20.30µs
17:48:54|-|: 4. Alias Comp:    13.00µs
17:48:54|-|: 5. Traversal/Misc:5.88µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:154 ~ test7[1d05]::case_13):       38.50µs
17:48:54|-|: 1. Decomposition: 4.63µs
17:48:54|-|: 2. Constraint:    832.00ns
17:48:54|-|: 3. Path Synthesis:4.62µs
17:48:54|-|: 4. Alias Comp:    12.63µs
17:48:54|-|: 5. Traversal/Misc:15.79µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:156 ~ test7[1d05]::case_14):       39.79µs
17:48:54|-|: 1. Decomposition: 4.04µs
17:48:54|-|: 2. Constraint:    586.00ns
17:48:54|-|: 3. Path Synthesis:4.95µs
17:48:54|-|: 4. Alias Comp:    14.34µs
17:48:54|-|: 5. Traversal/Misc:15.88µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:158 ~ test7[1d05]::case_15):       67.38µs
17:48:54|-|: 1. Decomposition: 6.63µs
17:48:54|-|: 2. Constraint:    709.00ns
17:48:54|-|: 3. Path Synthesis:6.04µs
17:48:54|-|: 4. Alias Comp:    21.29µs
17:48:54|-|: 5. Traversal/Misc:32.71µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:160 ~ test7[1d05]::case_16):       526.58µs
17:48:54|-|: 1. Decomposition: 7.50µs
17:48:54|-|: 2. Constraint:    24.77µs
17:48:54|-|: 3. Path Synthesis:143.34µs
17:48:54|-|: 4. Alias Comp:    265.97µs
17:48:54|-|: 5. Traversal/Misc:85.00µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:162 ~ test7[1d05]::case_17):       222.13µs
17:48:54|-|: 1. Decomposition: 6.50µs
17:48:54|-|: 2. Constraint:    13.09µs
17:48:54|-|: 3. Path Synthesis:58.82µs
17:48:54|-|: 4. Alias Comp:    108.84µs
17:48:54|-|: 5. Traversal/Misc:34.87µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:164 ~ test7[1d05]::case_18):       131.67µs
17:48:54|-|: 1. Decomposition: 6.17µs
17:48:54|-|: 2. Constraint:    6.75µs
17:48:54|-|: 3. Path Synthesis:31.37µs
17:48:54|-|: 4. Alias Comp:    60.84µs
17:48:54|-|: 5. Traversal/Misc:26.54µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:166 ~ test7[1d05]::case_19):       49.00µs
17:48:54|-|: 1. Decomposition: 4.58µs
17:48:54|-|: 2. Constraint:    1.38µs
17:48:54|-|: 3. Path Synthesis:10.63µs
17:48:54|-|: 4. Alias Comp:    19.37µs
17:48:54|-|: 5. Traversal/Misc:13.04µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:168 ~ test7[1d05]::case_20):       112.29µs
17:48:54|-|: 1. Decomposition: 8.54µs
17:48:54|-|: 2. Constraint:    3.45µs
17:48:54|-|: 3. Path Synthesis:39.04µs
17:48:54|-|: 4. Alias Comp:    47.26µs
17:48:54|-|: 5. Traversal/Misc:14.00µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:170 ~ test7[1d05]::case_21):       35.71µs
17:48:54|-|: 1. Decomposition: 4.17µs
17:48:54|-|: 2. Constraint:    419.00ns
17:48:54|-|: 3. Path Synthesis:2.83µs
17:48:54|-|: 4. Alias Comp:    11.25µs
17:48:54|-|: 5. Traversal/Misc:17.04µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:172 ~ test7[1d05]::case_22):       3.36ms
17:48:54|-|: 1. Decomposition: 9.38µs
17:48:54|-|: 2. Constraint:    233.26µs
17:48:54|-|: 3. Path Synthesis:961.92µs
17:48:54|-|: 4. Alias Comp:    1.88ms
17:48:54|-|: 5. Traversal/Misc:271.59µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:174 ~ test7[1d05]::case_23):       215.79µs
17:48:54|-|: 1. Decomposition: 10.25µs
17:48:54|-|: 2. Constraint:    4.00µs
17:48:54|-|: 3. Path Synthesis:21.50µs
17:48:54|-|: 4. Alias Comp:    80.83µs
17:48:54|-|: 5. Traversal/Misc:99.21µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:176 ~ test7[1d05]::case_24):       224.54µs
17:48:54|-|: 1. Decomposition: 6.42µs
17:48:54|-|: 2. Constraint:    9.37µs
17:48:54|-|: 3. Path Synthesis:51.09µs
17:48:54|-|: 4. Alias Comp:    114.25µs
17:48:54|-|: 5. Traversal/Misc:43.41µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:178 ~ test7[1d05]::case_26):       23.38µs
17:48:54|-|: 1. Decomposition: 3.33µs
17:48:54|-|: 2. Constraint:    333.00ns
17:48:54|-|: 3. Path Synthesis:3.46µs
17:48:54|-|: 4. Alias Comp:    8.63µs
17:48:54|-|: 5. Traversal/Misc:7.63µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:180 ~ test7[1d05]::case_27):       89.33µs
17:48:54|-|: 1. Decomposition: 5.96µs
17:48:54|-|: 2. Constraint:    2.29µs
17:48:54|-|: 3. Path Synthesis:15.83µs
17:48:54|-|: 4. Alias Comp:    29.50µs
17:48:54|-|: 5. Traversal/Misc:35.75µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:182 ~ test7[1d05]::case_28):       40.71µs
17:48:54|-|: 1. Decomposition: 4.42µs
17:48:54|-|: 2. Constraint:    710.00ns
17:48:54|-|: 3. Path Synthesis:5.04µs
17:48:54|-|: 4. Alias Comp:    14.67µs
17:48:54|-|: 5. Traversal/Misc:15.88µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:184 ~ test7[1d05]::case_29):       48.79µs
17:48:54|-|: 1. Decomposition: 6.08µs
17:48:54|-|: 2. Constraint:    833.00ns
17:48:54|-|: 3. Path Synthesis:5.62µs
17:48:54|-|: 4. Alias Comp:    13.08µs
17:48:54|-|: 5. Traversal/Misc:23.17µs
17:48:54|-|: ===========================
17:48:54|-|: === Performance Profiling ===
17:48:54|-|: Total Time of DefId(0:186 ~ test7[1d05]::case_30):       371.71µs
17:48:54|-|: 1. Decomposition: 20.04µs
17:48:54|-|: 2. Constraint:    13.63µs
17:48:54|-|: 3. Path Synthesis:140.03µs
17:48:54|-|: 4. Alias Comp:    140.18µs
17:48:54|-|: 5. Traversal/Misc:57.83µs
17:48:54|-|: ===========================
"""

log_data0 = """
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:12830 ~ core[23ab]::slice::sort::stable::quicksort::quicksort):       69.62ms
17:57:33|-|: 1. Decomposition: 14.54µs
17:57:33|-|: 2. Constraint:    312.66µs
17:57:33|-|: 3. Path Synthesis:1.58ms
17:57:33|-|: 4. Alias Comp:    64.06ms
17:57:33|-|: 5. Traversal/Misc:3.65ms
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:9588 ~ core[23ab]::iter::traits::double_ended::DoubleEndedIterator::rfold):       362.04µs
17:57:33|-|: 1. Decomposition: 5.88µs
17:57:33|-|: 2. Constraint:    1.71µs
17:57:33|-|: 3. Path Synthesis:12.42µs
17:57:33|-|: 4. Alias Comp:    165.58µs
17:57:33|-|: 5. Traversal/Misc:176.46µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:10050 ~ core[23ab]::iter::traits::iterator::{impl#3}::spec_try_fold):       764.71µs
17:57:33|-|: 1. Decomposition: 8.67µs
17:57:33|-|: 2. Constraint:    3.42µs
17:57:33|-|: 3. Path Synthesis:23.54µs
17:57:33|-|: 4. Alias Comp:    391.26µs
17:57:33|-|: 5. Traversal/Misc:337.83µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37367 ~ core[23ab]::iter::adapters::step_by::{impl#12}::spec_fold):       498.38µs
17:57:33|-|: 1. Decomposition: 8.58µs
17:57:33|-|: 2. Constraint:    2.95µs
17:57:33|-|: 3. Path Synthesis:18.05µs
17:57:33|-|: 4. Alias Comp:    160.21µs
17:57:33|-|: 5. Traversal/Misc:308.58µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37381 ~ core[23ab]::iter::adapters::step_by::{impl#14}::spec_fold):       472.21µs
17:57:33|-|: 1. Decomposition: 8.17µs
17:57:33|-|: 2. Constraint:    3.12µs
17:57:33|-|: 3. Path Synthesis:15.17µs
17:57:33|-|: 4. Alias Comp:    150.00µs
17:57:33|-|: 5. Traversal/Misc:295.76µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37395 ~ core[23ab]::iter::adapters::step_by::{impl#16}::spec_fold):       472.50µs
17:57:33|-|: 1. Decomposition: 8.29µs
17:57:33|-|: 2. Constraint:    2.88µs
17:57:33|-|: 3. Path Synthesis:17.30µs
17:57:33|-|: 4. Alias Comp:    154.45µs
17:57:33|-|: 5. Traversal/Misc:289.58µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37409 ~ core[23ab]::iter::adapters::step_by::{impl#18}::spec_fold):       470.96µs
17:57:33|-|: 1. Decomposition: 8.46µs
17:57:33|-|: 2. Constraint:    3.38µs
17:57:33|-|: 3. Path Synthesis:16.54µs
17:57:33|-|: 4. Alias Comp:    150.66µs
17:57:33|-|: 5. Traversal/Misc:291.92µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37423 ~ core[23ab]::iter::adapters::step_by::{impl#20}::spec_fold):       555.83µs
17:57:33|-|: 1. Decomposition: 8.71µs
17:57:33|-|: 2. Constraint:    3.04µs
17:57:33|-|: 3. Path Synthesis:18.05µs
17:57:33|-|: 4. Alias Comp:    178.08µs
17:57:33|-|: 5. Traversal/Misc:347.96µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:8719 ~ core[23ab]::iter::adapters::take::{impl#10}::spec_fold):       614.29µs
17:57:33|-|: 1. Decomposition: 8.00µs
17:57:33|-|: 2. Constraint:    2.54µs
17:57:33|-|: 3. Path Synthesis:18.01µs
17:57:33|-|: 4. Alias Comp:    282.98µs
17:57:33|-|: 5. Traversal/Misc:302.76µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:8941 ~ core[23ab]::iter::adapters::zip::{impl#20}::spec_fold):       432.17µs
17:57:33|-|: 1. Decomposition: 6.88µs
17:57:33|-|: 2. Constraint:    2.08µs
17:57:33|-|: 3. Path Synthesis:13.92µs
17:57:33|-|: 4. Alias Comp:    203.79µs
17:57:33|-|: 5. Traversal/Misc:205.50µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:8947 ~ core[23ab]::iter::adapters::zip::{impl#21}::spec_fold):       6.85ms
17:57:33|-|: 1. Decomposition: 17.38µs
17:57:33|-|: 2. Constraint:    46.71µs
17:57:33|-|: 3. Path Synthesis:2.75ms
17:57:33|-|: 4. Alias Comp:    3.49ms
17:57:33|-|: 5. Traversal/Misc:542.00µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:9149 ~ core[23ab]::iter::range::{impl#13}::spec_try_fold):       14.13ms
17:57:33|-|: 1. Decomposition: 17.54µs
17:57:33|-|: 2. Constraint:    14.54µs
17:57:33|-|: 3. Path Synthesis:53.16µs
17:57:33|-|: 4. Alias Comp:    11.18ms
17:57:33|-|: 5. Traversal/Misc:2.87ms
17:57:33|-|: ===========================
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37419 ~ core[23ab]::iter::adapters::step_by::{impl#20}::spec_try_fold):       643.42µs
17:57:33|-|: 1. Decomposition: 9.46µs
17:57:33|-|: 2. Constraint:    3.66µs
17:57:33|-|: 3. Path Synthesis:24.59µs
17:57:33|-|: 4. Alias Comp:    269.66µs
17:57:33|-|: 5. Traversal/Misc:336.05µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37405 ~ core[23ab]::iter::adapters::step_by::{impl#18}::spec_try_fold):       596.83µs
17:57:33|-|: 1. Decomposition: 7.63µs
17:57:33|-|: 2. Constraint:    3.29µs
17:57:33|-|: 3. Path Synthesis:22.46µs
17:57:33|-|: 4. Alias Comp:    244.16µs
17:57:33|-|: 5. Traversal/Misc:319.30µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37391 ~ core[23ab]::iter::adapters::step_by::{impl#16}::spec_try_fold):       554.50µs
17:57:33|-|: 1. Decomposition: 7.75µs
17:57:33|-|: 2. Constraint:    2.92µs
17:57:33|-|: 3. Path Synthesis:21.17µs
17:57:33|-|: 4. Alias Comp:    242.20µs
17:57:33|-|: 5. Traversal/Misc:280.46µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37377 ~ core[23ab]::iter::adapters::step_by::{impl#14}::spec_try_fold):       557.04µs
17:57:33|-|: 1. Decomposition: 7.46µs
17:57:33|-|: 2. Constraint:    3.51µs
17:57:33|-|: 3. Path Synthesis:21.58µs
17:57:33|-|: 4. Alias Comp:    240.13µs
17:57:33|-|: 5. Traversal/Misc:284.37µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37363 ~ core[23ab]::iter::adapters::step_by::{impl#12}::spec_try_fold):       578.46µs
17:57:33|-|: 1. Decomposition: 8.00µs
17:57:33|-|: 2. Constraint:    3.46µs
17:57:33|-|: 3. Path Synthesis:21.74µs
17:57:33|-|: 4. Alias Comp:    252.54µs
17:57:33|-|: 5. Traversal/Misc:292.71µs
17:57:33|-|: Total Time of DefId(0:9161 ~ core[23ab]::iter::range::{impl#14}::spec_try_fold):       10.43ms
17:57:33|-|: 1. Decomposition: 14.54µs
17:57:33|-|: 2. Constraint:    10.75µs
17:57:33|-|: 3. Path Synthesis:37.83µs
17:57:33|-|: 4. Alias Comp:    8.30ms
17:57:33|-|: 5. Traversal/Misc:2.07ms
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:10050 ~ core[23ab]::iter::traits::iterator::{impl#3}::spec_try_fold):       764.71µs
17:57:33|-|: 1. Decomposition: 8.67µs
17:57:33|-|: 2. Constraint:    3.42µs
17:57:33|-|: 3. Path Synthesis:23.54µs
17:57:33|-|: 4. Alias Comp:    391.26µs
17:57:33|-|: 5. Traversal/Misc:337.83µs
17:57:33|-|: Total Time of DefId(0:10350 ~ core[23ab]::net::parser::{impl#0}::read_number::{closure#0}):       5.31ms
17:57:33|-|: 1. Decomposition: 22.04µs
17:57:33|-|: 2. Constraint:    15.75µs
17:57:33|-|: 3. Path Synthesis:74.12µs
17:57:33|-|: 4. Alias Comp:    3.29ms
17:57:33|-|: 5. Traversal/Misc:1.91ms
17:57:33|-|: Total Time of DefId(0:37434 ~ core[23ab]::iter::adapters::step_by::{impl#21}::spec_rfold):       216.13µs
17:57:33|-|: 1. Decomposition: 5.38µs
17:57:33|-|: 2. Constraint:    1.58µs
17:57:33|-|: 3. Path Synthesis:10.76µs
17:57:33|-|: 4. Alias Comp:    81.08µs
17:57:33|-|: 5. Traversal/Misc:117.33µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37445 ~ core[23ab]::iter::adapters::step_by::{impl#22}::spec_rfold):       208.25µs
17:57:33|-|: 1. Decomposition: 5.38µs
17:57:33|-|: 2. Constraint:    1.51µs
17:57:33|-|: 3. Path Synthesis:10.46µs
17:57:33|-|: 4. Alias Comp:    78.29µs
17:57:33|-|: 5. Traversal/Misc:112.62µs
17:57:33|-|: ===========================
17:57:33|-|: Total Time of DefId(0:37456 ~ core[23ab]::iter::adapters::step_by::{impl#23}::spec_rfold):       205.96µs
17:57:33|-|: 1. Decomposition: 5.33µs
17:57:33|-|: 2. Constraint:    1.50µs
17:57:33|-|: 3. Path Synthesis:9.96µs
17:57:33|-|: 4. Alias Comp:    77.34µs
17:57:33|-|: 5. Traversal/Misc:111.83µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:37467 ~ core[23ab]::iter::adapters::step_by::{impl#24}::spec_rfold):       218.88µs
17:57:33|-|: 1. Decomposition: 5.29µs
17:57:33|-|: 2. Constraint:    1.50µs
17:57:33|-|: 3. Path Synthesis:10.29µs
17:57:33|-|: 4. Alias Comp:    89.25µs
17:57:33|-|: 5. Traversal/Misc:112.54µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:9621 ~ core[23ab]::iter::traits::double_ended::{impl#1}::spec_rfold):       286.75µs
17:57:33|-|: 1. Decomposition: 5.38µs
17:57:33|-|: 2. Constraint:    1.67µs
17:57:33|-|: 3. Path Synthesis:11.87µs
17:57:33|-|: 4. Alias Comp:    143.29µs
17:57:33|-|: 5. Traversal/Misc:124.54µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:6666 ~ core[23ab]::iter::adapters::array_chunks::{impl#8}::fold):       493.17µs
17:57:33|-|: 1. Decomposition: 8.00µs
17:57:33|-|: 2. Constraint:    2.86µs
17:57:33|-|: 3. Path Synthesis:20.30µs
17:57:33|-|: 4. Alias Comp:    239.00µs
17:57:33|-|: 5. Traversal/Misc:223.01µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:8861 ~ core[23ab]::iter::adapters::zip::{impl#4}::fold):       850.67µs
17:57:33|-|: 1. Decomposition: 8.96µs
17:57:33|-|: 2. Constraint:    2.83µs
17:57:33|-|: 3. Path Synthesis:23.46µs
17:57:33|-|: 4. Alias Comp:    346.08µs
17:57:33|-|: 5. Traversal/Misc:469.34µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:9809 ~ core[23ab]::iter::traits::iterator::Iterator::fold):       415.25µs
17:57:33|-|: 1. Decomposition: 7.33µs
17:57:33|-|: 2. Constraint:    1.91µs
17:57:33|-|: 3. Path Synthesis:13.17µs
17:57:33|-|: 4. Alias Comp:    179.54µs
17:57:33|-|: 5. Traversal/Misc:213.29µs
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41180 ~ core[23ab]::slice::iter::{impl#166}::fold):       4.40ms
17:57:38|-|: 1. Decomposition: 10.96µs
17:57:38|-|: 2. Constraint:    70.30µs
17:57:38|-|: 3. Path Synthesis:82.04µs
17:57:38|-|: 4. Alias Comp:    2.15ms
17:57:38|-|: 5. Traversal/Misc:2.08ms
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41245 ~ core[23ab]::slice::iter::{impl#174}::fold):       4.34ms
17:57:38|-|: 1. Decomposition: 11.08µs
17:57:38|-|: 2. Constraint:    45.92µs
17:57:38|-|: 3. Path Synthesis:80.00µs
17:57:38|-|: 4. Alias Comp:    2.26ms
17:57:38|-|: 5. Traversal/Misc:1.95ms
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:12973 ~ core[23ab]::slice::sort::select::partition_at_index_loop):       427.13ms
17:57:38|-|: 1. Decomposition: 15.42µs
17:57:38|-|: 2. Constraint:    713.51µs
17:57:38|-|: 3. Path Synthesis:4.12ms
17:57:38|-|: 4. Alias Comp:    396.89ms
17:57:38|-|: 5. Traversal/Misc:25.39ms
17:57:31|-|: === Performance Profiling ===
17:57:31|-|: Total Time of DefId(0:18028 ~ core[23ab]::num::bignum::{impl#4}::sub):       335.96µs
17:57:31|-|: 1. Decomposition: 6.42µs
17:57:31|-|: 2. Constraint:    877.00ns
17:57:31|-|: 3. Path Synthesis:8.00µs
17:57:31|-|: 4. Alias Comp:    258.04µs
17:57:31|-|: 5. Traversal/Misc:62.63µs
17:57:31|-|: Total Time of DefId(0:18080 ~ core[23ab]::num::bignum::tests::{impl#0}::sub):       340.00µs
17:57:31|-|: 1. Decomposition: 5.83µs
17:57:31|-|: 2. Constraint:    835.00ns
17:57:31|-|: 3. Path Synthesis:7.71µs
17:57:31|-|: 4. Alias Comp:    263.29µs
17:57:31|-|: 5. Traversal/Misc:62.33µs
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41196 ~ core[23ab]::slice::iter::{impl#166}::rposition):       855.33µs
17:57:38|-|: 1. Decomposition: 8.75µs
17:57:38|-|: 2. Constraint:    28.92µs
17:57:38|-|: 3. Path Synthesis:22.50µs
17:57:38|-|: 4. Alias Comp:    488.92µs
17:57:38|-|: 5. Traversal/Misc:306.25µs
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41261 ~ core[23ab]::slice::iter::{impl#174}::rposition):       1.06ms
17:57:38|-|: 1. Decomposition: 9.00µs
17:57:38|-|: 2. Constraint:    33.38µs
17:57:38|-|: 3. Path Synthesis:26.92µs
17:57:38|-|: 4. Alias Comp:    606.74µs
17:57:38|-|: 5. Traversal/Misc:386.38µs
17:57:31|-|: === Performance Profiling ===
17:57:31|-|: Total Time of DefId(0:18022 ~ core[23ab]::num::bignum::{impl#4}::add):       475.50µs
17:57:31|-|: 1. Decomposition: 7.58µs
17:57:31|-|: 2. Constraint:    1.12µs
17:57:31|-|: 3. Path Synthesis:8.33µs
17:57:31|-|: 4. Alias Comp:    363.50µs
17:57:31|-|: 5. Traversal/Misc:94.96µs
17:57:31|-|: === Performance Profiling ===
17:57:31|-|: Total Time of DefId(0:18074 ~ core[23ab]::num::bignum::tests::{impl#0}::add):       461.00µs
17:57:31|-|: 1. Decomposition: 6.96µs
17:57:31|-|: 2. Constraint:    789.00ns
17:57:31|-|: 3. Path Synthesis:7.38µs
17:57:31|-|: 4. Alias Comp:    355.38µs
17:57:31|-|: 5. Traversal/Misc:90.50µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:2250 ~ core[23ab]::mem::maybe_uninit::{impl#8}::spec_fill):       870.79µs
17:57:33|-|: 1. Decomposition: 8.96µs
17:57:33|-|: 2. Constraint:    3.42µs
17:57:33|-|: 3. Path Synthesis:18.46µs
17:57:33|-|: 4. Alias Comp:    550.99µs
17:57:33|-|: 5. Traversal/Misc:288.96µs
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:14354 ~ core[23ab]::slice::specialize::{impl#0}::spec_fill):       354.63µs
17:57:38|-|: 1. Decomposition: 7.63µs
17:57:38|-|: 2. Constraint:    1.71µs
17:57:38|-|: 3. Path Synthesis:11.25µs
17:57:38|-|: 4. Alias Comp:    185.08µs
17:57:38|-|: 5. Traversal/Misc:148.96µs
17:57:38|-|: Total Time of DefId(0:14357 ~ core[23ab]::slice::specialize::{impl#1}::spec_fill):       132.75µs
17:57:38|-|: 1. Decomposition: 6.42µs
17:57:38|-|: 2. Constraint:    1.04µs
17:57:38|-|: 3. Path Synthesis:11.04µs
17:57:38|-|: 4. Alias Comp:    55.25µs
17:57:38|-|: 5. Traversal/Misc:59.00µs
17:57:38|-|: Total Time of DefId(0:41446 ~ core[23ab]::slice::specialize::{impl#4}::spec_fill):       276.17µs
17:57:38|-|: 1. Decomposition: 8.50µs
17:57:38|-|: 2. Constraint:    1.96µs
17:57:38|-|: 3. Path Synthesis:12.29µs
17:57:38|-|: 4. Alias Comp:    62.91µs
17:57:38|-|: 5. Traversal/Misc:190.50µs
17:57:38|-|: ===========================
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41449 ~ core[23ab]::slice::specialize::{impl#5}::spec_fill):       265.17µs
17:57:38|-|: 1. Decomposition: 8.13µs
17:57:38|-|: 2. Constraint:    1.83µs
17:57:38|-|: 3. Path Synthesis:10.96µs
17:57:38|-|: 4. Alias Comp:    58.79µs
17:57:38|-|: 5. Traversal/Misc:185.47µs
17:57:38|-|: ===========================
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41452 ~ core[23ab]::slice::specialize::{impl#6}::spec_fill):       266.88µs
17:57:38|-|: 1. Decomposition: 7.71µs
17:57:38|-|: 2. Constraint:    1.88µs
17:57:38|-|: 3. Path Synthesis:10.88µs
17:57:38|-|: 4. Alias Comp:    62.74µs
17:57:38|-|: 5. Traversal/Misc:183.67µs
17:57:38|-|: ===========================
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41455 ~ core[23ab]::slice::specialize::{impl#7}::spec_fill):       301.63µs
17:57:38|-|: 1. Decomposition: 8.42µs
17:57:38|-|: 2. Constraint:    2.00µs
17:57:38|-|: 3. Path Synthesis:12.96µs
17:57:38|-|: 4. Alias Comp:    76.04µs
17:57:38|-|: 5. Traversal/Misc:202.21µs
17:57:38|-|: ===========================
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41458 ~ core[23ab]::slice::specialize::{impl#8}::spec_fill):       279.33µs
17:57:38|-|: 1. Decomposition: 7.88µs
17:57:38|-|: 2. Constraint:    1.87µs
17:57:38|-|: 3. Path Synthesis:11.62µs
17:57:38|-|: 4. Alias Comp:    64.47µs
17:57:38|-|: 5. Traversal/Misc:193.50µs
17:57:38|-|: ===========================
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41461 ~ core[23ab]::slice::specialize::{impl#9}::spec_fill):       273.42µs
17:57:38|-|: 1. Decomposition: 7.67µs
17:57:38|-|: 2. Constraint:    1.46µs
17:57:38|-|: 3. Path Synthesis:11.00µs
17:57:38|-|: 4. Alias Comp:    62.84µs
17:57:38|-|: 5. Traversal/Misc:190.46µs
17:57:38|-|: ===========================
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41464 ~ core[23ab]::slice::specialize::{impl#10}::spec_fill):       276.46µs
17:57:38|-|: 1. Decomposition: 7.83µs
17:57:38|-|: 2. Constraint:    1.46µs
17:57:38|-|: 3. Path Synthesis:10.71µs
17:57:38|-|: 4. Alias Comp:    61.45µs
17:57:38|-|: 5. Traversal/Misc:195.00µs
17:57:38|-|: ===========================
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41467 ~ core[23ab]::slice::specialize::{impl#11}::spec_fill):       271.38µs
17:57:38|-|: 1. Decomposition: 7.58µs
17:57:38|-|: 2. Constraint:    1.59µs
17:57:38|-|: 3. Path Synthesis:10.79µs
17:57:38|-|: 4. Alias Comp:    61.79µs
17:57:38|-|: 5. Traversal/Misc:189.62µs
17:57:38|-|: ===========================
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41470 ~ core[23ab]::slice::specialize::{impl#12}::spec_fill):       268.88µs
17:57:38|-|: 1. Decomposition: 7.54µs
17:57:38|-|: 2. Constraint:    1.63µs
17:57:38|-|: 3. Path Synthesis:11.00µs
17:57:38|-|: 4. Alias Comp:    60.37µs
17:57:38|-|: 5. Traversal/Misc:188.34µs
17:57:38|-|: ===========================
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41473 ~ core[23ab]::slice::specialize::{impl#13}::spec_fill):       266.63µs
17:57:38|-|: 1. Decomposition: 9.13µs
17:57:38|-|: 2. Constraint:    2.04µs
17:57:38|-|: 3. Path Synthesis:11.13µs
17:57:38|-|: 4. Alias Comp:    60.74µs
17:57:38|-|: 5. Traversal/Misc:183.59µs
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41194 ~ core[23ab]::slice::iter::{impl#166}::position):       729.29µs
17:57:38|-|: 1. Decomposition: 8.21µs
17:57:38|-|: 2. Constraint:    80.08µs
17:57:38|-|: 3. Path Synthesis:22.66µs
17:57:38|-|: 4. Alias Comp:    414.79µs
17:57:38|-|: 5. Traversal/Misc:203.55µs
17:57:38|-|: === Performance Profiling ===
17:57:38|-|: Total Time of DefId(0:41259 ~ core[23ab]::slice::iter::{impl#174}::position):       801.46µs
17:57:38|-|: 1. Decomposition: 8.46µs
17:57:38|-|: 2. Constraint:    66.96µs
17:57:38|-|: 3. Path Synthesis:24.51µs
17:57:38|-|: 4. Alias Comp:    471.83µs
17:57:38|-|: 5. Traversal/Misc:229.71µs
17:57:31|-|: === Performance Profiling ===
17:57:31|-|: Total Time of DefId(0:18028 ~ core[23ab]::num::bignum::{impl#4}::sub):       335.96µs
17:57:31|-|: 1. Decomposition: 6.42µs
17:57:31|-|: 2. Constraint:    877.00ns
17:57:31|-|: 3. Path Synthesis:8.00µs
17:57:31|-|: 4. Alias Comp:    258.04µs
17:57:31|-|: 5. Traversal/Misc:62.63µs
17:57:31|-|: === Performance Profiling ===
17:57:31|-|: Total Time of DefId(0:18080 ~ core[23ab]::num::bignum::tests::{impl#0}::sub):       340.00µs
17:57:31|-|: 1. Decomposition: 5.83µs
17:57:31|-|: 2. Constraint:    835.00ns
17:57:31|-|: 3. Path Synthesis:7.71µs
17:57:31|-|: 4. Alias Comp:    263.29µs
17:57:31|-|: 5. Traversal/Misc:62.33µs
17:57:33|-|: === Performance Profiling ===
17:57:33|-|: Total Time of DefId(0:12579 ~ core[23ab]::hash::sip::{impl#5}::write):       555.54µs
17:57:33|-|: 1. Decomposition: 29.92µs
17:57:33|-|: 2. Constraint:    4.34µs
17:57:33|-|: 3. Path Synthesis:26.17µs
17:57:33|-|: 4. Alias Comp:    151.20µs
17:57:33|-|: 5. Traversal/Misc:343.92µs
17:57:39|-|: === Performance Profiling ===
17:57:39|-|: Total Time of DefId(0:15813 ~ core[23ab]::wtf8::{impl#3}::fmt):       1.33ms
17:57:39|-|: 1. Decomposition: 13.83µs
17:57:39|-|: 2. Constraint:    4.70µs
17:57:39|-|: 3. Path Synthesis:19.42µs
17:57:39|-|: 4. Alias Comp:    746.95µs
17:57:39|-|: 5. Traversal/Misc:545.84µs
"""

def parse_time(time_str):
    match = re.search(r'([\d\.]+)(ns|µs|us|ms|s)', time_str)
    if not match:
        return 0.0
    
    value = float(match.group(1))
    unit = match.group(2)
    
    if unit == 'ns':
        return value / 1000.0
    elif unit == 'µs' or unit == 'us':
        return value
    elif unit == 'ms':
        return value * 1000.0
    elif unit == 's':
        return value * 1000000.0
    return 0.0

def calculate_averages(log_text):
    data = {
        "Total Time": [],
        "1. Decomposition": [],
        "2. Constraint": [],
        "3. Path Synthesis": [],
        "4. Alias Comp": [],
        "5. Traversal/Misc": []
    }
    
    lines = log_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        
        if "Total Time" in line:
            data["Total Time"].append(parse_time(line))
        elif "1. Decomposition" in line:
            data["1. Decomposition"].append(parse_time(line))
        elif "2. Constraint" in line:
            data["2. Constraint"].append(parse_time(line))
        elif "3. Path Synthesis" in line:
            data["3. Path Synthesis"].append(parse_time(line))
        elif "4. Alias Comp" in line:
            data["4. Alias Comp"].append(parse_time(line))
        elif "5. Traversal/Misc" in line:
            data["5. Traversal/Misc"].append(parse_time(line))
            
    print(f"{'Category':<20} | {'Count':<5} | {'Avg (µs)':<12} | {'Avg (ms)':<12}")
    print("-" * 55)
    
    for category, values in data.items():
        if values:
            avg_us = sum(values) / len(values)
            avg_ms = avg_us / 1000.0
            print(f"{category:<20} | {len(values):<5} | {avg_us:<12.2f} | {avg_ms:<12.4f}")
        else:
            print(f"{category:<20} | 0     | N/A          | N/A")

if __name__ == "__main__":
    calculate_averages(log_data0)