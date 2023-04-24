import itertools,collections,xmltodict,json,xml.dom.minidom as minidom,xml.etree.ElementTree as ET
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime
import numpy

class transformxml():
    def __init__(self, path):
        self.mapping = self.readmapping(path)

    def readmapping(self,path):
        with open(path,encoding='utf-8') as f:
            mapping = json.load(f)
        return mapping

    def only_axis(self,axis):
        only = []
        if axis!=None:
            for xx in axis:
                only.append(xx.split('|')[0])
            only=list(set(only))
        return only

    def uniq(self,lst):
        last = object()
        for item in lst:
            if item == last:
                continue
            yield item
            last = item

    def sort_and_deduplicate(self,l):
        return list(self.uniq(sorted(l, reverse=True)))

    def readxbrl(self,path):
        with open(path, encoding='utf-8') as xml_file:
            instance = xmltodict.parse(xml_file.read())
        xml_root=instance['xbrli:xbrl']
        contexts=xml_root['xbrli:context']
        context_data={}
        varible_data={}
        for context in contexts:
            context_data[context['@id']]={}
            td_dict = []
            if 'xbrldi:explicitMember' in context['xbrli:scenario'].keys():
                ex_dict=[]
                if type(context['xbrli:scenario']['xbrldi:explicitMember'])==list:
                    for ex in context['xbrli:scenario']['xbrldi:explicitMember']:
                        ex_dict.append(ex['@dimension']+'|'+ex['#text'])
                else:
                    ex_dict.append(context['xbrli:scenario']['xbrldi:explicitMember']['@dimension'] + '|' + context['xbrli:scenario']['xbrldi:explicitMember']['#text'])
                context_data[context['@id']]['axis']=ex_dict

            if 'xbrldi:typedMember' in context['xbrli:scenario'].keys():
                if type(context['xbrli:scenario']['xbrldi:typedMember']) == list:
                    for td_key in context['xbrli:scenario']['xbrldi:typedMember'].keys():
                        if '@' not in td_key:
                            domain_name=td_key
                        taxis=context['xbrli:scenario']['xbrldi:typedMember']['@dimension']
                        taxis_domain=taxis+'|'+domain_name+'|'+context['xbrli:scenario']['xbrldi:typedMember'][domain_name]
                        td_dict.append(taxis_domain)
                    context_data[context['@id']]['taxis']= td_dict
                else:
                    for td_key in context['xbrli:scenario']['xbrldi:typedMember'].keys():
                        if '@' not in td_key:
                            domain_name = td_key
                    taxis = context['xbrli:scenario']['xbrldi:typedMember']['@dimension']
                    taxis_domain = taxis + '|' + domain_name + '|' + context['xbrli:scenario']['xbrldi:typedMember'][
                        domain_name]
                    td_dict.append(taxis_domain)
            context_data[context['@id']]['taxis'] = td_dict
        # for xx in context_data.keys():
        #     print(xx,context_data[xx])
        # print('------------------------------------------------------------------------------------------------------')
        for xx in xml_root.keys():
            if '@' not in xx and 'xbrli:context'!=xx and 'xbrli:unit'!=xx and 'link:schemaRef'!=xx:
                varible_data[xx] = {}
                #context_data[xml_root[xx]['@contextRef']][xx]=xml_root[xx]['#text']
                if type(xml_root[xx])==list:
                    for yy in xml_root[xx]:
                        varible_data[xx][yy['@contextRef']]=yy['#text']
                else:
                    varible_data[xx][xml_root[xx]['@contextRef']] = xml_root[xx]['#text']
        # for xx in varible_data.keys():
        #     print(xx,varible_data[xx])

        data_dict=self.mapping.get('data')
        data_list_reverse=[]
        for razdel_key in data_dict.keys():
            razdel_axis=[]
            for axis_synt in data_dict[razdel_key]['axiss_y_synthetic'].keys():
                for axis_synt_value in data_dict[razdel_key]['axiss_y_synthetic'][axis_synt].keys():
                    for axis_synt_value_final in data_dict[razdel_key]['axiss_y_synthetic'][axis_synt][axis_synt_value]:
                        razdel_axis.append(axis_synt_value_final)
            razdel_axis=self.only_axis(razdel_axis)
            razdel_axis.sort()

            razdel_taxis=[]
            for taxis_key in data_dict[razdel_key]['taxis'].keys():
                razdel_taxis.append(data_dict[razdel_key]['taxis'][taxis_key])
            razdel_taxis.sort()

            for varible_key in data_dict[razdel_key]['varible'].keys():
                # varible_axis=self.only_axis(data_dict[razdel_key]['varible'][varible_key]['axis'])
                data_list_reverse.append({'razdel':razdel_key,'var':data_dict[razdel_key]['varible'][varible_key]['var'],
                                          'razdel_axis': razdel_axis,
                                          'varible_axis': data_dict[razdel_key]['varible'][varible_key]['axis'],
                                          'taxis':razdel_taxis,
                                          'name':varible_key})

        # for xx in data_list_reverse:
        #     print(xx)
        final_data=[]
        for var in varible_data.keys():
            for cont in varible_data[var].keys():
                context=cont
                value=varible_data[var][cont]
                axis=context_data[cont].get('axis')
                axis.sort()
                taxis=context_data[cont].get('taxis')
                only_axis=self.only_axis(axis)
                only_axis.sort()
                for xx in data_list_reverse:
                    if xx['var']==var and numpy.isin(xx['varible_axis'],axis).all():
                        #final_data.append([list(set(axis) - set(xx['varible_axis'])),var,context,xx['name'],value])
                        temp_razde_axis=list(set(axis) - set(xx['varible_axis']))
                        temp_razde_axis.sort()
                        final_data.append({'razdel':xx['razdel'],'razdel_axis':temp_razde_axis,'razdel_taxis':taxis,'var':var,'context':context,'name':xx['name'],'value':value})
                        #print(var, context, [tt.split('|')[0]+tt.split('|')[1] for tt in taxis],xx['taxis'])
                    elif xx['var']==var and numpy.isin(xx['razdel_axis'],only_axis).all() and numpy.isin(only_axis,xx['razdel_axis']).all() and xx['varible_axis']==None:
                        #final_data.append([axis, var, context, xx['name'], value])
                        final_data.append({'razdel':xx['razdel'],'razdel_axis': axis,'razdel_taxis':taxis, 'var':var,'context':context,'name':xx['name'],'value':value})
                        #print(var, context, [tt.split('|')[0]+tt.split('|')[1] for tt in taxis],xx['taxis'])

        for xx in range(len(final_data)):
            final_data[xx]['group_osi']=final_data[xx].get('razdel_axis')+final_data[xx].get('razdel_taxis')

        # for xx in final_data:
        #     print(xx)

        line_group=[xx.get('group_osi') for xx in final_data]
        line_group.sort()
        result_otchet= {}
        for group_osi in self.sort_and_deduplicate(line_group):
            result_otchet[str(group_osi)]={}
            for xx in final_data:
                if numpy.isin(xx['group_osi'],group_osi).all() and numpy.isin(group_osi,xx['group_osi']).all():
                    result_otchet[str(group_osi)]['razdel'] = xx['razdel']
                    result_otchet[str(group_osi)][xx['name']] = xx['value']

        for xx in result_otchet.keys():
            print(xx,result_otchet[xx])

if __name__ == "__main__":
    ss=transformxml('mapping_0409725_old.json')
    ss.readxbrl('report_0409725_output.xml')
