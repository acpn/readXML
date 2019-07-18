import xml.etree.ElementTree as ET
import sys
import random

ET.register_namespace('', "http://www.portalfiscal.inf.br/nfe")
file_name = sys.argv[1]
# Speciffic to GPA due to custom objects   

def computeDv(key):
    mult = [2,3,4,5,6,7,8,9]
    soma_ponderada = 0
    i = 42
    m = 0
    while i >= 0:
        m = 0
        while i >= 0 and m < len(mult):
            soma_ponderada += int(key[i]) * int(mult[m])
            i -= 1
            m += 1
    resto = soma_ponderada % 11;
    if resto == '0' or resto == '1':
        return 0
    else:
        return (11 - resto)

def getItemStructure(tree):
    data = []
    root = tree.getroot()
    for tag in root.iter():
        clean_t = str(tag.tag).split('}')[-1]
        if  clean_t == 'cProd':
            data.append(tag.text)
        if  clean_t == 'cEAN':
            data.append(tag.text)
        if  clean_t == 'qCom':
            data.append(tag.text)
        if  clean_t == 'vUnCom':  
            data.append(tag.text)

    return data

def getValue(n_tag, tree):
    data = []
    root = tree.getroot()
    for tag in root.iter():
        clean_t = str(tag.tag).split('}')[-1]
        if  clean_t == n_tag:
            data.append(tag.text)
    
    return data

# You can get the purcase order from your database here (Oracle, Mysql, Postgress etc..)
def returnPO():
	return "48891"

def changeXML(tree):
    key = []
    data = getValue('cEAN', tree)
    root = tree.getroot()
    purchase_order = []
    for x in data:
        purchase_order.append(returnPO())

    # change xPed, chNFe and nNF
    for tag in root.iter():        
        clean_tag = str(tag.tag).split('}')[-1]
        if clean_tag == 'nNF':
            doc_no = list(tag.text)
            doc_no[len(doc_no) - 2] = str(random.randint(0, 9))
            doc_no[len(doc_no) - 1] = str(random.randint(0, 9))
            doc_no = "".join(doc_no)
            tag.text = doc_no
        if clean_tag == 'chNFe':
            key = list(tag.text)
            key[len(key) - 12] = "2"
            dv = computeDv(key[0:43])
            key[43] = str(dv)
            key = "".join(key)
            tag.text = key
        if clean_tag == 'cEAN':
            last_ean = tag.text
        if clean_tag == 'xPed':
            for i in range(0, len(purchase_order)):
                if last_ean == purchase_order[i][0]:
                    tag.text = purchase_order[i][1]
                    # When we've just one purchase order may the supplier
                    # sent yhe purchase order in header and detail
                    if len(purchase_order) > 1:
                        last_ean = ""

    tree.write(key+".xml")

    return key

def processXML(file_name):
    tree = ET.parse(file_name)
    cnpj = getValue('CNPJ', tree)
    litems = getItemStructure(tree)
    print(cnpj)
    print(litems)
    print(changeXML(tree))
    
   
processXML(file_name)
