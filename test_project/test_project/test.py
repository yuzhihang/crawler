# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import bson
import re
from scrapy.exceptions import DropItem
from pymongo.errors import DuplicateKeyError
from pprint import pprint

client = pymongo.MongoClient('mongodb://localhost:27017')
mails = client['compass']['mails']
resumes = client['compass']['resumes']
cmail = 0
cresumes = 0
for mail in mails.find(
        {"company": bson.objectid.ObjectId("53f2f8c31a1eae10003701e9"), "attachments.0": {'$exists': 1}}):
    cmail += 1
    if not mail.get('subject'):
        continue

    for resume in resumes.find({'mail': bson.objectid.ObjectId(mail["_id"])}):
        status = resume.get('status')
        path = ""
        cresumes += 1
        if status == "new":
            path += status + "/"
        if mail.get('html'):
            with open('yitong/' + path + mail['subject'].replace('/', '') + '.html', 'w+') as m:
                m.write(mail['html'])

        for at in mail['attachments']:
            content_type = at.get('contentType')
            pprint(at['fileName'] + content_type)
            if at.get('content'):
                if re.search('(word|pdf)', content_type):

                    with open('yitong/' + path + mail['subject'].replace('/', '') + at['fileName'],
                              'wb+') as f:
                        f.write(at['content'])

print(cmail)
print(cresumes)
