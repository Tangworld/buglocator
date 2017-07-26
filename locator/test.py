from collections import Counter

def calc_pws(ws, t_vocab, pz, phi, omega, ptw):
    pws = {}

    ws = list(set(ws))
    for w in ws:
        pws[w] = 0
        for t in t_vocab:
            if w == t:
                pws[w] += (ptw[w] + (1 - ptw[w])*phi[t][w])*pz[t]
            else:
                pws[w] += phi[t][w]*pz[t]

    return pws


def calc_pwds(ws):
    pwds = {}

    ws_sum = len(ws)
    cws = Counter(ws)
    for w in cws:
        pwds[w] = cws[w]*1.0/ws_sum

    return pwds


def llda_test(data, k_vocab_total, pl, phi, omega, ptw):
    l0 = phi.keys()[0]
    w_vocab = set(phi[l0].keys())
    t_vocab = pl.keys()

    # f_result = open(fn, 'w')

    
    wss = data["ws"]
    tags = data["ts"]

    ws_temp = wss[:]
    ws = wss[:]
    for w in ws_temp:
        if w not in w_vocab:
            ws.remove(w)
    del ws_temp

    pws = calc_pws(ws, t_vocab, pl, phi, omega, ptw)
    pwds = calc_pwds(ws)

    pzd = {}
    for t in t_vocab:
        pzd[t] = 0
        for w in set(ws):
            #if w == t:
            if w in k_vocab_total:
                pzd[t] += (ptw[t] * omega[t][w] + (1 - ptw[t])*phi[t][w])*pl[t]*pwds[w]/pws[w]
            else:
                pzd[t] += phi[t][w]*pl[t]*pwds[w]/pws[w]

    del pwds
    del pws
    '''
    pzd_f = {}
    for t in pzd.keys():
        if len(list(set([sCom]) & sourceCom[t])) > 0:
            pzd_f[t] = pzd[t]
    '''
    # test one record
    s_ptd = sorted(pzd.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    
    return s_ptd