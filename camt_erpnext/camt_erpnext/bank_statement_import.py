import frappe
import csv
import json
import os
import datetime
from datetime import datetime
from pytz import timezone
import re
import xml.etree.ElementTree as ET

@frappe.whitelist()
def convert_xml_to_csv(file):
   xml_file = get_absolute_path(file) #getting file with path
   #frappe.msgprint(xml_file)
   current_date= datetime.now(timezone("Asia/Kolkata"))
   current_time = current_date.strftime("%d-%m-%Y %H:%M:%S")
   #frappe.msgprint(current_time)
   #filename = os.path.join(os.environ["USERPROFILE"], "Desktop", "test.csv")
   #filename = 'C:/Users/seyfert user/Desktop/newfile' +str(current_time) +'.csv'
   filename = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}/public/files/'+current_time+'.csv'
   xml=ET.parse(xml_file)
   root=xml.getroot()
   name = root.tag
   prevalue=""
   str1 = name.split('{')
   l=[]
   for i in str1:
       if '}' in i:
           l.append(i.split('}')[0])
       else:
           l.append(i)
   var = ''.join(l) 
   #frappe.msgprint(var)
   

   with open(filename,"w",newline='')as csvfile:
           field_names=["Name"]
           csv_writer = csv.writer(csvfile)
           headers = ['Date','Bank Account','Company','Deposit','Withdrawal','Reference Number','Description']
           csv_writer.writerow(headers)
           num_records = len(root)
           withdraw =""

        

           for item in root.iter('{'+var+'}'+'Ntry'):
                Date=item.find('.//{' + var+ '}BookgDt/{'+var+'}Dt').text if item.find('.//{'+var+'}BookgDt/{'+var+'}Dt') is not None else ""
                #Bank='PPS - ICICI'
                #Company = 'SeyfertSoft Private Limited'

                # Extract Bank and Company information
                bank_elem = root.find('.//{' + var + '}Acct/{'+ var + '}Svcr/{' + var + '}FinInstnId/{' + var + '}Nm')
                company_elem = root.find('.//{' + var + '}Acct/{' + var + '}Ownr/{' + var + '}Nm')
                Bank = bank_elem.text if bank_elem is not None else ""
                Company = company_elem.text if company_elem is not None else ""

                Credt=item.find('{+var+}+CdtDbtInd').text if item.find('{+var+}+CdtDbtInd') is not None else ""
                if item.find('{'+var+'}'+'CdtDbtInd').text == 'CRDT':
                    Deposit=item.find('{'+var+'}'+'Amt').text if item.find('{'+var+'}'+'Amt') is not None else " "
                elif item.find('{'+var+'}'+'CdtDbtInd').text == 'DBIT':
                    Deposit = ""
                if item.find('{'+var+'}'+'CdtDbtInd').text == 'DBIT':
                    withdraw =item.find('{'+var+'}'+'Amt').text if item.find('{'+var+'}'+'Amt') is not None else " "
                elif item.find('{'+var+'}'+'CdtDbtInd').text == 'CRDT':
                     withdraw = ''
                Ntry=item.find('{'+var+'}'+'NtryRef').text if item.find('{'+var+'}'+'NtryRef') is not None else ""
                des=item.find('{'+var+'}'+'AddtlNtryInf').text if item.find('{'+var+'}'+'AddtlNtryInf') is not None else ""
                csv_writer.writerow([Date,Bank,Company,Deposit,withdraw,Ntry,des])
           '''
           fileurl= filename
           filename1 = fileurl.split('files/')
           filenames = filename1[1]
           
           doc = frappe.get_doc({
           'doctype': 'File',
           'file_name': filenames,
           'file_url':"/files/"+filenames
           })
           doc.insert()
           '''
           
           return filename

#@frappe.whitelist()
def get_absolute_path(file_name):
	if(file_name.startswith('/files/')):
		file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}/public{file_name}'
	if(file_name.startswith('/private/')):
		file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}{file_name}'
	return file_path

