// 数据存储
const STORAGE_KEY = 'lucky-feet-transactions';

// 从wave_data.json导入真实数据（内嵌数据）
const waveData = [
    {
        "date": "2026-01-01",
        "description": "Debit Arrangement AccountLoan payment",
        "category": "other",
        "type": "expense",
        "amount": 259.11
    },
    {
        "date": "2026-01-01",
        "description": "Cheque cleared Cheque 145",
        "category": "salary",
        "type": "expense",
        "amount": 358.55
    },
    {
        "date": "2026-01-02",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 207.0
    },
    {
        "date": "2026-01-02",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 61.15
    },
    {
        "date": "2026-01-05",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 113.36
    },
    {
        "date": "2026-01-05",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 514.0
    },
    {
        "date": "2026-01-06",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 223.65
    },
    {
        "date": "2026-01-06",
        "description": "Preauthorized payment VANCITY VISA AUTO PAYMNT VANCITY VISA AUTO PAYMNT",
        "category": "other",
        "type": "expense",
        "amount": 129.13
    },
    {
        "date": "2026-01-08",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 151.2
    },
    {
        "date": "2026-01-12",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 566.05
    },
    {
        "date": "2026-01-14",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 146.5
    },
    {
        "date": "2026-01-15",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 151.75
    },
    {
        "date": "2026-01-16",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 229.95
    },
    {
        "date": "2026-01-19",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-01-19",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 230.5
    },
    {
        "date": "2026-01-19",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 32.48
    },
    {
        "date": "2026-01-20",
        "description": "Preauthorized payment SHAW CABLESYSTEMS G.P. SHAW CABLESYSTEMS G.P.",
        "category": "utilities",
        "type": "expense",
        "amount": 87.31
    },
    {
        "date": "2026-01-20",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 224.2
    },
    {
        "date": "2026-01-21",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-01-21",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 81.9
    },
    {
        "date": "2026-01-22",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 166.0
    },
    {
        "date": "2026-01-23",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 234.2
    },
    {
        "date": "2026-01-26",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 226.8
    },
    {
        "date": "2026-01-26",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 151.24
    },
    {
        "date": "2026-01-27",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 136.0
    },
    {
        "date": "2026-01-28",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 378.55
    },
    {
        "date": "2026-01-29",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 468.95
    },
    {
        "date": "2026-01-29",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 0.68
    },
    {
        "date": "2026-01-30",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 192.25
    },
    {
        "date": "2026-01-30",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 5.9
    },
    {
        "date": "2026-01-31",
        "description": "Charges applied to account Periodic Flat FeeCAPITALISE",
        "category": "other",
        "type": "expense",
        "amount": 8.0
    },
    {
        "date": "2026-02-01",
        "description": "Debit Arrangement AccountLoan payment",
        "category": "other",
        "type": "expense",
        "amount": 259.11
    },
    {
        "date": "2026-02-02",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 439.5
    },
    {
        "date": "2026-02-02",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-02-02",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 75.53
    },
    {
        "date": "2026-02-03",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 75.6
    },
    {
        "date": "2026-02-04",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 75.6
    },
    {
        "date": "2026-02-05",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 567.5
    },
    {
        "date": "2026-02-06",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 305.17
    },
    {
        "date": "2026-02-06",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 148.6
    },
    {
        "date": "2026-02-06",
        "description": "Preauthorized payment VANCITY VISA AUTO PAYMNT VANCITY VISA AUTO PAYMNT",
        "category": "other",
        "type": "expense",
        "amount": 357.29
    },
    {
        "date": "2026-02-09",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 507.15
    },
    {
        "date": "2026-02-10",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 151.2
    },
    {
        "date": "2026-02-11",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 345.5
    },
    {
        "date": "2026-02-12",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 166.0
    },
    {
        "date": "2026-02-13",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 368.75
    },
    {
        "date": "2026-02-17",
        "description": "Cheque cleared Cheque 144",
        "category": "salary",
        "type": "expense",
        "amount": 2403.35
    },
    {
        "date": "2026-02-17",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 916.85
    },
    {
        "date": "2026-02-17",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 32.48
    },
    {
        "date": "2026-02-18",
        "description": "Preauthorized payment B.C. HYDRO POWER AUTHORI B.C. HYDRO POWER AUTHORI",
        "category": "utilities",
        "type": "expense",
        "amount": 346.71
    },
    {
        "date": "2026-02-18",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 249.4
    },
    {
        "date": "2026-02-19",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 166.0
    },
    {
        "date": "2026-02-20",
        "description": "Preauthorized payment SHAW CABLESYSTEMS G.P. SHAW CABLESYSTEMS G.P.",
        "category": "utilities",
        "type": "expense",
        "amount": 87.31
    },
    {
        "date": "2026-02-20",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 189.1
    },
    {
        "date": "2026-02-23",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 226.8
    },
    {
        "date": "2026-02-24",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 72.76
    },
    {
        "date": "2026-02-25",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 151.2
    },
    {
        "date": "2026-02-26",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 317.2
    },
    {
        "date": "2026-02-26",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 0.42
    },
    {
        "date": "2026-02-27",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 78.63
    },
    {
        "date": "2026-02-27",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 239.4
    },
    {
        "date": "2026-02-27",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 6.37
    },
    {
        "date": "2026-02-28",
        "description": "Charges applied to account Periodic Flat FeeCAPITALISE",
        "category": "other",
        "type": "expense",
        "amount": 8.0
    },
    {
        "date": "2026-03-01",
        "description": "Debit Arrangement AccountLoan payment",
        "category": "other",
        "type": "expense",
        "amount": 259.11
    },
    {
        "date": "2026-03-02",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 369.8
    },
    {
        "date": "2026-03-02",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 95.65
    },
    {
        "date": "2026-03-03",
        "description": "Cheque cleared Cheque 148",
        "category": "salary",
        "type": "expense",
        "amount": 263.6
    },
    {
        "date": "2026-03-04",
        "description": "Cheque deposit-branch",
        "category": "other",
        "type": "income",
        "amount": 83.24
    },
    {
        "date": "2026-03-04",
        "description": "Charges applied to account Immediate Charge for CR TxnC",
        "category": "other",
        "type": "expense",
        "amount": 1.25
    },
    {
        "date": "2026-03-04",
        "description": "Bill payment 0001 749843710RT0001",
        "category": "other",
        "type": "expense",
        "amount": 83.24
    },
    {
        "date": "2026-03-05",
        "description": "Cheque cleared Cheque 149",
        "category": "salary",
        "type": "expense",
        "amount": 83.24
    },
    {
        "date": "2026-03-05",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 229.0
    },
    {
        "date": "2026-03-06",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 143.6
    },
    {
        "date": "2026-03-09",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 113.01
    },
    {
        "date": "2026-03-09",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 506.9
    },
    {
        "date": "2026-03-10",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 239.4
    },
    {
        "date": "2026-03-10",
        "description": "Preauthorized payment VANCITY VISA AUTO PAYMNT VANCITY VISA AUTO PAYMNT",
        "category": "other",
        "type": "expense",
        "amount": 678.34
    },
    {
        "date": "2026-03-11",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 199.0
    },
    {
        "date": "2026-03-12",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 323.25
    },
    {
        "date": "2026-03-13",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 368.55
    },
    {
        "date": "2026-03-16",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 72.76
    },
    {
        "date": "2026-03-16",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 529.67
    },
    {
        "date": "2026-03-17",
        "description": "Cheque cleared Cheque 150",
        "category": "salary",
        "type": "expense",
        "amount": 1518.0
    },
    {
        "date": "2026-03-17",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 318.15
    },
    {
        "date": "2026-03-17",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 32.48
    },
    {
        "date": "2026-03-19",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 833.8
    },
    {
        "date": "2026-03-20",
        "description": "Preauthorized payment SHAW CABLESYSTEMS G.P. SHAW CABLESYSTEMS G.P.",
        "category": "utilities",
        "type": "expense",
        "amount": 87.31
    },
    {
        "date": "2026-03-20",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 78.75
    },
    {
        "date": "2026-03-23",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 459.9
    },
    {
        "date": "2026-03-24",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 346.5
    },
    {
        "date": "2026-03-26",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 226.8
    },
    {
        "date": "2026-03-27",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 163.8
    },
    {
        "date": "2026-03-30",
        "description": "e-Transfer credit Ref 20260330144602812055 LEICAO",
        "category": "income",
        "type": "income",
        "amount": 73.5
    },
    {
        "date": "2026-03-30",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 650.25
    },
    {
        "date": "2026-03-30",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 0.68
    },
    {
        "date": "2026-03-31",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 4.83
    },
    {
        "date": "2026-03-31",
        "description": "Charges applied to account Periodic Flat FeeCAPITALISE",
        "category": "other",
        "type": "expense",
        "amount": 8.0
    },
    {
        "date": "2026-04-01",
        "description": "Debit Arrangement AccountLoan payment",
        "category": "other",
        "type": "expense",
        "amount": 259.11
    },
    {
        "date": "2026-04-01",
        "description": "Cheque cleared Cheque 151",
        "category": "salary",
        "type": "expense",
        "amount": 967.75
    },
    {
        "date": "2026-04-01",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 107.68
    },
    {
        "date": "2026-04-02",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 148.6
    },
    {
        "date": "2026-04-06",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 380.4
    },
    {
        "date": "2026-04-07",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 83.28
    },
    {
        "date": "2026-04-07",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 73.0
    },
    {
        "date": "2026-04-08",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 180.1
    },
    {
        "date": "2026-04-08",
        "description": "Preauthorized payment VANCITY VISA AUTO PAYMNT VANCITY VISA AUTO PAYMNT",
        "category": "other",
        "type": "expense",
        "amount": 340.19
    },
    {
        "date": "2026-04-09",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 491.4
    },
    {
        "date": "2026-04-10",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 73.0
    },
    {
        "date": "2026-04-11",
        "description": "Cheque cleared Cheque 117",
        "category": "salary",
        "type": "expense",
        "amount": 2600.0
    },
    {
        "date": "2026-04-11",
        "description": "Cheque cleared Cheque 118",
        "category": "salary",
        "type": "expense",
        "amount": 2600.0
    },
    {
        "date": "2026-04-11",
        "description": "Cheque cleared Cheque 119",
        "category": "salary",
        "type": "expense",
        "amount": 2600.0
    },
    {
        "date": "2026-04-11",
        "description": "Cheque cleared Cheque 120",
        "category": "salary",
        "type": "expense",
        "amount": 2600.0
    },
    {
        "date": "2026-04-11",
        "description": "Cheque cleared Cheque 121",
        "category": "salary",
        "type": "expense",
        "amount": 2600.0
    },
    {
        "date": "2026-04-11",
        "description": "Cheque cleared Cheque 122",
        "category": "salary",
        "type": "expense",
        "amount": 2600.0
    },
    {
        "date": "2026-04-13",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 352.6
    },
    {
        "date": "2026-04-14",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 418.0
    },
    {
        "date": "2026-04-15",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 146.0
    },
    {
        "date": "2026-04-15",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 19.65
    },
    {
        "date": "2026-04-16",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 606.0
    },
    {
        "date": "2026-04-17",
        "description": "Cheque cleared Cheque 167",
        "category": "salary",
        "type": "expense",
        "amount": 1136.75
    },
    {
        "date": "2026-04-17",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 229.0
    },
    {
        "date": "2026-04-17",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 32.48
    },
    {
        "date": "2026-04-20",
        "description": "Preauthorized payment SHAW CABLESYSTEMS G.P. SHAW CABLESYSTEMS G.P.",
        "category": "utilities",
        "type": "expense",
        "amount": 87.31
    },
    {
        "date": "2026-04-20",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 88.1
    },
    {
        "date": "2026-04-20",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 599.05
    },
    {
        "date": "2026-04-21",
        "description": "Preauthorized payment B.C. HYDRO POWER AUTHORI B.C. HYDRO POWER AUTHORI",
        "category": "utilities",
        "type": "expense",
        "amount": 320.27
    },
    {
        "date": "2026-04-21",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 440.0
    },
    {
        "date": "2026-04-22",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 75.6
    },
    {
        "date": "2026-04-23",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 308.7
    },
    {
        "date": "2026-04-24",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 151.5
    },
    {
        "date": "2026-04-28",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 287.2
    },
    {
        "date": "2026-04-29",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 209.0
    },
    {
        "date": "2026-04-29",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 0.62
    },
    {
        "date": "2026-04-30",
        "description": "Charges applied to account Periodic Flat FeeCAPITALISE",
        "category": "other",
        "type": "expense",
        "amount": 8.0
    },
    {
        "date": "2026-04-30",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 2.23
    },
    {
        "date": "2026-05-01",
        "description": "Debit Arrangement AccountLoan payment",
        "category": "other",
        "type": "expense",
        "amount": 259.11
    },
    {
        "date": "2026-05-01",
        "description": "Cheque cleared Cheque 168",
        "category": "salary",
        "type": "expense",
        "amount": 1524.0
    },
    {
        "date": "2026-05-01",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 171.2
    },
    {
        "date": "2026-05-01",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 111.1
    },
    {
        "date": "2026-05-04",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 1192.35
    },
    {
        "date": "2026-05-05",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 289.75
    },
    {
        "date": "2026-05-06",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 62.85
    },
    {
        "date": "2026-05-06",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-05-06",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 78.75
    },
    {
        "date": "2026-05-07",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 83.28
    },
    {
        "date": "2026-05-07",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 163.8
    },
    {
        "date": "2026-05-07",
        "description": "Preauthorized payment VANCITY VISA AUTO PAYMNT VANCITY VISA AUTO PAYMNT",
        "category": "other",
        "type": "expense",
        "amount": 723.18
    },
    {
        "date": "2026-05-08",
        "description": "Cheque cleared Cheque 154",
        "category": "salary",
        "type": "expense",
        "amount": 2600.0
    },
    {
        "date": "2026-05-08",
        "description": "Cheque cleared Cheque 152",
        "category": "salary",
        "type": "expense",
        "amount": 2600.0
    },
    {
        "date": "2026-05-08",
        "description": "Cheque cleared Cheque 153",
        "category": "salary",
        "type": "expense",
        "amount": 2600.0
    },
    {
        "date": "2026-05-08",
        "description": "Charges applied to account Overdraft FeeCAPITALISE ACTI",
        "category": "other",
        "type": "expense",
        "amount": 5.0
    },
    {
        "date": "2026-05-08",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-05-08",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 75.6
    },
    {
        "date": "2026-05-08",
        "description": "Reversal of Overdraft Fee",
        "category": "other",
        "type": "expense",
        "amount": 5.0
    },
    {
        "date": "2026-05-08",
        "description": "Returned item credit",
        "category": "income",
        "type": "income",
        "amount": 2600.0
    },
    {
        "date": "2026-05-08",
        "description": "Debit Arrangement AccountItem returned unpaid",
        "category": "other",
        "type": "expense",
        "amount": 48.0
    },
    {
        "date": "2026-05-11",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-05-11",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-05-11",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 514.6
    },
    {
        "date": "2026-05-12",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-05-12",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 73.0
    },
    {
        "date": "2026-05-13",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 227.35
    },
    {
        "date": "2026-05-13",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 78.98
    },
    {
        "date": "2026-05-14",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 377.6
    },
    {
        "date": "2026-05-15",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 94.5
    },
    {
        "date": "2026-05-19",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 1199.2
    },
    {
        "date": "2026-05-19",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 32.48
    },
    {
        "date": "2026-05-20",
        "description": "Preauthorized payment SHAW CABLESYSTEMS G.P. SHAW CABLESYSTEMS G.P.",
        "category": "utilities",
        "type": "expense",
        "amount": 87.31
    },
    {
        "date": "2026-05-20",
        "description": "Cheque cleared Cheque 169",
        "category": "salary",
        "type": "expense",
        "amount": 2192.97
    },
    {
        "date": "2026-05-20",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 151.75
    },
    {
        "date": "2026-05-21",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-05-21",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 159.2
    },
    {
        "date": "2026-05-22",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 72.76
    },
    {
        "date": "2026-05-22",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 239.0
    },
    {
        "date": "2026-05-24",
        "description": "e-Transfer credit Ref 20260524161811818252 ZHIYILIU",
        "category": "income",
        "type": "income",
        "amount": 73.0
    },
    {
        "date": "2026-05-25",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 800.95
    },
    {
        "date": "2026-05-26",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 302.95
    },
    {
        "date": "2026-05-27",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 75.6
    },
    {
        "date": "2026-05-28",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 239.0
    },
    {
        "date": "2026-05-28",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 0.97
    },
    {
        "date": "2026-05-29",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 138.6
    },
    {
        "date": "2026-05-29",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 2.72
    },
    {
        "date": "2026-05-31",
        "description": "Charges applied to account Periodic Flat FeeCAPITALISE",
        "category": "other",
        "type": "expense",
        "amount": 8.0
    },
    {
        "date": "2026-06-01",
        "description": "Debit Arrangement AccountLoan payment",
        "category": "other",
        "type": "expense",
        "amount": 259.11
    },
    {
        "date": "2026-06-01",
        "description": "Cash deposit-branch",
        "category": "income",
        "type": "income",
        "amount": 1200.0
    },
    {
        "date": "2026-06-01",
        "description": "Charges applied to account Immediate Charge for CR TxnC",
        "category": "other",
        "type": "expense",
        "amount": 1.25
    },
    {
        "date": "2026-06-01",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 792.0
    },
    {
        "date": "2026-06-01",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 75.47
    },
    {
        "date": "2026-06-01",
        "description": "Preauthorized payment FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "other",
        "type": "expense",
        "amount": 131.36
    },
    {
        "date": "2026-06-02",
        "description": "Cheque cleared Cheque 170",
        "category": "salary",
        "type": "expense",
        "amount": 1963.0
    },
    {
        "date": "2026-06-02",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 499.55
    },
    {
        "date": "2026-06-03",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 219.2
    },
    {
        "date": "2026-06-04",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 437.6
    },
    {
        "date": "2026-06-05",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 435.33
    },
    {
        "date": "2026-06-08",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 83.28
    },
    {
        "date": "2026-06-08",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 659.0
    },
    {
        "date": "2026-06-08",
        "description": "Preauthorized payment VANCITY VISA AUTO PAYMNT VANCITY VISA AUTO PAYMNT",
        "category": "other",
        "type": "expense",
        "amount": 1268.91
    },
    {
        "date": "2026-06-09",
        "description": "Preauthorized credit IOT PAY TECHNOLOGIES INC IOT PAY TECHNOLOGIES INC",
        "category": "income",
        "type": "income",
        "amount": 151.24
    },
    {
        "date": "2026-06-09",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 216.0
    },
    {
        "date": "2026-06-11",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 219.0
    },
    {
        "date": "2026-06-12",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 552.35
    },
    {
        "date": "2026-06-15",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 430.75
    },
    {
        "date": "2026-06-16",
        "description": "Cheque cleared Cheque 171",
        "category": "salary",
        "type": "expense",
        "amount": 2219.2
    },
    {
        "date": "2026-06-16",
        "description": "Preauthorized credit FIRST DATA CANADA(J) FIRST DATA CANADA(J)",
        "category": "income",
        "type": "income",
        "amount": 141.0
    }
];

sampleTransactions = waveData.map((t, i) => ({
    id: i + 1,
    date: t.date,
    description: t.description,
    type: t.type,
    category: t.category,
    amount: t.amount,
    note: ''
}));

// 同时保存到localStorage
localStorage.setItem(STORAGE_KEY, JSON.stringify(sampleTransactions));


// 获取数据
function getTransactions() {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : sampleTransactions;
}

// 保存数据
function saveTransactions(transactions) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(transactions));
}

// 导航切换
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = link.dataset.tab;
        
        // 更新导航高亮
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // 切换内容
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.getElementById(tab).classList.add('active');
        
        // 刷新数据
        if (tab === 'dashboard') updateDashboard();
        if (tab === 'transactions') renderTransactions();
    });
});

// 设置默认日期
document.getElementById('date').value = new Date().toISOString().split('T')[0];
document.getElementById('month-filter').value = new Date().toISOString().slice(0, 7);
document.getElementById('report-month').value = new Date().toISOString().slice(0, 7);

// 表单提交
document.getElementById('transaction-form').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const editId = document.getElementById('edit-id').value;
    const transaction = {
        id: editId ? parseInt(editId) : Date.now(),
        date: document.getElementById('date').value,
        description: document.getElementById('description').value,
        type: document.getElementById('type').value,
        category: document.getElementById('category').value,
        amount: parseFloat(document.getElementById('amount').value),
        note: document.getElementById('note').value,
    };
    
    let transactions = getTransactions();
    
    if (editId) {
        // 编辑模式
        const index = transactions.findIndex(t => t.id === parseInt(editId));
        if (index !== -1) transactions[index] = transaction;
    } else {
        // 新增模式
        transactions.push(transaction);
    }
    
    saveTransactions(transactions);
    document.getElementById('transaction-form').reset();
    document.getElementById('edit-id').value = '';
    document.getElementById('form-title').textContent = '添加交易';
    document.getElementById('date').value = new Date().toISOString().split('T')[0];
    
    alert('保存成功！');
    updateDashboard();
});

// 渲染交易列表
function renderTransactions() {
    const transactions = getTransactions();
    const tbody = document.getElementById('transaction-list');
    tbody.innerHTML = '';
    
    transactions.sort((a, b) => new Date(b.date) - new Date(a.date)).forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${t.date}</td>
            <td>${t.description}</td>
            <td>${t.category}</td>
            <td class="${t.type}">${t.type === 'income' ? '收入' : '支出'}</td>
            <td class="${t.type}">$${t.amount.toFixed(2)}</td>
            <td>
                <button onclick="editTransaction(${t.id})" class="btn-edit">编辑</button>
                <button onclick="deleteTransaction(${t.id})" class="btn-delete">删除</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// 编辑交易
function editTransaction(id) {
    const transactions = getTransactions();
    const t = transactions.find(tr => tr.id === id);
    if (!t) return;
    
    document.getElementById('edit-id').value = t.id;
    document.getElementById('date').value = t.date;
    document.getElementById('description').value = t.description;
    document.getElementById('type').value = t.type;
    document.getElementById('category').value = t.category;
    document.getElementById('amount').value = t.amount;
    document.getElementById('note').value = t.note || '';
    document.getElementById('form-title').textContent = '编辑交易';
    
    // 切换到添加页面
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelector('[data-tab="add"]').classList.add('active');
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.getElementById('add').classList.add('active');
}

// 删除交易
function deleteTransaction(id) {
    if (!confirm('确定删除这条记录？')) return;
    
    let transactions = getTransactions();
    transactions = transactions.filter(t => t.id !== id);
    saveTransactions(transactions);
    renderTransactions();
    updateDashboard();
}

// 更新仪表盘
function updateDashboard() {
    const transactions = getTransactions();
    const month = new Date().toISOString().slice(0, 7);
    
    const monthTxns = transactions.filter(t => t.date.startsWith(month));
    const income = monthTxns.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0);
    const expense = monthTxns.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);
    
    document.getElementById('month-income').textContent = `$${income.toFixed(2)}`;
    document.getElementById('month-expense').textContent = `$${expense.toFixed(2)}`;
    document.getElementById('month-balance').textContent = `$${(income - expense).toFixed(2)}`;
    document.getElementById('month-count').textContent = monthTxns.length;
}

// 生成报表
document.getElementById('generate-report').addEventListener('click', () => {
    const transactions = getTransactions();
    const month = document.getElementById('report-month').value;
    const type = document.getElementById('report-type').value;
    
    let filtered = transactions;
    if (month) filtered = transactions.filter(t => t.date.startsWith(month));
    
    // 按分类汇总
    const categoryTotals = {};
    filtered.forEach(t => {
        if (!categoryTotals[t.category]) categoryTotals[t.category] = { income: 0, expense: 0 };
        categoryTotals[t.category][t.type] += t.amount;
    });
    
    // 渲染数据表格
    const reportData = document.getElementById('report-data');
    reportData.innerHTML = '<h2>分类汇总</h2><table class="transaction-table"><thead><tr><th>分类</th><th>收入</th><th>支出</th><th>净额</th></tr></thead><tbody>';
    
    Object.entries(categoryTotals).forEach(([cat, totals]) => {
        const net = totals.income - totals.expense;
        reportData.innerHTML += `<tr>
            <td>${cat}</td>
            <td class="income">$${totals.income.toFixed(2)}</td>
            <td class="expense">$${totals.expense.toFixed(2)}</td>
            <td class="${net >= 0 ? 'income' : 'expense'}">$${net.toFixed(2)}</td>
        </tr>`;
    });
    reportData.innerHTML += '</tbody></table>';
    
    // 渲染图表
    const ctx = document.getElementById('report-chart').getContext('2d');
    if (window.reportChart) window.reportChart.destroy();
    
    const categories = Object.keys(categoryTotals);
    const incomes = categories.map(c => categoryTotals[c].income);
    const expenses = categories.map(c => categoryTotals[c].expense);
    
    window.reportChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [
                { label: '收入', data: incomes, backgroundColor: '#27ae60' },
                { label: '支出', data: expenses, backgroundColor: '#e74c3c' },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    });
});

// 搜索过滤
document.getElementById('search-input').addEventListener('input', () => {
    const query = document.getElementById('search-input').value.toLowerCase();
    const rows = document.querySelectorAll('#transaction-list tr');
    rows.forEach(row => {
        row.style.display = row.textContent.toLowerCase().includes(query) ? '' : 'none';
    });
});

// 分类过滤
document.getElementById('category-filter').addEventListener('change', () => {
    const category = document.getElementById('category-filter').value;
    const rows = document.querySelectorAll('#transaction-list tr');
    rows.forEach(row => {
        if (!category) { row.style.display = ''; return; }
        row.style.display = row.cells[2].textContent.toLowerCase() === category.toLowerCase() ? '' : 'none';
    });
});

// 月份过滤
document.getElementById('month-filter').addEventListener('change', () => {
    const month = document.getElementById('month-filter').value;
    const rows = document.querySelectorAll('#transaction-list tr');
    rows.forEach(row => {
        if (!month) { row.style.display = ''; return; }
        row.style.display = row.cells[0].textContent.startsWith(month) ? '' : 'none';
    });
});

// ==================== 密码保护 ====================
const APP_PASSWORD = 'luxuryfeet2026';

function checkLogin() {
    if (localStorage.getItem('lucky-feet-logged-in') === 'true') {
        showApp();
        return;
    }
    document.getElementById('login-screen').style.display = 'block';
    document.getElementById('main-app').style.display = 'none';
}

document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const pwd = document.getElementById('password').value;
    if (pwd === APP_PASSWORD) {
        localStorage.setItem('lucky-feet-logged-in', 'true');
        showApp();
    } else {
        document.getElementById('login-error').style.display = 'block';
    }
});

document.getElementById('logout-btn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.removeItem('lucky-feet-logged-in');
    location.reload();
});

function showApp() {
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('main-app').style.display = 'block';
    updateDashboard();
    renderTransactions();
}

// 初始化
checkLogin();