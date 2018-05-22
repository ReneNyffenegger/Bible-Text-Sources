#!/bin/python
# vi: foldmarker=_{,_} foldmethod=marker


import importlib.util
import os

spec   = importlib.util.spec_from_file_location('?', '../lib/DBTranslation.py')
dbTrx  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dbTrx)


db_file_name = 'lxx.db'
if os.path.isfile(db_file_name):
   os.remove(db_file_name)


db_lxx = dbTrx.db(db_file_name)
db_lxx.create_schema()

db_lxx.create_indices()
# db_lxx.cur.execute('commit')
