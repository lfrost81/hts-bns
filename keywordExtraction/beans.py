#!/usr/bin/python

import sqlite3
import os
import sys
import glob
from datetime import datetime


class Bean:
    data = None
    """
    field = [
    ("DOCID", "docid", "text", "primary key"),\
    ("DATE", "date", "int"),\
    ("URL", "url", "text"),\
    ("CATEGORY", "category", "text"),\
    ("TITLE", "title", "text"),\
    ("SNIPPET", "snippet", "text"),\
    ("CONTENT", "content", "text"),\
    ("SEQ","token", "text")\
]

    """

    def __init__(self, data):
        if type(data) is tuple and len(data) == 8:
            self.data = data

    def __del__(self):
        if self.data != None:
            del self.data

    def getDocumentId(self):
        if self.data == None:
            return None
        return self.data[0]

    def getDate(self):
        if self.data == None:
            return None
        return self.data[1]

    def getTitle(self):
        if self.data == None:
            return None
        return self.data[4]

    def getContent(self):
        if self.data == None:
            return None
        return self.data[6]

    def getKeyword(self):
        if self.data == None:
            return None
        return self.data[5]

    def getToken(self):
        if self.data == None:
            return None
        return self.data[7]

    def getCategory(self):
        if self.data == None:
            return None
        return self.data[3]

    def getData(self):
        if self.data == None:
            return None
        return data


class Beans:
    base_path = None;
    conn = None;
    field = None;

    def __init__(self):
        None

    def __del__(self):
        if self.conn != None:
            self.conn.close()

    def log(self, message):
        print(message)

    def init(self, path, field, init):
        self.base_path = os.path.abspath(path)
        self.field = field

        ret = self.init_db(init)

        if ret[0] < 0:
            self.log(ret)

        if init:
            ret = self.init_table(field)

            if ret[0] < 0:
                self.log(ret)

        return ret

    def init_db(self, flag):
        data_file = os.path.join(self.base_path, "data.db");

        if flag and os.path.exists(data_file):
            os.remove(data_file)

        self.conn = sqlite3.connect(data_file)

        return 0, "No Error"

    def init_table(self, field):
        c = self.conn.cursor()

        create_query = "CREATE TABLE IF NOT EXISTS document ( %s )" % ", ".join([" ".join(f[1:]) for f in field])

        print(create_query)

        c.execute(create_query)
        self.conn.commit()

        return 0, "No Error"

    def read_file(self):
        beans = []
        file_list = glob.glob(os.path.join(self.base_path, "*.hcdf"))

        # make backup directory
        os.makedirs(os.path.join(self.base_path, "backup"), mode=0o755, exist_ok=True)

        file_index = 0
        for file in file_list:
            file_index += 1
            self.log("\n" + "[" + str(datetime.now()) + "][" + str(file_index) + "] read file => " + file)
            self.load_file(file, beans)
            ret = self.save_data(beans)

            print("couldn't insert %d data in file[=%s]" % (ret[0], file))

            os.rename(file, os.path.join(self.base_path, "backup", os.path.basename(file)))
            del beans[:]

        return 0, "No Error"

    def load_file(self, file, beans):
        field_names = "+".join([k[0] for k in self.field])

        document = []
        with open(file, "r") as fin:
            for line in fin:
                line = line.strip()

                if len(line) == 0:
                    continue

                pos = line.find("::=")
                if pos > 0 and field_names.find(line[:pos]) >= 0:
                    if line[:pos] == "DOCID" and len(self.field) == len(document) and field_names == "+".join(
                            [k for (k, v) in document]):
                        beans.append(dict())
                        for k, v in document:
                            beans[len(beans) - 1][k] = v

                        del document[:]

                    document.append([line[:pos], line[pos + 3:]])
                else:
                    document[len(document) - 1][1] += " " + line

        if len(self.field) == len(document) and field_names == "+".join([k for (k, v) in document]):
            beans.append(dict())
            for k, v in document:
                beans[len(beans) - 1][k] = v

        return 0, "No Error"

    def save_data(self, beans):
        c = self.conn.cursor()

        columns = ""
        placeholders = ""
        query = ""
        nError = 0

        for bean in beans:
            columns = ', '.join([f[1] for f in self.field])
            placeholders = ':' + ', :'.join([f[0] for f in self.field])
            query = 'INSERT INTO document (%s) VALUES (%s)' % (columns, placeholders)

            try:
                c.execute(query, bean)
            except sqlite3.IntegrityError:
                nError += 1
                None  # print ("couldn't add %s" % bean["DOCID"] )

        self.conn.commit()

        return nError, (len(beans) - nError)

    def executeQuery(self, query):
        c = self.conn.cursor()

        try:
            result = c.execute(query)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        return c.fetchall()

    def getDocument(self, docid):
        c = self.conn.cursor()

        try:
            c.execute("select * from document where docid=?", (docid,))
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        return Bean(c.fetchone())


if __name__ == '__main__':
    print( "="*10 + "recommender start" + "="*10 )

    field = [
        ("DOCID", "docid", "text", "primary key"), \
        ("DATE", "date", "int"), \
        ("URL", "url", "text"), \
        ("CATEGORY", "category", "text"), \
        ("TITLE", "title", "text"), \
        ("SNIPPET", "snippet", "text"), \
        ("CONTENT", "content", "text"), \
        ("SEQ", "token", "text") \
        ]

    bean = Beans()
    bean.init("./data/beans_komoran", field, False )

    bean.read_file()

    print ( bean.executeQuery("select * from document limit 1") )

    print( "="*10 + "recommender end" + "="*10 )
