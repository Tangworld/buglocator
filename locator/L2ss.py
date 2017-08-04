import time
from collections import Counter
import copy
import pickle
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

mini_count = 1
def isSpecialWord(w, t):
    return len(w) >= mini_count and t.find(w) >= 0


def calc_pws(ws, t_vocab, pz, phi, phi2, ptw):
    pws = {}
    ws = list(set(ws))
    for w in ws:
        pws[w] = 0
        for t in t_vocab:
            if isSpecialWord(w, t):
                pws[w] += (ptw[t] * phi2[t].get(w, 0) + (1 - ptw[t]) * phi[t][w]) * pz[t]
            else:
                pws[w] += phi[t][w] * pz[t]
    return pws


def calc_pwds(ws):
    pwds = {}

    ws_sum = len(ws)
    cws = Counter(ws)
    for w in cws:
        pwds[w] = cws[w] * 1.0 / ws_sum
    return pwds


def l2ss_test(bugid, epl, pl, phi, phi2, ptw, tr_dis, data):

    pkl_component_l2ss = file(BASE_DIR + '/data/L2SS/component_t.pkl', 'rb')
    pkl_t_vocab_l2ss = file(BASE_DIR + '/data/L2SS/t_vocab.pkl', 'rb')
    t_vocab = pickle.load(pkl_t_vocab_l2ss)
    component_t = pickle.load(pkl_component_l2ss)

    pkl_component_l2ss.close()
    pkl_t_vocab_l2ss.close()

    metadata = 'cm'
    l0 = phi.keys()[0]
    w_vocab = set(phi[l0].keys())

    d = data[bugid]
    wss = d["ws"]
    tags = d["ts"]
    cm = d[metadata]
    trs = d['tr']
    ws_temp = wss[:]
    ws = wss[:]
    for w in ws_temp:
        if w not in w_vocab:
            ws.remove(w)
    del ws_temp

    # pws = calc_pws(ws, t_vocab, pl, phi, phi2, ptw)
    pwds = calc_pwds(ws)
    if not component_t.has_key(cm):
        ptv = copy.deepcopy(epl)
    else:
        ptv = copy.deepcopy(pl[cm])
    ptr = {}
    pc = 1.0
    for tr in trs:
        ptr[tr] = tr_dis
        pc -= tr_dis
    for t in t_vocab:
        if t not in trs:
            ptr[t] = pc / (len(t_vocab) - len(trs))
        ptv[t] *= ptr[t]

    pzd = {k: 0 for k in ptv}
    for w in set(ws):
        pzw = {}
        sum_pzw = 0
        for t in ptv:
            if isSpecialWord(w, t):
                pzw[t] = pzw.get(t, 0) + (ptw[t] * phi2[t].get(w, 0) + (1 - ptw[t]) * phi[t][w]) * ptv[t]
            else:
                pzw[t] = pzw.get(t, 0) + phi[t][w] * ptv[t]
            sum_pzw += pzw[t]
        for t in ptv:
            pzw[t] /= sum_pzw
            pzd[t] += pzw[t] * pwds[w]

    del pwds

    s_ptd = sorted(pzd.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

    return s_ptd
'''
start = time.time()

pkl_aspectj_l2ss = file(BASE_DIR + '/data/L2SS/aspectj.pkl', 'rb')
pkl_epl_l2ss = file(BASE_DIR + '/data/L2SS/epl_l2ss.pkl', 'rb')
pkl_phi2_l2ss = file(BASE_DIR + '/data/L2SS/phi2_l2ss.pkl', 'rb')
pkl_phi_l2ss = file(BASE_DIR + '/data/L2SS/phi_l2ss.pkl', 'rb')
pkl_pl_l2ss = file(BASE_DIR + '/data/L2SS/pl_l2ss.pkl', 'rb')
pkl_ptw_l2ss = file(BASE_DIR + '/data/L2SS/ptw_l2ss.pkl', 'rb')
pkl_tr_dis_l2ss = file(BASE_DIR + '/data/L2SS/tr_dis_l2ss.pkl', 'rb')

data_l2ss = pickle.load(pkl_aspectj_l2ss)
epl_l2ss = pickle.load(pkl_epl_l2ss)
phi_l2ss = pickle.load(pkl_phi_l2ss)
phi2_l2ss = pickle.load(pkl_phi2_l2ss)
pl_l2ss = pickle.load(pkl_pl_l2ss)
ptw_l2ss = pickle.load(pkl_ptw_l2ss)
tr_dis_l2ss = pickle.load(pkl_tr_dis_l2ss)

pkl_aspectj_l2ss.close()
pkl_epl_l2ss.close()
pkl_phi2_l2ss.close()
pkl_phi_l2ss.close()
pkl_pl_l2ss.close()
pkl_ptw_l2ss.close()
pkl_tr_dis_l2ss.close()

result = l2ss_test('166514', epl_l2ss, pl_l2ss, phi_l2ss, phi2_l2ss, ptw_l2ss, tr_dis_l2ss, data_l2ss)
print result
print len(result)
end = time.time()
print end - start
#l2ss_test(bugid, epl, pl, phi, phi2, ptw, tr_dis, data)
'''