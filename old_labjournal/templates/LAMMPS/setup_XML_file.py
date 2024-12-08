"""
File to create an XML file for the templates
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

def add_script(fname, flag, description=''):
    child =ET.SubElement(inputscripts,
                         'script',
                         attrib={'flag': flag, 'file' : fname},
                         )
    child.text=description
    return child

root = ET.Element('files')
tree = ET.ElementTree(root)
inputscripts = ET.SubElement(root, 'input_scripts', attrib={'folder':'input_scripts'})


add_script('input.ar_ubiquitin.lammps','X','Inputscript for Ubiquitin [real units]')
add_script('input.ae_caco3.lammps','X','Inputscript for atomisitc CaCO3 [metal units]')
add_script('input.cg_caco3.lammps','X','Inputscript for coarse-grained CaCO3 [real units]')

with open("overview_files.xml", "w") as fp:
    fp.write(minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ", newl="\n"))