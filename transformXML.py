import xml.etree.ElementTree as ET
import json
import xmltodict
import xml.dom.minidom as minidom
import itertools,collections
from bs4 import BeautifulSoup

class transformxml():
    def __init__(self,path):
        self.mapping=self.readmapping(path)
        self.contexts=[]
        self.varibles=[]

    def readmapping(self,path):
        with open(path,encoding='utf-8') as f:
            mapping = json.load(f)
        return mapping

    def parseXML(self,path):
        instance_data = {}
        with open(path, encoding='utf-8') as xml_file:
            instance = xmltodict.parse(xml_file.read())
        instance_root=instance.get(self.mapping.get('root'))
        instance_data['period']=instance_root.get('@ОтчДата')
        instance_data['ogrn'] = instance_root.get('Составитель').get('@ОГРН')
        for razdel in self.mapping.get('data').keys():
            mapping_razdel=self.mapping.get('data').get(razdel)
            root_f = []
            final_tag = mapping_razdel.get('tag')
            for xx in instance_root.keys():
                f_tag = xx
                root2 = instance_root
                #print(final_tag)
                while final_tag not in f_tag:  # бежим по тегам, ищем нужный
                    try:
                        root2 = root2.get(f_tag)
                        keys = root2.keys()
                        for kk in keys:
                            if final_tag in kk:
                                if type(root2.get(kk)) == list:
                                    for ll in root2.get(kk):
                                        root_f.append(ll)
                                elif type(root2.get(kk)) == dict:
                                    root_f.append(root2.get(kk))
                        f_tag = kk
                    except:
                        break
                else:
                    break
            instance_data[razdel] = root_f
        return instance_data

    def makeXBRL(self):
        xbrl = ET.Element('xbrli:xbrl')
        xbrl.attrib = self.mapping.get('xbrl_header')
        schref = ET.SubElement(xbrl, 'link:schemaRef')
        schref.attrib = {'xlink:href': self.mapping.get('schemaref'),'xlink:type': "simple"}
        return xbrl

    def saveXBRL(self,xbrl,filename):
        rough_string = ET.tostring(xbrl, encoding='utf-8', method='xml')
        reparsed = minidom.parseString(rough_string)
        reparsed.writexml(open(f'{filename}.xml', 'w'), indent="  ", addindent="  ", newl='\n', encoding="utf-8")

    def makecontext(self,context_id,ogrn,period,period_type,axis,taxis,taxis_value):
        context = ET.Element("xbrli:context")
        context.attrib = {"id": context_id}
        entiy = ET.SubElement(context, "xbrli:entity")
        ident = ET.SubElement(entiy, "xbrli:identifier")
        ident.attrib = {"scheme": "http://www.cbr.ru"}
        ident.text = ogrn
        period_ = ET.SubElement(context, "xbrli:period")
        if period_type == "duration":
            startdate = ET.SubElement(period_, "xbrli:startDate")
            startdate.text = "2023-07-01"
            enddate = ET.SubElement(period_, "xbrli:endDate")
            enddate.text = period
        else:
            instant = ET.SubElement(period_, "xbrli:instant")
            instant.text = period
        scenario = ET.SubElement(context, "xbrli:scenario")
        for xx in axis:
            explicitMember1 = ET.SubElement(scenario, "xbrldi:explicitMember")
            explicitMember1.attrib = {'dimension': xx.split('|')[0]}
            explicitMember1.text = xx.split('|')[1]
        if taxis:
            typedMember = ET.SubElement(scenario, "xbrldi:typedMember")
            typedMember.attrib = {'dimension': taxis.split('|')[0]}
            elem_et = ET.SubElement(typedMember, taxis.split('|')[1])
            elem_et.text = taxis_value
        self.contexts.append(context)

    def writecontext(self,xbrl):
        for xx in self.contexts:
            xbrl.append(xx)

    def makevarible(self,context_id,var,enum,text,unit,decimals):
        atrib = {}
        var = ET.Element(var)
        atrib['contextRef'] = context_id
        if unit not in (None,''): atrib['unitRef'] = unit
        if decimals not in (None,''): atrib['decimals'] = decimals
        var.attrib = atrib
        var.text = text if enum in ('',None) else enum.get(text)
        self.varibles.append(var)

    def writevarible(self,xbrl):
        for xx in self.varibles:
            xbrl.append(xx)

    def makeUnit(self,xbrl):
        units=self.mapping.get('units')
        keys=units.keys()
        for xx in keys:
            unit=ET.SubElement(xbrl, "xbrli:unit")
            unit.attrib={'id':units.get(xx).get('id')}
            measure=ET.SubElement(unit,'xbrli:measure')
            measure.text=units.get(xx).get('text')

    def fillcontext(self,instance_data):
        keys= [key for key in instance_data.keys() if 'razdel' in key]
        ogrn=instance_data.get('ogrn')
        period=instance_data.get('period')
        context_var_list=[]
        context_id_temp=None
        for key in keys:
            print(key)
            data_full=instance_data.get(key)
            axiss_y_synthetic=self.mapping.get('data').get(key).get('axiss_y_synthetic')
            varible=self.mapping.get('data').get(key).get('varible')
            taxis=self.mapping.get('data').get(key).get('taxis')
            axis_pok=axiss_y_synthetic.keys()
            i = 0
            check=True
            for data_stroka in data_full:
                default_axis_stroka=[]
                for axis_pok_key in axis_pok:
                    default_axis_stroka=list(itertools.chain(default_axis_stroka,axiss_y_synthetic[axis_pok_key].get(data_stroka[axis_pok_key])))

                taxis_temp, taxis_value_temp = None, None
                for pokazatel in data_stroka.keys():
                    if taxis.get(pokazatel):
                        taxis_temp = taxis.get(pokazatel)
                        taxis_value_temp= data_stroka[pokazatel]

                for pokazatel in data_stroka.keys():
                    if varible.get(pokazatel):
                        if varible.get(pokazatel).get('axis')!=None:
                            axis_temp=list(itertools.chain(default_axis_stroka,varible.get(pokazatel).get('axis')))
                        else:
                            axis_temp=default_axis_stroka

                        if context_var_list==[]:
                            context_id_temp=f'{key}_{i}'
                            context_var_list.append({'razdel':key,'context_id':context_id_temp,'axis': axis_temp,'taxis':taxis_temp,'taxis_value':taxis_value_temp,'period_type':varible.get(pokazatel).get('period')})
                            self.makecontext( context_id_temp, ogrn, period, varible.get(pokazatel).get('period'),axis_temp, taxis_temp,taxis_value_temp)
                            check= True
                        else:
                            for cc in context_var_list:
                                if collections.Counter(axis_temp) == collections.Counter(cc.get('axis')) and cc['taxis']==taxis_temp and cc['taxis_value']==taxis_value_temp and cc['period_type']==varible.get(pokazatel).get('period'):
                                    context_id_temp=cc.get('context_id')
                                    check = True
                                    break
                                else:
                                    check=False
                        if check==False:
                            i=i+1
                            context_id_temp = f'{key}_{i}'
                            context_var_list.append({'razdel':key,'context_id': context_id_temp, 'axis': axis_temp,'taxis':taxis_temp,'taxis_value':taxis_value_temp,'period_type':varible.get(pokazatel).get('period')})
                            self.makecontext(context_id_temp,ogrn,period,varible.get(pokazatel).get('period'),axis_temp,taxis_temp,taxis_value_temp)
                        self.makevarible(context_id_temp,varible.get(pokazatel).get('var'),varible.get(pokazatel).get('enum'),data_stroka.get(pokazatel),varible.get(pokazatel).get('unit'),varible.get(pokazatel).get('decimals'))
                        print(context_id_temp)

if __name__ == "__main__":
    ss=transformxml('mapping_0409725.json')
    xbrl=ss.makeXBRL()
    instance=ss.parseXML('report_04209725.xml')
    ss.fillcontext(instance)
    ss.writecontext(xbrl)
    ss.makeUnit(xbrl)
    ss.writevarible(xbrl)
    ss.saveXBRL(xbrl,'report_04209725_output')