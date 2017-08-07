# -*- coding:utf-8 -*-
import pickle
import time
import types
import MySQLdb
'''
def wordmapinsert():
    db = MySQLdb.connect("localhost", "root", "123456", "locator")
    cursor = db.cursor()
    file1 = open('WordMap.txt', 'r')

    words = file1.readlines()
    count = 0
    for word in words:
        # cursor.execute("select * from locator_bugidmap")
        cursor.execute("insert into locator_wordmap(wordID, word) values('"+str(count)+"', '"+word.strip()+"')")
        count += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

wordmapinsert()

'''

def f2winsert():
    db = MySQLdb.connect("localhost", "root", "123456", "locator")
    cursor = db.cursor()
    file_pws = open('File2Word.txt', 'r')

    pre_pws = file_pws.readlines()
    pws = eval(pre_pws[0])
    print len(pws.keys())
    cnt = 0
    for key in pws.keys():
        string = ''
        for i in range(40):
            string = string + str(pws[key][i][0]) + ' '
        # cursor.execute("select * from locator_bugidmap")
        cursor.execute("insert into locator_f2w(fileID, keywords) values('"+str(key)+"', '"+string+"')")
        cnt += 1

    print cnt
    db.commit()  # Commit the transaction
    cursor.close()
    db.close()


f2winsert()


'''
start = time.time()

pkl_k_vocab = file('k_vocab.pkl', 'rb')
pkl_phi = file('phi.pkl', 'rb')
pkl_pl = file('pl.pkl', 'rb')
pkl_ptw = file('ptw.pkl', 'rb')
pkl_pws = file('pws.pkl', 'rb')

pre_k_vocab = pickle.load(pkl_k_vocab)
#pre_omega = omega.readlines()
pre_phi = pickle.load(pkl_phi)
pre_pl = pickle.load(pkl_pl)
pre_ptw = pickle.load(pkl_ptw)
pre_pws = pickle.load(pkl_pws)

end = time.time()
print end - start
print type(pre_pws)
print type(pre_phi)
print type(pre_pl)
print type(pre_ptw)
print type(pre_k_vocab)
'''
'''
file_k_vocab = open('k_vocab.txt', 'r')
#omega = open(BASE_DIR + '/data/bughunter/omega.txt', 'r')
file_phi = open('phi.txt', 'r')
file_pl = open('pl.txt', 'r')
file_ptw = open('ptw.txt', 'r')
file_pws = open('pws_dict.txt', 'r')

pre_k_vocab = file_k_vocab.readlines()
#pre_omega = omega.readlines()
pre_phi = file_phi.readlines()
pre_pl = file_pl.readlines()
pre_ptw = file_ptw.readlines()
pre_pws = file_pws.readlines()

# 获取k_vocab参数
# print pre_k_vocab
r_k_vocab = eval(pre_k_vocab[0])
# 获取omega参数
# r_omega = eval(pre_omega[0])
# 获取phi参数
r_phi = eval(pre_phi[0])
# 获取pl参数
r_pl = eval(pre_pl[0])
r_ptw = eval(pre_ptw[0])
r_pws = eval(pre_pws[0])

file_k_vocab.close()
#omega.close()
file_phi.close()
file_pl.close()
file_ptw.close()
file_pws.close()

pickle.dump(r_k_vocab, pkl_k_vocab, True)
pickle.dump(r_phi, pkl_phi, True)
pickle.dump(r_pl, pkl_pl, True)
pickle.dump(r_ptw, pkl_ptw, True)
pickle.dump(r_pws, pkl_pws, True)
'''