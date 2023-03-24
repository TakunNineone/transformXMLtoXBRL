import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom as minidom
import config

class transformxml():
    def __init__(self):
        self.xbrl_header=config.xbrl_header #подгружаем типовую шапку
        self.mapping=config.mapping #подгружаем маппинг
        self.units=config.units
        self.varibale=[]
        self.contexts=[]

    #Создание тела контекста
    def makeContext(self,context_id,identificator,period,period_type):
        context=ET.Element("xbrli:context")
        context.attrib={'id':context_id}
        entiy=ET.SubElement(context, "xbrli:entity")
        ident=ET.SubElement(entiy, "xbrli:identifier")
        ident.attrib={'scheme':"http://www.cbr.ru"}
        ident.text=identificator
        # period_ = ET.SubElement(context, "xbrli:period")
        # if period_type=='duration':
        #     startdate=ET.SubElement(period_,'xbrli:startDate')
        #     startdate.text='2023-07-01'
        #     enddate = ET.SubElement(period_, 'xbrli:endDate')
        #     enddate.text = period
        # else:
        #     instant=ET.SubElement(period_, "xbrli:instant")
        #     instant.text=period
        scenario=ET.SubElement(context, "xbrli:scenario")
        self.contexts.append(context)
        return scenario,context

    def makePeriod(self,context,period,period_type):
        period_ = ET.SubElement(context, "xbrli:period")
        print(context)
        if period_type=='duration':
            startdate=ET.SubElement(period_,'xbrli:startDate')
            startdate.text='2023-07-01'
            enddate = ET.SubElement(period_, 'xbrli:endDate')
            enddate.text = period
        else:
            instant=ET.SubElement(period_, "xbrli:instant")
            instant.text=period

    def makeContexts(self,root,contexts):
        for xx in contexts:
            root.append(xx)

    # создание открытой оси
    def makeAxis_2(self, root, dimension,text):
        explicitMember1 = ET.SubElement(root, "xbrldi:explicitMember")
        explicitMember1.attrib={'dimension': dimension}
        explicitMember1.text=text
        return explicitMember1

    # создание закрытой оси
    def makeTaxis(self,root, dimension,member,text):
        typedMember = ET.SubElement(root, "xbrldi:typedMember")
        typedMember.attrib={'dimension':dimension}
        elem_et=ET.SubElement(typedMember, member)
        elem_et.text=text
        return typedMember

    # создание показателя
    def makeVaribal_2(self,contextRef,var,text,unit,decimals):
        atrib = {}
        var = ET.Element(var)
        atrib['contextRef'] = contextRef
        if unit != '': atrib['unitRef'] = unit
        if decimals != '': atrib['decimals'] = decimals
        var.attrib = atrib
        var.text = text
        self.varibale.append(var)


    # Создание контекстов на основе парсинга отчета
    def makeContAndVar(self, mapping, data, razdel):
        contexts_defaul=[]
        period_type=None
        for xx in range(len(data.get('data_root'))):
            i=0
            context_id = data.get('data_root')[xx].get('context_id')
            if mapping.get(razdel).get('axis') or mapping.get(razdel).get('taxis') or mapping.get(razdel).get('varible'):
                scenario,cont = self.makeContext(context_id, data.get('@ОГРН'), data.get('@ОтчДата'),'instant')
                for yy in data.get('data_root')[xx].keys():
                    if mapping.get(razdel).get('axis'):
                        if yy in mapping.get(razdel).get('axis').keys():
                            period_type=mapping.get(razdel).get('axis').get(yy).get('period')
                            dimension=mapping.get(razdel).get('axis').get(yy).get(data.get('data_root')[xx].get(yy)).get('axis')
                            text=mapping.get(razdel).get('axis').get(yy).get(data.get('data_root')[xx].get(yy)).get('member')
                            contexts_defaul.append(self.makeAxis_2(scenario,dimension,text))
                    if mapping.get(razdel).get('taxis'):
                        if yy in mapping.get(razdel).get('taxis').keys():
                            period_type = mapping.get(razdel).get('taxis').get(yy).get('period')
                            dimension=mapping.get(razdel).get('taxis').get(yy).get('taxis')
                            member=mapping.get(razdel).get('taxis').get(yy).get('member')
                            text=data.get('data_root')[xx].get(yy)
                            self.makeTaxis(scenario,dimension,member,text)
                    if mapping.get(razdel).get('varible'):
                        if yy in mapping.get(razdel).get('varible').keys():
                            var=mapping.get(razdel).get('varible').get(yy).get('var')
                            unit=mapping.get(razdel).get('varible').get(yy).get('unit')
                            decimals=mapping.get(razdel).get('varible').get(yy).get('decimals')
                            text=data.get('data_root')[xx].get(yy) if mapping.get(razdel).get('varible').get(yy).get('member')==None else \
                                mapping.get(razdel).get('varible').get(yy).get('member').get(data.get('data_root')[xx].get(yy))
                            self.makeVaribal_2(context_id,var,text,unit,decimals)
                if period_type:
                    self.makePeriod(cont, data.get('@ОтчДата'), period_type)

            for yy in data.get('data_root')[xx].keys():
                if mapping.get(razdel).get('axis_varible'):
                    if yy in mapping.get(razdel).get('axis_varible').keys():
                        period_type2 = mapping.get(razdel).get('axis_varible').get(yy).get('period')
                        scenario2,cont2 = self.makeContext(f'{context_id}_{i}', data.get('@ОГРН'), data.get('@ОтчДата'), period_type)
                        self.makePeriod(cont2,data.get('@ОтчДата'),period_type2)
                        if mapping.get(razdel).get('axis'):
                            for zz in contexts_defaul:
                                scenario2.append(zz)
                        var = mapping.get(razdel).get('axis_varible').get(yy).get('var')
                        unit = mapping.get(razdel).get('axis_varible').get(yy).get('unit')
                        decimals = mapping.get(razdel).get('axis_varible').get(yy).get('decimals')
                        text = data.get('data_root')[xx].get(yy)
                        self.makeVaribal_2(f'{context_id}_{i}',var,text,unit,decimals)
                        i=i+1
                        for aa in mapping.get(razdel).get('axis_varible').get(yy).get('axiss'):
                            self.makeAxis_2(scenario2, aa.get('axis'), aa.get('member'))
            contexts_defaul=[]

    # создание блока Unit
    def makeUnit(self,root,units):
        keys=units.keys()
        for xx in keys:
            unit=ET.SubElement(root, "xbrli:unit")
            unit.attrib={'id':units.get(xx).get('id')}
            measure=ET.SubElement(unit,'xbrli:measure')
            measure.text=units.get(xx).get('text')

    # сохранение XML
    def saveXML(self,data,filename):
        rough_string = ET.tostring(data, encoding='utf-8', method='xml')
        reparsed = minidom.parseString(rough_string)
        reparsed.writexml(open(f'{filename}.xml', 'w'), indent="  ", addindent="  ", newl='\n', encoding="utf-8")

    # создание корневого XML
    def makeXML(self):
        xbrl = ET.Element('xbrli:xbrl')
        xbrl.attrib = self.xbrl_header
        schref = ET.SubElement(xbrl, 'link:schemaRef')
        schref.attrib = {'xlink:href': config.schemaref,'xlink:type': "simple"}
        return xbrl

    # Создание показателей на основе парсинга отчета
    def makeVaribalse_2(self,root,varibles):
        for xx in varibles:
            root.append(xx)

    # чтение XML, перевод его в словарь
    def readXML(self,path):
        with open(path, encoding='utf-8') as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
            xml_file.close()
        return data_dict

    # парсинг XML
    def parseXML(self,data,mapping,razdel): #Задается первый корневой тег и тег в котором данные репорта
        root_f=[]
        ret_dic={}
        root = data.get(mapping.get(razdel).get('root'))
        final_tag=mapping.get(razdel).get('tag')
        for xx in root.keys():
            if '@' in xx:
                ret_dic[xx]=root[xx] # записываем данные из корневого тега
            if 'Составитель' == xx :
                ret_dic['@ОГРН']=root[xx]['@ОГРН']
            else:
                f_tag=xx
                root2=root
                while final_tag not in f_tag: # бежим по тегам, ищем нужный
                    try:
                        root2=root2.get(f_tag)
                        keys=root2.keys()
                        for kk in keys:
                            if final_tag in kk:
                                if type(root2.get(kk))==list:
                                    for ll in root2.get(kk):
                                        root_f.append(ll)
                                elif type(root2.get(kk))==dict:
                                    root_f.append(root2.get(kk))
                        f_tag=kk
                    except:
                        break
                else:
                    break

        for xx in range(len(root_f)):
            root_f[xx]['context_id']=f'{razdel}_{xx}' # создаем id контекста
        ret_dic['data_root'] = root_f # записываем результаты парсинга
        return ret_dic

if __name__ == "__main__":
    # ss=transformxml()
    # data=ss.readXML('report_0409725new3.xml') # Путь к отчету
    # xbrl = ss.makeXML()
    # okud='Ф0409725'
    # mapping=ss.mapping.get('okud')[okud]
    # for xx in mapping.keys():
    #     data_instance = ss.parseXML(data,mapping,xx)
    #     ss.makeContAndVar(mapping,data_instance,xx)
    # ss.makeContexts(xbrl,ss.contexts)
    # ss.makeUnit(xbrl, ss.units)
    # ss.makeVaribalse_2(xbrl,ss.varibale)
    # ss.saveXML(xbrl,'report_0409725new3_output')

    ss=transformxml()
    data=ss.readXML('report_04209728.xml') # Путь к отчету
    xbrl = ss.makeXML()
    okud='Ф0409728'
    mapping=ss.mapping.get('okud')[okud]
    for xx in mapping.keys():
        data_instance = ss.parseXML(data,mapping,xx)
        ss.makeContAndVar(mapping,data_instance,xx)
    ss.makeContexts(xbrl,ss.contexts)
    ss.makeUnit(xbrl, ss.units)
    ss.makeVaribalse_2(xbrl,ss.varibale)
    ss.saveXML(xbrl,'report_04209728_output')