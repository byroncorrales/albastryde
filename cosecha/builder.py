# -*- coding: utf-8 -*-
from datetime import date
from time import mktime
from cosecha.models import Cosecha
#from django.db import connection
from django.contrib.contenttypes.models import ContentType


content_type = ContentType.objects.get(app_label__exact='cosecha', name__exact='cosecha').id

def cosecha_builder(form_data,frequencies):
	# Recogiendo datos del formulario, mas es campo frecuencias, ya truducido a ingles
	departamentos = form_data['Departamento']
	municipios = form_data['Municipio']
	cosecha_variable = form_data['CosechaVariable']
	cosecha_producto = form_data['CosechaProducto']
	start_date = form_data['Desde']
	end_date = form_data['Hasta']



# juntar todos los municipios de cada uno de los departamentos seleccionados con la lista de muncipios selecionados directamente
	for departamento in departamentos:
		if len(departamento.municipios.all()) > 0:
			if len(municipios) > 0:
				municipios = municipios | departamento.municipios.all()
			else:
				municipios = departamento.municipios.all()

	pk_list=[]
	graphs=[]
	
	# Aqui se llama la funcion para hacer cada uno de los graficos
	for frequency in frequencies:
		for d in cosecha_variable:
			for e in municipios:
				for i in cosecha_producto:
					graph,pk_list=cosecha_graph(variable=d,municipio=e,producto=i,start_date=start_date,end_date=end_date,pk_list=pk_list)
					if not graph==None:
						graphs.append(graph)	
	return graphs,pk_list
# Esta es para traducir las fechas de los tiempos
def traducir_fecha(date):
	cosecha_tiempo={}
	if date.month < 3:
		cosecha_tiempo['ano']=date.year-1
		cosecha_tiempo['tiempo']=3
	elif date.month > 2 and date.month < 6:
		cosecha_tiempo['ano']=date.year
		cosecha_tiempo['tiempo']=1
	elif date.month > 5 and date.month < 9:
		cosecha_tiempo['ano']=date.year
		cosecha_tiempo['tiempo']=2
	elif date.month > 8:
		cosecha_tiempo['ano']=date.year
		cosecha_tiempo['tiempo']=3
	return cosecha_tiempo

def traducir_tiempo(ano,tiempo):
	if tiempo==1:
		return date(year=ano,month=3,day=1)
	elif tiempo==2:
		return date(year=ano,month=6,day=1)
	elif tiempo==3:
		return date(year=ano,month=9,day=1)
	return None
	
def cosecha_graph(variable,producto,municipio,start_date,end_date,pk_list):
	cosecha_start=traducir_fecha(start_date)
	cosecha_end=traducir_fecha(end_date)
	a= Cosecha.objects.filter(ano=cosecha_start['ano']).filter(tiempo__gt= cosecha_start['tiempo']-1)
	b= Cosecha.objects.filter(ano__gt=cosecha_start['ano']).filter(ano__lt=cosecha_end['ano'])
	c= Cosecha.objects.filter(ano=cosecha_end['ano']).filter(tiempo__lt=cosecha_end['tiempo']+1)
	d= a | b| c
	queryset=d.filter(producto=producto).filter(municipio=municipio)
	if len(queryset)==0:
		return None,pk_list
	data=[]
	list_of_pk=[]
	for i in queryset:
		if variable=='area estimada':
			value=i.area_estimada
			unit= 'mz'
		elif variable=='producto estimado':
			value=i.producto_estimado
			unit='qq'
		elif variable=='area sembrada':
			value=i.area_sembrada
			unit='mz'
		elif variable=='area cosechada':
			value=i.area_cosechada
			unit='mz'
		elif variable=='producto obtenido':
			value=i.producto_obtenido
			unit='qq'
		elif variable=='rendimiento estimado':
			value=i.rendimiento_estimado()
			unit='qq/mz'
		elif variable=='rendimiento obtenido':
			value=i.rendimiento_obtenido()
			unit='qq/mz'
		elif variable=='area perdida':
			value=i.area_perdida()
			unit='mz'
		elif variable=='area miscalculada':
			value=i.area_miscalculada()
			unit='mz'
		elif variable=='producto miscalculado':
			value=i.producto_miscalculado()
			unit='qq'
		else:
			value=0
			unit=""
		fecha=int(mktime(traducir_tiempo(ano=i.ano,tiempo=i.tiempo).timetuple()))
		if i.tiempo==3:
			to_tiempo=1
			to_ano=i.ano+1
		else:
			to_tiempo=i.tiempo+1
			to_ano=i.ano
		to_fecha=int(mktime(traducir_tiempo(ano=to_ano,tiempo=to_tiempo).timetuple())-1)
		unique_pk=str(content_type)+"_"+str(i.pk)
		list_of_pk.append(str(i.pk))
#		data.append([fecha,value,unique_pk])
		data.append([[fecha,to_fecha],value,unique_pk])
	pk_list.append([content_type,list_of_pk])
	result = {'included_variables':{'municipio':municipio.nombre, 'cosecha_producto':producto.nombre, 'tipovariable':variable},'data':data,'source':'raw','unit':unit,'type':'cosecha '+variable,'frequency':'monthly','main_variable_js':'"'+variable+' de "+this.included_variables.cosecha_producto','place_js':'this.included_variables.municipio','normalize_factor_js':'this.start_value','display':'bars'}
	return result,pk_list

