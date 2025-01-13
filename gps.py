from xml.etree import ElementTree as et

class Kml(object):
    def __init__(self):
        self.root = et.Element('kml')
        self.doc = et.SubElement(self.root,'Document')

    def add_placemark(self,name,desc,long, lat,alt):
        pm = et.SubElement(self.doc,'Placemark')
        et.SubElement(pm,'name').text = name
        et.SubElement(pm,'description').text = desc
        pt = et.SubElement(pm,'Point')
        et.SubElement(pt,'coordinates').text = '{},{},{}'.format(lat,long,alt)

    def write(self,filename):
        tree = et.ElementTree(self.root)
        tree.write(filename)
    
    def tostring(self):
        return et.tostring(self.root, encoding='utf8', method='xml')

