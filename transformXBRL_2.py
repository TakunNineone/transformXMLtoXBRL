import itertools,collections,xmltodict,json,xml.dom.minidom as minidom,xml.etree.ElementTree as ET
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime
import numpy
import hashlib
import itertools

class transformxml():
    def __init__(self, path):
        self.mapping = self.readmapping(path)
        self.context_data= {}
        self.varible_data= {}
        self.data_list_reverse= {}
        self.axis_synt_list=[]
        self.taxis_list=[]
        self.var_list=[]

    def uniq(self, lst):
        last = object()
        for item in lst:
            if item == last:
                continue
            yield item
            last = item

    def sort_and_deduplicate(self, l):
        return list(self.uniq(sorted(l, reverse=True)))

    def only_axis(self,axis):
        only = []
        if axis!=None:
            for xx in axis:
                only.append(xx.split('|')[0])
            only=list(set(only))
        return only

    def minus_list(self,list1,list2):
        list3=[]
        if list1!=[]:
            for xx in list1:
                if xx not in list2:
                    list3.append(xx)
        else:
            list3=list2
        return list3

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
            self.context_data[context['@id']]={}
            td_dict = []
            td_dict_only=[]
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
                        taxis_domain_only=f"{context['xbrli:scenario']['xbrldi:typedMember']['@dimension']}|{td_key}"
                        td_dict.append(taxis_domain)
                        td_dict_only.append(taxis_domain_only)
            self.context_data[context['@id']]['axis'] = self.sort_and_deduplicate(ex_dict)
            self.context_data[context['@id']]['taxis'] = self.sort_and_deduplicate(td_dict)
            self.context_data[context['@id']]['only_taxis'] = self.sort_and_deduplicate(td_dict_only)
        # for xx in self.context_data.keys():
        #     print(xx,self.context_data[xx])

        for xx in xml_root.keys():
            if '@' not in xx and 'xbrli:context' != xx and 'xbrli:unit' != xx and 'link:schemaRef' != xx:
                self.varible_data[xx] = {}
                if type(xml_root[xx]) == list:
                    for yy in xml_root[xx]:
                        self.varible_data[xx][yy['@contextRef']] = yy['#text']
                else:
                    self.varible_data[xx][xml_root[xx]['@contextRef']] = xml_root[xx]['#text']

    def parsemapping(self):
        data_dict = self.mapping.get('data')
        for razdel_key in data_dict.keys():
            axis_list,taxis_list= [],[]
            tag=data_dict[razdel_key].get('tag')
            axis_synt_list_temp={}
            for ax in data_dict[razdel_key]['axiss_y_synthetic'].keys():
                for ax_value in data_dict[razdel_key]['axiss_y_synthetic'][ax].keys():
                    ax_tax=data_dict[razdel_key]['axiss_y_synthetic'][ax][ax_value]
                    axis_list.append({tuple(ax_tax):{'name':ax,'value':ax_value}})
                    axis_synt_list_temp[tuple(ax_tax)]={'name':ax,'value':ax_value}

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

            var_list_temp1={}
            var_list_temp={}
            for var_name in data_dict[razdel_key]['varible'].keys():
                var_tax=data_dict[razdel_key]['varible'][var_name].get('var')
                var_axis=data_dict[razdel_key]['varible'][var_name].get('axis')
                var_axis = var_axis if var_axis else []
                #var_list_temp.append({var_tax:{'name':var_name,'var_axis':var_axis,'razdel_axis':razdel_axis,'razdel_taxis':razdel_taxis}})
                var_list_temp1[tuple(var_axis+razdel_axis+razdel_taxis)]={'name':var_name,'tag':tag}
                var_list_temp[var_tax]=var_list_temp1
            # print(var_list_temp)
            self.axis_synt_list.append(axis_synt_list_temp)
            self.taxis_list.append(taxis_list_temp)
            self.var_list.append({'data':var_list_temp,'razdel_axis':razdel_axis,'razdel_taxis':razdel_taxis})
            # print(self.var_list)

        # for xx in self.taxis_list:
        #     print(xx)

    def find_in_mapping(self,var_taxonomy,axis_taxonomy,taxis_taxonomy):
        taxis_taxonomy_clean=[]
        for xx in taxis_taxonomy:
            taxis_taxonomy_clean.append(xx.split('|')[0]+'|'+xx.split('|')[1])
        for xx in self.var_list:
            if var_taxonomy in xx['data'].keys():
                line_osi = []
                find_osi = []
                group_osi = []
                for zz in axis_taxonomy:
                    if zz.split('|')[0] in xx['razdel_axis']:
                        line_osi.append(zz)
                        find_osi.append(zz.split('|')[0])
                    else:
                        find_osi.append(zz)
                osi=find_osi+taxis_taxonomy_clean
                group_osi=line_osi+taxis_taxonomy
                group_osi.sort()
                for kk in xx['data'][var_taxonomy].keys():
                    if numpy.isin(list(kk),osi).all() and numpy.isin(osi,list(kk)).all():
                        razdel=xx['data'][var_taxonomy][kk]['tag']
                        name=xx['data'][var_taxonomy][kk]['name']
        return {'group_ois':group_osi,'razdel':razdel,'name':name,'line_osi':line_osi}

    def do_line(self):
        for xx in self.varible_data.keys():
            for yy in self.varible_data[xx]:
                axis=self.context_data[yy]['axis']
                taxis=self.context_data[yy]['taxis']
                parse_result=self.find_in_mapping(xx,axis,taxis)
                print(parse_result,self.varible_data[xx][yy])


                # print(var_taxonomy)
        # print(axis_taxonomy)
        # print(taxis_taxonomy)
        # for xx in self.var_list:
        #     if var_taxonomy in xx.keys():
        #         print(xx[var_taxonomy])
        #         print(axis_taxonomy)
        #         print(taxis_taxonomy)





if __name__ == "__main__":
    ss=transformxml('mapping_0409725_old.json')
    ss.readxbrl('report_0409725_output.xml')
    ss.parsemapping()
    # ss.find_in_mapping('nfo-dic:GosRegNomerVyp',['dim-int:Uroven_riskaAxis|mem-int:StandartMember', 'dim-int:Tip_i_status_klientaAxis|mem-int:FLMember', 'dim-int:Rezident_nerezidentAxis|mem-int:RezidentMember'],
    #                    ['dim-int:ID_CzennojBumagiTaxis|dim-int:ID_CzennojBumagi_TypedName|RU0007661625'])
    # ss.find_in_mapping('ko-dic:Kol_nepokr_poz',['dim-int:Uroven_riskaAxis|mem-int:PovyshMember', 'dim-int:Tip_i_status_klientaAxis|mem-int:YULMember', 'dim-int:Rezident_nerezidentAxis|mem-int:NerezidentMember', 'dim-int:PozicziyaPoSdelkeAxis|mem-int:KorotkayaMember'],[])
    ss.do_line()