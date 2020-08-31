from ckanapi import RemoteCKAN, CKANAPIError
import json, requests, re


def clearText(text):
    return re.sub("\s+", " ", re.sub("\n", "", re.sub("<[^>]+>", "", text)))

ckan = RemoteCKAN('http://dados.gov.br')

datasets = ckan.action.package_list()

types = []
count = 0
error = 0

for dataset in datasets:
   try:
      dataset = ckan.action.package_show(id=dataset)

      for resource in dataset["resources"]:
         types.append(resource["format"].upper())

      count += 1
   except CKANAPIError:
      print("------->> Error to process dataset", dataset)
      error += 1
      continue

print("count:", count, "error:", error, "qtd files:", len(types))

types_semrepeticao = list(set(types))
count = 0
coluna = []

for t in types_semrepeticao:
   for i in types:
      if(t == i):
         count += 1   
   print(t, count)
   count = 0


