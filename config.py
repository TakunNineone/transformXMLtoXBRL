schemaref='http://www.cbr.ru/xbrl/nso/ko/rep/2022-11-30/ep/ep_SR_0409725.xsd'

xbrl_header={'xmlns:mem-int': 'http://www.cbr.ru/xbrl/udr/dom/mem-int',
                       'xmlns:xlink': 'http://www.w3.org/1999/xlink',
                       'xmlns:ko-dic': 'http://www.cbr.ru/xbrl/nso/ko/dic/ko-dic',
                       'xmlns:dim-int': 'http://www.cbr.ru/xbrl/udr/dim/dim-int',
                       'xmlns:iso4217': 'http://www.xbrl.org/2003/iso4217',
                       'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                       'xmlns:link': 'http://www.xbrl.org/2003/linkbase',
                       'xmlns:nfo-dic': 'http://www.cbr.ru/xbrl/nso/nfo/dic',
                       'xmlns:xbrldi': 'http://xbrl.org/2006/xbrldi',
                       'xmlns:xbrli': 'http://www.xbrl.org/2003/instance'}

units={
	'unit1':{'id':'pure','text':'xbrli:pure'},
	'unit2':{'id':'RUB','text':'iso4217:RUB'}
	}


schemaref='http://www.cbr.ru/xbrl/nso/ko/rep/2022-11-30/ep/ep_SR_0409725.xsd'

xbrl_header={'xmlns:mem-int': 'http://www.cbr.ru/xbrl/udr/dom/mem-int',
                       'xmlns:xlink': 'http://www.w3.org/1999/xlink',
                       'xmlns:ko-dic': 'http://www.cbr.ru/xbrl/nso/ko/dic/ko-dic',
                       'xmlns:dim-int': 'http://www.cbr.ru/xbrl/udr/dim/dim-int',
                       'xmlns:iso4217': 'http://www.xbrl.org/2003/iso4217',
                       'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                       'xmlns:link': 'http://www.xbrl.org/2003/linkbase',
                       'xmlns:nfo-dic': 'http://www.cbr.ru/xbrl/nso/nfo/dic',
                       'xmlns:xbrldi': 'http://xbrl.org/2006/xbrldi',
                       'xmlns:xbrli': 'http://www.xbrl.org/2003/instance'}

units={
	'unit1':{'id':'pure','text':'xbrli:pure'},
	'unit2':{'id':'RUB','text':'iso4217:RUB'}
	}


schemaref='http://www.cbr.ru/xbrl/nso/ko/rep/2022-11-30/ep/ep_SR_0409725.xsd'

xbrl_header={'xmlns:mem-int': 'http://www.cbr.ru/xbrl/udr/dom/mem-int',
                       'xmlns:xlink': 'http://www.w3.org/1999/xlink',
                       'xmlns:ko-dic': 'http://www.cbr.ru/xbrl/nso/ko/dic/ko-dic',
                       'xmlns:dim-int': 'http://www.cbr.ru/xbrl/udr/dim/dim-int',
                       'xmlns:iso4217': 'http://www.xbrl.org/2003/iso4217',
                       'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                       'xmlns:link': 'http://www.xbrl.org/2003/linkbase',
                       'xmlns:nfo-dic': 'http://www.cbr.ru/xbrl/nso/nfo/dic',
                       'xmlns:xbrldi': 'http://xbrl.org/2006/xbrldi',
                       'xmlns:xbrli': 'http://www.xbrl.org/2003/instance'}

units={
	'unit1':{'id':'pure','text':'xbrli:pure'},
	'unit2':{'id':'RUB','text':'iso4217:RUB'}
	}


schemaref='http://www.cbr.ru/xbrl/nso/ko/rep/2022-11-30/ep/ep_SR_0409725.xsd'

xbrl_header={'xmlns:mem-int': 'http://www.cbr.ru/xbrl/udr/dom/mem-int',
                       'xmlns:xlink': 'http://www.w3.org/1999/xlink',
                       'xmlns:ko-dic': 'http://www.cbr.ru/xbrl/nso/ko/dic/ko-dic',
                       'xmlns:dim-int': 'http://www.cbr.ru/xbrl/udr/dim/dim-int',
                       'xmlns:iso4217': 'http://www.xbrl.org/2003/iso4217',
                       'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                       'xmlns:link': 'http://www.xbrl.org/2003/linkbase',
                       'xmlns:nfo-dic': 'http://www.cbr.ru/xbrl/nso/nfo/dic',
                       'xmlns:xbrldi': 'http://xbrl.org/2006/xbrldi',
                       'xmlns:xbrli': 'http://www.xbrl.org/2003/instance'}

units={
	'unit1':{'id':'pure','text':'xbrli:pure'},
	'unit2':{'id':'RUB','text':'iso4217:RUB'}
	}


mapping={
    'razdel1':{
        'root':'Ф0409725',
        'tag':'Ф0409725_Раздел1_Идент',
        'axis': {
            '@Резидентность':{
                'Резидент':{'member':'mem-int:RezidentMember','axis':'dim-int:Rezident_nerezidentAxis'},
                'Нерезидент':{'member':'mem-int:NerezidentMember', 'axis':'dim-int:Rezident_nerezidentAxis'}},
            '@Тип_Клиента':{
                'ФЛ':{'member':'mem-int:FLMember','axis':'dim-int:Tip_i_status_klientaAxis'},
                'ЮЛ':{'member':'mem-int:YULMember','axis':'dim-int:Tip_i_status_klientaAxis'}},
            '@Уровень_Риска':{
                'Стандартный':{'member':'mem-int:StandartMember','axis':'dim-int:Uroven_riskaAxis'},
                'Повышенный':{'member':'mem-int:PovyshMember','axis':'dim-int:Uroven_riskaAxis'},
                'Особый':{'member':'mem-int:OsobMember','axis':'dim-int:Uroven_riskaAxis'}}
                        },
        'varible':
            {
                '@КолКлиенНепокрПоз': {'var': 'ko-dic:Kol_nepokr_poz', 'decimals': '0', 'unit': 'pure'},
                '@СумЗначПланПозКлиент': {'var': 'ko-dic:Summ_plan_poz', 'decimals': '2', 'unit': 'RUB'},
                '@СумЗначОтрПланПозКлиент': {'var': 'ko-dic:Summ_otricz_plan_poz', 'decimals': '2', 'unit': 'RUB'},
                '@СумЗначОтрПланПозКлиентНомВал': {'var': 'ko-dic:Summ_otricz_plan_pozNomInVal', 'decimals': '2','unit': 'RUB'},
                '@СумЗначОтрПланПозКлиентДрагМет': {'var': 'ko-dic:Summ_otricz_plan_pozDragMet', 'decimals': '2','unit': 'RUB'},
                '@СумНедостСредИспНПР1': {'var': 'ko-dic:NedostSrNorm', 'decimals': '2', 'unit': 'RUB'}
            },
        'axis_varible':{
            '@КолКлиенНепокрПозПозСделКор': {
                'axiss':[{'axis': 'dim-int:PozicziyaPoSdelkeAxis', 'member': 'mem-int:KorotkayaMember'}],
                'decimals': '0','unit': 'pure','var': 'ko-dic:Kol_nepokr_poz'},
            '@КолКлиенНепокрПозПозСделДлин': {'axiss':[{'axis': 'dim-int:PozicziyaPoSdelkeAxis', 'member': 'mem-int:DlinnayaMember'}],
                                              'decimals': '0', 'unit': 'pure','var': 'ko-dic:Kol_nepokr_poz'},
            '@СумЗначНепокрПозПозСделКорВалРФЭквРуб': {'axiss':[{'axis': 'dim-int:PozicziyaPoSdelkeAxis', 'member': 'mem-int:KorotkayaMember'},
                {'axis': 'dim-int:NaczVal_RubEkvAxis', 'member': 'mem-int:Rubli_Member'}],
                'decimals': '2', 'unit': 'RUB','var':'ko-dic:SumNepokPoz'},
            '@СумЗначНепокрПозПозСделКорВалРФЭквВал': {'axiss':[
                {'axis': 'dim-int:PozicziyaPoSdelkeAxis', 'member': 'mem-int:KorotkayaMember'},
                {'axis': 'dim-int:NaczVal_RubEkvAxis', 'member': 'mem-int:ValyutaMember'}],'decimals': '2', 'unit': 'RUB','var':'ko-dic:SumNepokPoz'},
            '@СумЗначНепокрПозПозСделКорВалРФЭквДрагМет': {'axiss':[
                {'axis': 'dim-int:PozicziyaPoSdelkeAxis', 'member': 'mem-int:KorotkayaMember'},
                {'axis': 'dim-int:NaczVal_RubEkvAxis', 'member': 'mem-int:DragoczennyeMetallyMember'}],'decimals': '2', 'unit': 'RUB','var':'ko-dic:SumNepokPoz'},
            '@СумЗначНепокрПозПозСделДлинВалРФЭквРуб': {'axiss':[
                {'axis': 'dim-int:PozicziyaPoSdelkeAxis', 'member': 'mem-int:DlinnayaMember'},
                {'axis': 'dim-int:NaczVal_RubEkvAxis', 'member': 'mem-int:Rubli_Member'}],'decimals': '2', 'unit': 'RUB','var':'ko-dic:SumNepokPoz'},
            '@СумЗначНепокрПозПозСделДлинВалРФЭквВал': {'axiss':[{'axis': 'dim-int:PozicziyaPoSdelkeAxis', 'member': 'mem-int:DlinnayaMember'},
                {'axis': 'dim-int:NaczVal_RubEkvAxis', 'member': 'mem-int:ValyutaMember'}],'decimals': '2', 'unit': 'RUB','var':'ko-dic:SumNepokPoz'},
            '@СумЗначНепокрПозПозСделДлинВалРФЭквДрагМет': {'axiss':[{'axis': 'dim-int:PozicziyaPoSdelkeAxis', 'member': 'mem-int:DlinnayaMember'},
                {'axis': 'dim-int:NaczVal_RubEkvAxis', 'member': 'mem-int:DragoczennyeMetallyMember'}],'decimals': '2', 'unit': 'RUB','var':'ko-dic:SumNepokPoz'},
			'@СумКорПланПозВалДолСША':{'axiss':[{'axis':'dim-int:Valyuta_Inf_baz_akt_svop_dogValyutaAxis','member':'mem-int:Dollar_SSHAMember'}],
			'decimals': '2', 'unit': 'RUB','var':'ko-dic:SumKorPlanPoz'},
			'@СумКорПланПозВалЕвро':{'axiss':[{'axis':'dim-int:Valyuta_Inf_baz_akt_svop_dogValyutaAxis','member':'mem-int:EvroMember'}],
			'decimals': '2', 'unit': 'RUB','var':'ko-dic:SumKorPlanPoz'}
        },
        'taxis': {}
    }
    ,
    'razdel2':{
        'root':'Ф0409725',
        'tag':'Ф0409725_Раздел2_Строка',
        'axis': {
            '@Резидентность':{
                'Резидент':{'member':'mem-int:RezidentMember','axis':'dim-int:Rezident_nerezidentAxis'},
                'Нерезидент':{'member':'mem-int:NerezidentMember', 'axis':'dim-int:Rezident_nerezidentAxis'}},
            '@Тип_Клиента':{
                'ФЛ':{'member':'mem-int:FLMember','axis':'dim-int:Tip_i_status_klientaAxis'},
                'ЮЛ':{'member':'mem-int:YULMember','axis':'dim-int:Tip_i_status_klientaAxis'}},
            '@Уровень_Риска':{
                'Стандартный':{'member':'mem-int:StandartMember','axis':'dim-int:Uroven_riskaAxis'},
                'Повышенный':{'member':'mem-int:PovyshMember','axis':'dim-int:Uroven_riskaAxis'},
                'Особый':{'member':'mem-int:OsobMember','axis':'dim-int:Uroven_riskaAxis'}}
                },
        'axis_varible':{},
        'taxis':{
            '@ДатаТоргДеньОтчПер':{'member':'dim-int:Data_Torg_denTypedname','taxis':'dim-int:Data_Torg_den_Taxis'}
                },
        'varible':
            {
                '@КолКлиентОтрНПР2':{'var':'ko-dic:Kol_OtrNPR_poz','decimals':'0','unit':'pure'}
            }
    },
'razdel3':
    {
        'root':'Ф0409725',
        'tag':'Ф0409725_Раздел3_Строка',
        'axis':{
            '@Резидентность':{
                'Резидент':{'member':'mem-int:RezidentMember','axis':'dim-int:Rezident_nerezidentAxis'},
                'Нерезидент':{'member':'mem-int:NerezidentMember', 'axis':'dim-int:Rezident_nerezidentAxis'}},
            '@Тип_Клиента':{
                'ФЛ':{'member':'mem-int:FLMember','axis':'dim-int:Tip_i_status_klientaAxis'},
                'ЮЛ':{'member':'mem-int:YULMember','axis':'dim-int:Tip_i_status_klientaAxis'}},
            '@Уровень_Риска':{
                'Стандартный':{'member':'mem-int:StandartMember','axis':'dim-int:Uroven_riskaAxis'},
                'Повышенный':{'member':'mem-int:PovyshMember','axis':'dim-int:Uroven_riskaAxis'},
                'Особый':{'member':'mem-int:OsobMember','axis':'dim-int:Uroven_riskaAxis'}}},
		'axis_varible':{},
		'taxis':{
                '@ИДЦенБум':{'member':'dim-int:ID_CzennojBumagi_TypedName','taxis':'dim-int:ID_CzennojBumagiTaxis'}
        },
        'varible':{
            '@ИДЦенБум':{'var':'nfo-dic:ISIN','decimals':'','unit':''},
            '@РегНомИдентНомВып':{'var':'nfo-dic:GosRegNomerVyp','decimals':'','unit':''},
            '@СумКорПланПоз':{'var':'ko-dic:SumKorPlanPoz', 'decimals': '2', 'unit': 'RUB'},
                   }
        }
}





