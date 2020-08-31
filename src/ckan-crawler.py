from ckanapi import RemoteCKAN
import json, requests, re, os, urllib.request, http.client

def clearText(text):
    return re.sub("\s+", " ", re.sub("\n", "", re.sub("<[^>]+>", "", text)))

base_folder = "$PATH"
base_file_name = "dataset.json"
resources_accepted = ["CSV","JSON", "XML", "KML","XLSX","ODS","XLS"]

ckan = RemoteCKAN('http://dados.gov.br')

datasets = ckan.action.package_list()

for dataset in datasets:
   try:

      dataset_result = ckan.action.package_show(id=dataset)

      if not os.path.exists(base_folder + dataset):
         os.mkdir(base_folder + dataset)

      with open(base_folder + dataset + "/" + base_file_name, 'w') as outfile:  
         json.dump(dataset_result, outfile, indent=4)

      for resource in dataset_result.get("resources"):
         if resource.get("format") in resources_accepted:

            name = resource.get("name")

            # Default file name
            if(name == None):
               name = "file." + resource.get("format")

            try:

               # If don't have URI to download
               if (resource.get("url") == ''):
                  continue

               urllib.request.urlretrieve(resource.get("url"), base_folder + dataset + "/" + name + "." + resource.get("format").lower())

            except http.client.IncompleteRead as e1:
               print("Error to download dataset file- IncompleteRead ", dataset, e1)
            except UnicodeEncodeError as e2:
                print("Error to download dataset file - UnicodeEncodeError", dataset, e2)
            except UnicodeError as e3:
               print("Error to download dataset file - UnicodeError", dataset, e3)

   except OSError as e:
      print("Error to create dataset folder - OSError", base_folder + dataset, e.strerror)

