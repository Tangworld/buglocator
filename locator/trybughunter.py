# -*- coding:utf-8 -*-
import test
import time
# import cal_pws

def main():
    start = time.time()
    k_vocab = open('../data/bughunter/k_vocab.txt', 'r')
    #omega = open('../data/bughunter/omega.txt', 'r')
    phi = open('../data/bughunter/phi.txt', 'r')
    pl = open('../data/bughunter/pl.txt', 'r')
    ptw = open('../data/bughunter/ptw.txt', 'r')
    pws = open('../data/bughunter/pws_dict.txt','r')


    # pws_dict = {}
    # pws_dict = pws_dict.fromkeys(r_pws.keys())
    # print pws_dict

    # for key in r_pws.keys():
       # pws_dict[key] = {}
      # for content in r_pws[key]:
         # pws_dict[key][content[0]] = content[1]
        # print pws_dict[key]
    # print >> file1, pws_dict

    # 获取pws_value参数简化运算
    pws_value = pws.readlines()
    r_pws = eval(pws_value[0])

    # 获取k_vocab参数
    k_vocab_value = k_vocab.readlines()
    r_k_vocab = eval(k_vocab_value[0])

    # 获取omega参数
    #omega_value = omega.readlines()
    #r_omega = eval(omega_value[0])

    # 获取phi参数
    phi_value = phi.readlines()
    r_phi = eval(phi_value[0])

    # 获取pl参数
    pl_value = pl.readlines()
    r_pl = eval(pl_value[0])

    ptw_value = ptw.readlines()
    r_ptw = eval(ptw_value[0])

    ws = [80]
    ts = [1, 2686, 3470, 3817, 1889, 3037]
    report = {'ws': ws, 'ts': ts}

    end = time.time()
    print end - start
    print "Loading Complete."
    s_ptd = test.llda_test(report, r_k_vocab, r_pl, r_phi, r_ptw, r_pws)
    #words = cal_pws.cal_pws(r_ptw, r_omega, r_phi)
    print s_ptd
    print len(s_ptd)
    #print len(words.keys())



if __name__ == "__main__":
    main()

