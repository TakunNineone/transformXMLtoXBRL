import numpy,xmltodict,json,xml.dom.minidom as minidom,xml.etree.ElementTree as ET,operator

class transformxml():
    def __init__(self, path):
        self.mapping = self.readmapping(path)
        self.root=self.mapping.get('root')
        self.context_data= {}
        self.varible_data= {}
        self.data_list_reverse= {}
        self.axis_synt_list=[]
        self.taxis_list=[]
        self.var_list=[]

    def saveXBRL(self,xbrl,filename):
        rough_string = ET.tostring(xbrl, encoding='utf-8', method='xml')
        reparsed = minidom.parseString(rough_string)
        reparsed.writexml(open(f'{filename}.xml', 'w'), indent="  ", addindent="  ", newl='\n', encoding="utf-8")

    def uniq(self, lst):
        last = object()
        for item in lst:
            if item == last:
                continue
            yield item
            last = item

    def list_to_dict(self,dict):
        taxis_list = {}
        for item in dict:
            keys = item.keys()
            for key in keys:
                taxis_list[key] = item[key]
        return taxis_list


    def sort_and_deduplicate(self, l):
        return list(self.uniq(sorted(l, reverse=True)))

    def only_axis(self,axis):
        only = []
        if axis!=None:
            for xx in axis:
                only.append(xx.split('|')[0])
            only=list(set(only))
        return only

    def readmapping(self,path):
        with open(path,encoding='utf-8') as f:
            mapping = json.load(f)
        return mapping

    def readxbrl(self,path):
        with open(path, encoding='utf-8') as xml_file:
            instance = xmltodict.parse(xml_file.read())
        xml_root=instance['xbrli:xbrl']
        contexts=xml_root['xbrli:context']
        for context in contexts:
            if 'xbrli:period' in context.keys():
                if 'xbrli:instant' in context['xbrli:period'].keys():
                    self.period=context['xbrli:period']['xbrli:instant']
            if 'xbrli:entity' in context.keys():
                if 'xbrli:identifier' in context['xbrli:entity'].keys():
                    self.ogrn=context['xbrli:entity']['xbrli:identifier']['#text']
            self.context_data[context['@id']]={}
            td_dict = []
            if 'xbrldi:explicitMember' in context['xbrli:scenario'].keys():
                ex_dict=[]
                if type(context['xbrli:scenario']['xbrldi:explicitMember'])==list:
                    for ex in context['xbrli:scenario']['xbrldi:explicitMember']:
                        ex_dict.append(f"{ex['@dimension']}|{ex['#text']}")
                else:
                    ex_dict.append(f"{context['xbrli:scenario']['xbrldi:explicitMember']['@dimension']}|{context['xbrli:scenario']['xbrldi:explicitMember']['#text']}")
            if 'xbrldi:typedMember' in context['xbrli:scenario'].keys():
                for td_key in context['xbrli:scenario']['xbrldi:typedMember'].keys():
                    if '@' not in td_key:
                        taxis_domain = f"{context['xbrli:scenario']['xbrldi:typedMember']['@dimension']}|{td_key}|{context['xbrli:scenario']['xbrldi:typedMember'][td_key]}"
                        td_dict.append(taxis_domain)
            self.context_data[context['@id']]['axis'] = self.sort_and_deduplicate(ex_dict)
            self.context_data[context['@id']]['taxis'] = self.sort_and_deduplicate(td_dict)


        for xx in xml_root.keys():
            if '@' not in xx and 'xbrli:context' != xx and 'xbrli:unit' != xx and 'link:schemaRef' != xx:
                self.varible_data[xx] = {}
                if type(xml_root[xx]) == list:
                    for yy in xml_root[xx]:
                        self.varible_data[xx][yy['@contextRef']] = yy['#text']
                else:
                    self.varible_data[xx][xml_root[xx]['@contextRef']] = xml_root[xx]['#text']

    def parsemapping(self):
        self.to_save_xml={}
        data_dict = self.mapping.get('data')
        self.root = self.mapping.get('root')
        self.root_xml = ET.Element(self.root)
        self.root_xml.attrib = {'xmlns': "",'ВидОЭС':'','ВидОтчета':'','ДатаВремяФормирования':'',
                                'КодФормы':self.root.replace('Ф',''),'ОКУД':self.root.replace('Ф',''),'ОтчДата':self.period,
                                'Периодичность':'','УникИдОЭС':''}
        sostavitel=ET.SubElement(self.root_xml,'Составитель')
        sostavitel.attrib={'БИК':'','ВидОрг':'','ДатаПодписания':'','КодОрг':'','КодТУ':'','ОГРН':self.ogrn,'ОКАТО':'','ОКПО':'',
                           'СокрНаимен':''}
        rukovoditel=ET.SubElement(sostavitel,'Руководитель')
        rukovoditel.attrib={'Должность':'','ФИО':''}
        glavbuh = ET.SubElement(sostavitel, 'ГлавБух')
        glavbuh.attrib = {'Должность': '', 'ФИО': ''}
        ispolnitel = ET.SubElement(sostavitel, 'Исполнитель')
        ispolnitel.attrib = {'Должность': '','Телефон':'', 'ФИО': ''}

        for razdel_key in data_dict.keys():
            parent_temp = self.root_xml
            tag=data_dict[razdel_key]['tag']
            for child in data_dict[razdel_key]['parent_tags']:
                sub = ET.SubElement(parent_temp, child)
                parent_temp = sub
            self.to_save_xml[tag]=sub

            if data_dict[razdel_key]['lines']:
                #lines={tuple(v):k for k, v in data_dict[razdel_key]['lines'].items()}
                lines=data_dict[razdel_key]['lines']
            else:
                lines=None


            axis_list,taxis_list= [],[]
            tag=data_dict[razdel_key].get('tag')
            axis_synt_list_temp={}
            for ax in data_dict[razdel_key]['axiss_y_synthetic'].keys():
                for ax_value in data_dict[razdel_key]['axiss_y_synthetic'][ax].keys():
                    ax_tax=data_dict[razdel_key]['axiss_y_synthetic'][ax][ax_value]
                    axis_list.append({tuple(ax_tax):{'name':ax,'value':ax_value}})
                    axis_synt_list_temp[ax_tax[0]]={'name':ax,'value':ax_value}

            taxis_list_temp={}
            for tax in data_dict[razdel_key]['taxis'].keys():
                tax_tax=data_dict[razdel_key]['taxis'][tax]
                taxis_list.append({tax_tax:tax})
                taxis_list_temp[tax_tax]=tax

            razdel_axis=[]
            for xx in axis_list:
                for yy in xx.keys():
                    razdel_axis=razdel_axis+self.only_axis(list(yy))
            razdel_axis=list(set(razdel_axis))
            razdel_axis.sort()

            razdel_taxis=[]
            for xx in taxis_list:
                for yy in xx.keys():
                    razdel_taxis.append(yy)
            var_list_temp={}
            for var_name in data_dict[razdel_key]['varible'].keys():
                var_tax=data_dict[razdel_key]['varible'][var_name].get('var')
                if data_dict[razdel_key]['varible'][var_name].get('enum'):
                    var_enum={v: k for k, v in data_dict[razdel_key]['varible'][var_name].get('enum').items()}
                else:
                    var_enum=None
                var_axis=data_dict[razdel_key]['varible'][var_name].get('axis')
                var_axis = var_axis if var_axis else []
                #var_list_temp.append({var_tax:{'name':var_name,'var_axis':var_axis,'razdel_axis':razdel_axis,'razdel_taxis':razdel_taxis}})
                #var_list_temp[tuple(var_axis+razdel_axis+razdel_taxis)]={'var_tax':var_tax,'name':var_name,'tag':tag}
                var_list_temp[var_name]={'var_tax':var_tax,'osi':var_axis+razdel_axis+razdel_taxis,'tag':tag,'var_enum':var_enum}
            self.var_list.append({'data': var_list_temp, 'razdel_axis': razdel_axis,'razdel_taxis': razdel_taxis, 'lines': lines})
            self.axis_synt_list.append(axis_synt_list_temp)
            self.taxis_list.append(taxis_list_temp)

        # for xx in self.var_list:
        #     print(xx)


    def find_in_mapping(self,var_taxonomy,axis_taxonomy,taxis_taxonomy):
        taxis_taxonomy_clean=[]
        for xx in taxis_taxonomy:
            taxis_taxonomy_clean.append(xx.split('|')[0]+'|'+xx.split('|')[1])
        for xx in self.var_list:
            for kk in xx['data'].keys():
                if var_taxonomy == xx['data'][kk]['var_tax']:
                    if numpy.isin(xx['razdel_axis'],self.only_axis(axis_taxonomy)).all() and numpy.isin(xx['razdel_taxis'],taxis_taxonomy_clean).all():
                        line_osi = []
                        find_osi = []
                        for zz in axis_taxonomy:
                            if zz.split('|')[0] in xx['razdel_axis']:
                                line_osi.append(zz)
                                find_osi.append(zz.split('|')[0])
                            else:
                                find_osi.append(zz)
                        osi = find_osi + taxis_taxonomy_clean
                        group_osi = line_osi + taxis_taxonomy
                        group_osi.sort()
                        if numpy.isin(xx['data'][kk]['osi'],osi).all() and numpy.isin(osi,xx['data'][kk]['osi']).all():
                            razdel=xx['data'][kk]['tag']
                            name=kk
                            var_enum=xx['data'][kk]['var_enum']
                            if xx['lines']:
                                for ll in xx['lines'].keys():
                                    if numpy.isin(xx['lines'][ll]['axis'],line_osi).all():
                                        line_name=ll
                                        line_order=xx['lines'][ll]['order']
                            else:
                                line_name=razdel
                                line_order=999
        return {'group_osi':group_osi,'razdel':razdel,'name':name,'line_name':line_name,'line_order':line_order,'var_enum':var_enum}

    def do_line(self):
        final=[]
        for xx in self.varible_data.keys():
            for yy in self.varible_data[xx]:
                value=self.varible_data[xx][yy]
                axis=self.context_data[yy]['axis']
                taxis=self.context_data[yy]['taxis']
                parse_result=self.find_in_mapping(xx,axis,taxis)
                final.append({'group_osi':parse_result['group_osi'],
                              'razdel':parse_result['razdel'],
                              'line_name':parse_result['line_name'],
                              'line_order':parse_result['line_order'],
                              'name':parse_result['name'],
                              'value':parse_result['var_enum'].get(value) if parse_result['var_enum'] else value})
        # for xx in final:
        #     print(xx)
        return final

    def do_xml(self,data):
        to_save=[]
        taxis_dict=self.list_to_dict(self.taxis_list)
        axis_dict=self.list_to_dict(self.axis_synt_list)
        group_list=self.sort_and_deduplicate([xx['group_osi'] for xx in data])
        group_list.sort()
        for xx in group_list:
            one_line={}
            for oo in xx:
                if len(oo.split('|'))==3:
                    one_line[taxis_dict.get(oo.split('|')[0]+'|'+oo.split('|')[1]).replace('@','')]=oo.split('|')[2]
                elif len(oo.split('|'))==2:
                    one_line[axis_dict[oo].get('name').replace('@','')]=axis_dict[oo].get('value')
            for yy in data:
                if yy['group_osi']==xx:
                    one_line[yy['name'].replace('@','')]=yy['value']
                    parent_elem=self.to_save_xml[yy['razdel']]
                    line_name=yy['line_name']
                    line_order=yy['line_order']
            sub_elem=ET.Element(line_name)
            sub_elem.attrib=one_line
            to_save.append({'line_order':line_order,'line_name':line_name,'parent': parent_elem,'element':sub_elem})

        to_save=sorted(to_save, key=operator.itemgetter('line_order'))
        for xx in to_save:
            xx['parent'].append(xx['element'])

if __name__ == "__main__":
    ss=transformxml('mapping_0409728_test.json')
    ss.readxbrl('report_0409728_output.xml')
    ss.parsemapping()
    ss.do_xml(ss.do_line())
    ss.saveXBRL(ss.root_xml,'report_0409728_REoutput')

    ss=transformxml('mapping_0409725_old.json')
    ss.readxbrl('report_0409725_output.xml')
    ss.parsemapping()
    ss.do_xml(ss.do_line())
    ss.saveXBRL(ss.root_xml,'report_0409725_REoutput')