
def cal_pws(ptw, omega, phi):
    file1 = open('../data/bughunter/File2Word.txt', 'w')
    file2 = open('../data/bughunter/pws_dict.txt', 'w')
    pws = {}
    pws_sorted = {}
    print "calculation..."
    for ptw_key in ptw.keys():
        if ptw_key in omega.keys() and ptw_key in phi.keys():
            tmp = []
            pws[ptw_key] = {}
            for omega_key in omega[ptw_key].keys():
                if omega_key in phi[ptw_key].keys():
                    pro = (ptw[ptw_key] * omega[ptw_key][omega_key]) + \
                                            ((1 - ptw[ptw_key]) * phi[ptw_key][omega_key])
                    pws[ptw_key][omega_key] = pro
                    tmp.append((omega_key, pro))
               # print len(tmp)
        #print ptw_key, pws[ptw_key]
        pws_sorted[ptw_key] = sorted(tmp, lambda x, y: cmp(x[1], y[1]), reverse=True)
        print ptw_key, pws_sorted[ptw_key]
    del ptw
    del omega
    del phi
    print >> file1, pws_sorted
    file1.close()
    print >> file2, pws
    file2.close()
    return pws_sorted
