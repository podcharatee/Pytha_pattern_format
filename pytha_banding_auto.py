from typing_extensions import final
import xml.etree.ElementTree as ET
import io
import pandas as pd
import os

from xml.dom.minidom import parseString



sheetname=[]
dataframe_list=[]
side_tag_list=['band-front','band-back','band-left','band-right','band-top','band-bottom']
rule_set_col_name = ['part-name', 'construction-type',
                     'band-front','band-back','band-left','band-right','band-top','band-bottom',
                     'raw-front','raw-back','raw-left','raw-right','raw-top','raw-bottom' ]

edge_dict = {
    'band-front':False,
    'band-back':False,
    'band-left':False,
    'band-right':False,
    'band-top':False,
    'band-bottom':False,
}

raw_dict = {
    'raw-front':0,
    'raw-back':0,
    'raw-left':0,
    'raw-right':0,
    'raw-top':0,
    'raw-bottom':0,
}


def forward_convert(fullpathxlsx, saveloc, filename):
    file_path = fullpathxlsx
    f = io.open(file_path, encoding="utf8")
    tree = ET.parse(f)
    root = tree.getroot()
    for rule_set in root:
        sheetname.append(rule_set.attrib['name']+' protected='+rule_set.attrib['protected'])
        
        rule_set_df = pd.DataFrame(columns=rule_set_col_name)


        for rule in rule_set:
            part_name = rule.attrib['part-name']
            construction_type = rule.attrib['construction-type']
            header_dict = {'part-name':part_name, 'construction-type':construction_type}

            edge_dict = {
                'band-front':False,
                'band-back':False,
                'band-left':False,
                'band-right':False,
                'band-top':False,
                'band-bottom':False,
            }

            raw_dict = {
                'raw-front':0,
                'raw-back':0,
                'raw-left':0,
                'raw-right':0,
                'raw-top':0,
                'raw-bottom':0,
            }

            for side in rule:
                side_name = side.tag.split("}")[1]
                side_raw = side.attrib['raw']
                side_edge = side.text

                edge_dict[side_name] = side_edge
                raw_dict['raw-' + side_name.split("-")[1]]

            final_dict = {**header_dict, **edge_dict, **raw_dict}
            rule_set_df = rule_set_df.append(final_dict, ignore_index=True)
            
        dataframe_list.append(rule_set_df)


        writter=pd.ExcelWriter(saveloc+"\\"+filename[0:-4] +"_Converted.xlsx",engine="openpyxl")
        i=0
        for df in dataframe_list:
            df.to_excel(writter,sheet_name=sheetname[i],index=False,engine="openpyxl")
            i+=1
        writter.save()
    

def backward_reverse(fullpathxlsx, saveloc, filename):
    df_dict = pd.read_excel(fullpathxlsx,sheet_name=None,dtype=str)
    

    xml_text='''<?xml version="1.0" encoding="UTF-8"?>
<!--
Brief explanation of the structure of this file

The line
  <banding-automatic xmlns="...">
must not be changed and identifies the file as an automatic edging file.

This can contain several automatic glueing devices. Every automatic edge banding system is a text block:
  <rule-set name="Musterautomatik" protected="0">
     ...
  </rule-set>
Each automatic edge banding system can contain several banding rules.

There is a text block for each edge banding rule:
  <rule part-name="Mustername" construction-type="Mustertyp">
     ...
  </rule>
This edge banding rule is applied to components that have the name pattern name and the construction type pattern type.

Each edging rule can set the following edging:
  <band-front raw="0">Musteranleimer vorne</band-front>
  <band-back raw="0">Musteranleimer hinten</band-back>
  <band-left raw="0">Musteranleimer links</band-left>
  <band-right raw="0">Musteranleimer rechts</band-right>s
  <band-top raw="0">Musteranleimer oben</band-top>
  <band-bottom raw="0">Musteranleimer unten</band-bottom>
Sample edging is a text: material, thickness in mm
and raw = "0" or raw = "1" specifies whether or not to cut dimensions.

All quotation marks "" and beak brackets <> are required.
-->\n'''


    root = ET.Element("banding-automatic", xmlns="http://xmlns.pytha.com/banding-automatic/1.0")
    


    for df_key in df_dict.keys():
        [name,protected] = df_key.split(' protected=')
        rule_set = ET.SubElement(root, "rule-set", name=name, protected=protected)
        for _,rule_row in df_dict[df_key].fillna(value="").iterrows():
            rule = ET.SubElement(rule_set, "rule",attrib = {'construction-type':rule_row['construction-type'], 'part-name':rule_row['part-name']} )
            for side_name in ['band-front','band-back','band-left','band-right','band-top','band-bottom']:
                if rule_row[side_name] != 'False' : ET.SubElement(rule, side_name, raw=rule_row['raw-'+side_name.split('-')[1]]).text = rule_row[side_name]
        
        pass
    xml_text = xml_text + parseString(ET.tostring(root,short_empty_elements=False).decode("utf-8")).childNodes[0].toprettyxml(indent="  ")
    file1 = open(saveloc+"\\"+filename.replace("_Converted","")[:-5]+".txt", 'w')
    file1.write(xml_text)
    file1.close()


    pass








if __name__ == "__main__":
    Method="0"
    while Method != "C" and Method != "R" and Method != "c" and Method != "r" :
        Method=input("Convert/Revert(C/R/):")
        if Method != "C" and Method != "R" and Method != "c" and Method != "r":
            print("Input C or R")
            print("You input "+Method)

    fullpathxlsx=input("File:")
    if "\"" in fullpathxlsx:
        fullpathxlsx=fullpathxlsx[1:-1]
    saveloc, filename= os.path.split(fullpathxlsx)

    if Method == "C" or Method == "c":
        forward_convert(fullpathxlsx, saveloc, filename)
    elif Method == "R" or Method == "r":
        backward_reverse(fullpathxlsx, saveloc, filename)
        pass