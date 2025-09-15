from lxml import etree
def display(alist):
     tree = etree.fromstring(''.join(alist))
     
     #for customer in tree.xpath('.//Customer'):
      #   print(customer.attrib['CustomerID'],customer.find('CompanyName').text,customer.find('Phone').text)
     for customer in tree.xpath('//Customer'):
         print("CustomerID >", customer.attrib['CustomerID'])
         for cus in customer:
             if cus.text != None:
                 print(cus.text)
         for FullAddress in customer.xpath('FullAddress'):
             #print(ShipInfo.attrib['ShippedDate'])
             for full in FullAddress:
                 print(full.tag,">",full.text)   
         break

     print("\n ~~~~~~~~~~~~~~~ \n")
     
     for order in tree.xpath('//Order'):
         for ordr in order:
             if ordr.text != None:
                 print(ordr.tag,">",ordr.text)
         for ShipInfo in order.xpath('ShipInfo'):
             print("ShippedDate >", ShipInfo.attrib['ShippedDate'])
             for ship in ShipInfo:
                 if ship.text != None:
                     print(ship.tag,">",ship.text)
             #print(ShipInfo.find('Freight').text,ShipInfo.find('ShipName').text)
         break
                 
        

     #for country in tree.xpath('.//country'):
     #    print(country.attrib['name'], country.find('rank').text, country.find('year').text)
     #    print([neighbour.attrib['name'] for neighbour in country.xpath('neighbor')])

path = 'D:\gowrishankar.p\Python Script\py_input\orders.xml'
accumulated_xml = []
with open(path) as temp:
    while True:
        line = temp.readline()
        if line:
            #print(line)
            if line.startswith('<?xml'):
                if accumulated_xml:
                    #display (accumulated_xml)
                    accumulated_xml = []
            else:
                accumulated_xml.append(line.strip())
        else:
            #display (accumulated_xml)
            break

