import MySQLdb

def main():
    input = open("aspectj.txt")
    lines = input.readlines()
    db = MySQLdb.connect("localhost", "root", "root", "CodeDefectLocation")
    cursor = db.cursor()


    for line in lines:
        temp = eval(line)
        priority = temp['pr']
        opendate = temp['tm']
        reporter = temp['rp']
        component = temp['cm']
        tr = temp['tr']
        fileloc = temp['ts']
        severity = temp['sv']
        version = temp['vs']
        keywords = temp['ws']
        platform = temp['pf']
        os = temp['os']
        bugid = temp['id']
        cursor.execute("INSERT INTO Report(bugid,reporter,priority,opendate,component,) VALUES('Jack London')")
        print bugid

if __name__ == "__main__":
    main()