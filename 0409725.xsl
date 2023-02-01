<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
                xmlns:report_0409725="urn:cbr-ru:rep0409725:v1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:exslt="http://exslt.org/common"
                xmlns:ko-dic="http://www.cbr.ru/xbrl/nso/ko/dic/ko-dic"
                xmlns:purcb-dic="http://www.cbr.ru/xbrl/nso/purcb/dic/purcb-dic"
                xmlns:link="http://www.xbrl.org/2003/linkbase"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
                xmlns:mem-int="http://www.cbr.ru/xbrl/udr/dom/mem-int"
                xmlns:xbrldi="http://xbrl.org/2006/xbrldi"
                xmlns:dim-int="http://www.cbr.ru/xbrl/udr/dim/dim-int"
                xmlns:xbrli="http://www.xbrl.org/2003/instance"
                xmlns:fn="http://www.w3.org/2005/xpath-functions"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:nfo-dic="http://www.cbr.ru/xbrl/nso/nfo/dic">
	<xsl:output method="xml"
	            indent="yes"/>
	<xsl:variable name="periodEnd"
	              select="//report_0409725:Ф0409725/@ОтчДата"/>
	<xsl:variable name="periodStart"
	              select="(if ((fn:month-from-date(xs:date($periodEnd))=3) or (fn:month-from-date(xs:date($periodEnd))=12) or (fn:month-from-date(xs:date($periodEnd))=9)) then (xs:date($periodEnd) - xs:yearMonthDuration('P3M')) else (xs:date($periodEnd) - xs:yearMonthDuration('P3M') + xs:dayTimeDuration('P1D'))) + xs:dayTimeDuration('P1D')"/>
	<xsl:variable name="identifier"
	              select="//report_0409725:Ф0409725/@ОГРН"/>
	<xsl:variable name="scheme"
	              select="'http://www.cbr.ru'"/>
	<xsl:template name="unit_add">
		<xsl:param name="unit_id"/>
		<xsl:param name="measure"/>
		<xbrli:unit>
			<xsl:attribute name="id">
				<xsl:value-of select="$unit_id"/>
			</xsl:attribute>
			<xbrli:measure>
				<xsl:value-of select="$measure"/>
			</xbrli:measure>
		</xbrli:unit>
	</xsl:template>
	<xsl:template name="dimensions_add">
		<xsl:param name="dimensions"/>
		<xsl:param name="type"/>
		<xsl:for-each select="exslt:node-set($dimensions)//item">
			<xsl:choose>
				<xsl:when test="$type = 'explicit'">
					<xbrldi:explicitMember>
						<xsl:attribute name="dimension">
							<xsl:value-of select="@dimension"/>
						</xsl:attribute>
						<xsl:value-of select="node()"/>
					</xbrldi:explicitMember>
				</xsl:when>
				<xsl:when test="$type = 'typed'">
					<xbrldi:typedMember>
						<xsl:attribute name="dimension">
							<xsl:value-of select="@dimension"/>
						</xsl:attribute>
						<xsl:copy-of select="node()"/>
					</xbrldi:typedMember>
				</xsl:when>
			</xsl:choose>
		</xsl:for-each>
	</xsl:template>
	<xsl:template name="context_add">
		<xsl:param name="context_id"/>
		<xsl:param name="period_type"/>
		<xsl:param name="explicit_dimensions"/>
		<xsl:param name="typed_dimensions"/>
		<xbrli:context>
			<xsl:attribute name="id">
				<xsl:value-of select="$context_id"/>
			</xsl:attribute>
			<xbrli:entity>
				<xbrli:identifier>
					<xsl:attribute name="scheme">
						<xsl:value-of select="$scheme"/>
					</xsl:attribute>
					<xsl:value-of select="$identifier"/>
				</xbrli:identifier>
			</xbrli:entity>
			<xbrli:period>
				<xsl:choose>
					<xsl:when test="$period_type = 'instant'">
						<xbrli:instant>
							<xsl:value-of select="$periodEnd"/>
						</xbrli:instant>
					</xsl:when>
					<xsl:when test="$period_type = 'duration'">
						<xbrli:startDate>
							<xsl:value-of select="$periodStart"/>
						</xbrli:startDate>
						<xbrli:endDate>
							<xsl:value-of select="$periodEnd"/>
						</xbrli:endDate>
					</xsl:when>
				</xsl:choose>
			</xbrli:period>
			<xsl:if test="($explicit_dimensions != '') or ($typed_dimensions != '')">
				<xbrli:scenario>
					<xsl:if test="$explicit_dimensions != ''">
						<xsl:call-template name="dimensions_add">
							<xsl:with-param name="dimensions"
							                select="$explicit_dimensions"/>
							<xsl:with-param name="type"
							                select="'explicit'"/>
						</xsl:call-template>
					</xsl:if>
					<xsl:if test="$typed_dimensions != ''">
						<xsl:call-template name="dimensions_add">
							<xsl:with-param name="dimensions"
							                select="$typed_dimensions"/>
							<xsl:with-param name="type"
							                select="'typed'"/>
						</xsl:call-template>
					</xsl:if>
				</xbrli:scenario>
			</xsl:if>
		</xbrli:context>
	</xsl:template>
	<xsl:template match="//report_0409725:Ф0409725">
		<xbrli:xbrl>
			<link:schemaRef xlink:type="simple"
			                xlink:href="http://www.cbr.ru/xbrl/nso/ko/rep/2022-11-30/ep/ep_SR_0409725.xsd"/>
			<xsl:for-each select="//report_0409725:Ф0409725_Раздел1/*">
				<xsl:if test="@КолКлиенНепокрПоз != '' or @СумЗначПланПозКлиент != '' or @СумЗначОтрПланПозКлиент != '' or @СумЗначОтрПланПозКлиентНомВал != '' or @СумЗначОтрПланПозКлиентДрагМет != '' or @СумНедостСредИспНПР1 != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_1_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@КолКлиенНепокрПозПозСделКор != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_2_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:PozicziyaPoSdelkeAxis">mem-int:KorotkayaMember</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@КолКлиенНепокрПозПозСделДлин != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_3_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:PozicziyaPoSdelkeAxis">mem-int:DlinnayaMember</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделКорВалРФЭквРуб != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_4_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:PozicziyaPoSdelkeAxis">mem-int:KorotkayaMember</item>
							<item dimension="dim-int:NaczVal_RubEkvAxis">mem-int:Rubli_Member</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделКорВалРФЭквВал != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_5_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:PozicziyaPoSdelkeAxis">mem-int:KorotkayaMember</item>
							<item dimension="dim-int:NaczVal_RubEkvAxis">mem-int:ValyutaMember</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделКорВалРФЭквДрагМет != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_6_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:PozicziyaPoSdelkeAxis">mem-int:KorotkayaMember</item>
							<item dimension="dim-int:NaczVal_RubEkvAxis">mem-int:DragoczennyeMetallyMember</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделДлинВалРФЭквРуб != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_7_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:PozicziyaPoSdelkeAxis">mem-int:DlinnayaMember</item>
							<item dimension="dim-int:NaczVal_RubEkvAxis">mem-int:Rubli_Member</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделДлинВалРФЭквВал != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_8_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:PozicziyaPoSdelkeAxis">mem-int:DlinnayaMember</item>
							<item dimension="dim-int:NaczVal_RubEkvAxis">mem-int:ValyutaMember</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделДлинВалРФЭквДрагМет != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_9_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:PozicziyaPoSdelkeAxis">mem-int:DlinnayaMember</item>
							<item dimension="dim-int:NaczVal_RubEkvAxis">mem-int:DragoczennyeMetallyMember</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@СумКорПланПозВалДолСША != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_10_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Valyuta_Inf_baz_akt_svop_dogValyutaAxis">mem-int:Dollar_SSHAMember</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
				<xsl:if test="@СумКорПланПозВалЕвро != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel1_11_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Valyuta_Inf_baz_akt_svop_dogValyutaAxis">mem-int:EvroMember</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
			</xsl:for-each>
			<xsl:for-each select="//report_0409725:Ф0409725_Раздел2/report_0409725:Ф0409725_Раздел2_Данные/report_0409725:Ф0409725_Раздел2_Строка">
				<xsl:call-template name="context_add">
					<xsl:with-param name="context_id">
						<xsl:text>context_razdel2_</xsl:text>
						<xsl:value-of select="position()"/>
					</xsl:with-param>
					<xsl:with-param name="period_type"
					                select="'instant'"/>
					<xsl:with-param name="explicit_dimensions">
						<item dimension="dim-int:Uroven_riskaAxis">
							<xsl:choose>
								<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
								<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
								<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
							</xsl:choose>
						</item>
						<item dimension="dim-int:Tip_i_status_klientaAxis">
							<xsl:choose>
								<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
								<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
							</xsl:choose>
						</item>
						<item dimension="dim-int:Rezident_nerezidentAxis">
							<xsl:choose>
								<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
								<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
							</xsl:choose>
						</item>
					</xsl:with-param>
					<xsl:with-param name="typed_dimensions">
						<item dimension="dim-int:Data_Torg_den_Taxis">
							<dim-int:Data_Torg_denTypedname>
								<xsl:value-of select="@ДатаТоргДеньОтчПер"/>
							</dim-int:Data_Torg_denTypedname>
						</item>
					</xsl:with-param>
				</xsl:call-template>
			</xsl:for-each>
			<xsl:for-each select="//report_0409725:Ф0409725_Раздел3/report_0409725:Ф0409725_Раздел3_Данные/report_0409725:Ф0409725_Раздел3_Строка">
				<xsl:if test="@ISIN != '' or @РегНомИдентНомВып != '' or @СумКорПланПоз != ''">
					<xsl:call-template name="context_add">
						<xsl:with-param name="context_id">
							<xsl:text>context_razdel3_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:with-param>
						<xsl:with-param name="period_type"
						                select="'instant'"/>
						<xsl:with-param name="explicit_dimensions">
							<item dimension="dim-int:Uroven_riskaAxis">
								<xsl:choose>
									<xsl:when test="@Уровень_Риска = 'Стандартный'">mem-int:StandartMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Повышенный'">mem-int:PovyshMember</xsl:when>
									<xsl:when test="@Уровень_Риска = 'Особый'">mem-int:OsobMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Tip_i_status_klientaAxis">
								<xsl:choose>
									<xsl:when test="@Тип_Клиента = 'ФЛ'">mem-int:FLMember</xsl:when>
									<xsl:when test="@Тип_Клиента = 'ЮЛ'">mem-int:YULMember</xsl:when>
								</xsl:choose>
							</item>
							<item dimension="dim-int:Rezident_nerezidentAxis">
								<xsl:choose>
									<xsl:when test="@Резидентность = 'Резидент'">mem-int:RezidentMember</xsl:when>
									<xsl:when test="@Резидентность = 'Нерезидент'">mem-int:NerezidentMember</xsl:when>
								</xsl:choose>
							</item>
						</xsl:with-param>
						<xsl:with-param name="typed_dimensions">
							<item dimension="dim-int:ID_CzennojBumagiTaxis">
								<dim-int:ID_CzennojBumagi_TypedName>
									<xsl:value-of select="@ИДЦенБум"/>
								</dim-int:ID_CzennojBumagi_TypedName>
							</item>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
			</xsl:for-each>
			<xsl:if test="count(//report_0409725:Ф0409725_Раздел1/*/@КолКлиенНепокрПоз) &gt; 0 or count(//report_0409725:Ф0409725_Раздел1/*/@КолКлиенНепокрПозПозСделКор) &gt; 0 or count(//report_0409725:Ф0409725_Раздел1/*/@КолКлиенНепокрПозПозСделДлин) &gt; 0 or count(//report_0409725:Ф0409725_Раздел2/report_0409725:Ф0409725_Раздел2_Данные/report_0409725:Ф0409725_Раздел2_Строка/@КолКлиентОтрНПР2) &gt; 0">
				<xsl:call-template name="unit_add">
					<xsl:with-param name="unit_id"
					                select="'PURE'"/>
					<xsl:with-param name="measure"
					                select="'xbrli:pure'"/>
				</xsl:call-template>
			</xsl:if>
			<xsl:if test="count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначПланПозКлиент) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначОтрПланПозКлиент) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначОтрПланПозКлиентНомВал) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначОтрПланПозКлиентДрагМет) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначНепокрПозПозСделКорВалРФЭквРуб) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначНепокрПозПозСделКорВалРФЭквВал) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначНепокрПозПозСделКорВалРФЭквДрагМет) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначНепокрПозПозСделДлинВалРФЭквРуб) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначНепокрПозПозСделДлинВалРФЭквВал) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумЗначНепокрПозПозСделДлинВалРФЭквДрагМет) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумНедостСредИспНПР1) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумКорПланПозВалДолСША) &gt; 0 or  count(//report_0409725:Ф0409725_Раздел1/*/@СумКорПланПозВалЕвро) &gt; 0 or count(//report_0409725:Ф0409725_Раздел3/report_0409725:Ф0409725_Раздел3_Данные/report_0409725:Ф0409725_Раздел3_Строка/@СумКорПланПоз) &gt; 0">
				<xsl:call-template name="unit_add">
					<xsl:with-param name="unit_id"
					                select="'RUB'"/>
					<xsl:with-param name="measure"
					                select="'iso4217:RUB'"/>
				</xsl:call-template>
			</xsl:if>
			<xsl:for-each select="//report_0409725:Ф0409725_Раздел1/*">
				<xsl:if test="@КолКлиенНепокрПоз != ''">
					<ko-dic:Kol_nepokr_poz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_1_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>PURE</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>0</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@КолКлиенНепокрПоз"/>
					</ko-dic:Kol_nepokr_poz>
				</xsl:if>
				<xsl:if test="@СумЗначПланПозКлиент != ''">
					<ko-dic:Summ_plan_poz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_1_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначПланПозКлиент"/>
					</ko-dic:Summ_plan_poz>
				</xsl:if>
				<xsl:if test="@СумЗначОтрПланПозКлиент != ''">
					<ko-dic:Summ_otricz_plan_poz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_1_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначОтрПланПозКлиент"/>
					</ko-dic:Summ_otricz_plan_poz>
				</xsl:if>
				<xsl:if test="@СумЗначОтрПланПозКлиентНомВал != ''">
					<ko-dic:Summ_otricz_plan_pozNomInVal>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_1_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначОтрПланПозКлиентНомВал"/>
					</ko-dic:Summ_otricz_plan_pozNomInVal>
				</xsl:if>
				<xsl:if test="@СумЗначОтрПланПозКлиентДрагМет != ''">
					<ko-dic:Summ_otricz_plan_pozDragMet>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_1_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначОтрПланПозКлиентДрагМет"/>
					</ko-dic:Summ_otricz_plan_pozDragMet>
				</xsl:if>
				<xsl:if test="@СумНедостСредИспНПР1 != ''">
					<ko-dic:NedostSrNorm>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_1_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумНедостСредИспНПР1"/>
					</ko-dic:NedostSrNorm>
				</xsl:if>
				<xsl:if test="@КолКлиенНепокрПозПозСделКор != ''">
					<ko-dic:Kol_nepokr_poz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_2_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>PURE</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>0</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@КолКлиенНепокрПозПозСделКор"/>
					</ko-dic:Kol_nepokr_poz>
				</xsl:if>
				<xsl:if test="@КолКлиенНепокрПозПозСделДлин != ''">
					<ko-dic:Kol_nepokr_poz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_3_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>PURE</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>0</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@КолКлиенНепокрПозПозСделДлин"/>
					</ko-dic:Kol_nepokr_poz>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделКорВалРФЭквРуб != ''">
					<ko-dic:SumNepokPoz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_4_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначНепокрПозПозСделКорВалРФЭквРуб"/>
					</ko-dic:SumNepokPoz>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделКорВалРФЭквВал != ''">
					<ko-dic:SumNepokPoz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_5_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначНепокрПозПозСделКорВалРФЭквВал"/>
					</ko-dic:SumNepokPoz>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделКорВалРФЭквДрагМет != ''">
					<ko-dic:SumNepokPoz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_6_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначНепокрПозПозСделКорВалРФЭквДрагМет"/>
					</ko-dic:SumNepokPoz>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделДлинВалРФЭквРуб != ''">
					<ko-dic:SumNepokPoz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_7_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначНепокрПозПозСделДлинВалРФЭквРуб"/>
					</ko-dic:SumNepokPoz>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделДлинВалРФЭквВал != ''">
					<ko-dic:SumNepokPoz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_8_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначНепокрПозПозСделДлинВалРФЭквВал"/>
					</ko-dic:SumNepokPoz>
				</xsl:if>
				<xsl:if test="@СумЗначНепокрПозПозСделДлинВалРФЭквДрагМет != ''">
					<ko-dic:SumNepokPoz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_9_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумЗначНепокрПозПозСделДлинВалРФЭквДрагМет"/>
					</ko-dic:SumNepokPoz>
				</xsl:if>
				<xsl:if test="@СумКорПланПозВалДолСША != ''">
					<ko-dic:SumKorPlanPoz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_10_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумКорПланПозВалДолСША"/>
					</ko-dic:SumKorPlanPoz>
				</xsl:if>
				<xsl:if test="@СумКорПланПозВалЕвро != ''">
					<ko-dic:SumKorPlanPoz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel1_11_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумКорПланПозВалЕвро"/>
					</ko-dic:SumKorPlanPoz>
				</xsl:if>
			</xsl:for-each>
			<xsl:for-each select="//report_0409725:Ф0409725_Раздел2/report_0409725:Ф0409725_Раздел2_Данные/report_0409725:Ф0409725_Раздел2_Строка">
				<xsl:if test="@КолКлиентОтрНПР2 != ''">
					<ko-dic:Kol_OtrNPR_poz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel2_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>PURE</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>0</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@КолКлиентОтрНПР2"/>
					</ko-dic:Kol_OtrNPR_poz>
				</xsl:if>
			</xsl:for-each>
			<xsl:for-each select="//report_0409725:Ф0409725_Раздел3/report_0409725:Ф0409725_Раздел3_Данные/report_0409725:Ф0409725_Раздел3_Строка">
				<xsl:if test="@ISIN != ''">
					<nfo-dic:ISIN>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel3_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:value-of select="@ISIN"/>
					</nfo-dic:ISIN>
				</xsl:if>
				<xsl:if test="@РегНомИдентНомВып != ''">
					<nfo-dic:GosRegNomerVyp>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel3_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:value-of select="@РегНомИдентНомВып"/>
					</nfo-dic:GosRegNomerVyp>
				</xsl:if>
				<xsl:if test="@СумКорПланПоз != ''">
					<ko-dic:SumKorPlanPoz>
						<xsl:attribute name="contextRef">
							<xsl:text>context_razdel3_</xsl:text>
							<xsl:value-of select="position()"/>
						</xsl:attribute>
						<xsl:attribute name="unitRef">
							<xsl:text>RUB</xsl:text>
						</xsl:attribute>
						<xsl:attribute name="decimals">
							<xsl:text>2</xsl:text>
						</xsl:attribute>
						<xsl:value-of select="@СумКорПланПоз"/>
					</ko-dic:SumKorPlanPoz>
				</xsl:if>				
			</xsl:for-each>			
		</xbrli:xbrl>
	</xsl:template>
</xsl:stylesheet>