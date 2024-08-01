# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd

st.write("Dashboard FisioClinics")
uploaded_file = st.file_uploader(
    "Introduce el excel con el diario económico", accept_multiple_files=False)

#options = st.multiselect("Mes", [1,2,3,4,5,6,7,8,9,10,11,12])   





def mes(csv,mes):
    datos = csv[pd.to_datetime(df['Fecha']).dt.month == mes]    
    deudas = datos.loc[df['Movimiento'] == "Deuda"]
    debes = deudas['Debe'].sum()
    abonos = datos.loc[df['Movimiento'] == "Abono"]
    pagos = abonos['Haber'].sum()
    metodos = abonos.drop_duplicates(subset=['Método de pago'])
    l_metodos = metodos['Método de pago'].to_list()
    m_pagos = {}
    for i in l_metodos:
        m_pago = abonos[abonos['Método de pago'] == i]
        m_pag_l = m_pago.shape[0]
        m_pago_total = m_pago['Haber'].sum()
        m_pagos[i] = [m_pag_l,m_pago_total]
    pacientes = deudas.drop_duplicates(subset=['Nombre de usuario'])
    n_pacientes = pacientes.shape[0]
    l_pacientes = pacientes['Nombre de usuario'].to_list()
    sesiones = []
    ingresos_medios = []
    deudores = {}
    for i in l_pacientes:
        pac = deudas[deudas['Nombre de usuario'] == i]
        sesion = pac.shape[0]
        sesiones.append(sesion)
        ingresos = pac['Debe'].sum()
        pac_deb = abonos[abonos['Nombre de usuario'] == i]
        debts = pac_deb['Haber'].sum()
        if ingresos + debts <= -1:
            deudores[i] = ingresos + debts
        ingresos_medios.append(ingresos)
    
    media_sesiones = sum(sesiones)/len(sesiones)
    media_ingresos = sum(ingresos_medios)/len(ingresos_medios)
    
    return ({'datos':deudas,"debes":debes, 'abonos':pagos, 'nº pacientes':len(l_pacientes),"media sesiones":media_sesiones,"n sesiones":sum(sesiones), "€ medio paciente": -media_ingresos, 'metodo': m_pagos, 'deudores': deudores})

    
def mes_terapeuta(csv):
    terapeutas = csv.drop_duplicates(subset=['Especialista'])
    l_terapeutas =terapeutas['Especialista'].to_list()
    resultados = {}
    sesiones = []
    for i in l_terapeutas:
        sesiones_prof = {}
        terapeuta = csv[csv['Especialista'] == i]
        servicios = terapeuta.drop_duplicates(subset=['Concepto'])
        l_servicios = servicios['Concepto'].to_list()
        for ii in l_servicios:
            servicio = terapeuta[terapeuta['Concepto'] == ii]
            sesiones = servicio.shape[0]
            debes = servicio['Debe'].sum()
            sesiones_prof[ii] = [sesiones,debes]
        sesiones = terapeuta.shape[0]
        debes = -(terapeuta['Debe'].sum())
        p_sesion = terapeuta['P. sesión'].sum()
        
        resultados[i] =[debes,sesiones,sesiones_prof,p_sesion]
        
    return (resultados)

        
def ingreso_servicio (csv):
    servicios = csv.drop_duplicates(subset=['Concepto'])
    l_servicios = servicios['Concepto'].to_list()
    resultados = {}
    for i in l_servicios:
        servicio = csv[csv['Concepto'] == i]
        sesiones = servicio.shape[0]
        debes = -(servicio['Debe'].sum())
        resultados[i] =[debes,sesiones]
        
    return (resultados)

def ocupación(csv,horas_prof):
    
        return()

try:
    df = pd.read_csv(uploaded_file)
    #df = pd.read_csv('C:/Users/cjove/Downloads/CSV.csv')
    df['Fecha']= pd.to_datetime(df['Fecha'],dayfirst=True)
    df = df.replace({'€':''}, regex=True)
    df["Debe"] = pd.to_numeric(df["Debe"])
    df["Haber"] = pd.to_numeric(df["Haber"])
    df["P. sesión"] = pd.to_numeric(df["P. sesión"])
        
    meses = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    resultados = {}
    for i in meses:
        try:
           x = mes(df,i)
           y = mes_terapeuta(x['datos'])
           z = ingreso_servicio(x['datos'])
           resultados[i] = [x,y,z]

       
        except:
            continue



    general = ['Haber','Debe','media sesiones', 'nº sesiones', 'nº pacientes', '€ medio paciente']
    general_data = []
    deudores_data = []
    metodo_data = []
    prof_data = []
    sesion_data = []
    servicio_data = []
    
    for i in resultados.keys():
        mes = resultados.get(i)
        datos_mes = mes[0]
        mes_t = mes[1]
        mes_s = mes[2]
        d_mes = [datos_mes.get('abonos'),datos_mes.get('debes'),datos_mes.get('media sesiones'),datos_mes.get('n sesiones'),datos_mes.get('nº pacientes'),datos_mes.get('€ medio paciente')]
        general_data.append(d_mes)
        df_deudores = pd.DataFrame.from_dict(datos_mes['deudores'], orient = 'index', columns = ['Importe'])
        df_deudores.insert(0, "Mes", [i]*df_deudores.shape[0], True)
        deudores_data.append(df_deudores)
        df_metodo = pd.DataFrame.from_dict(datos_mes['metodo'], orient = 'index', columns = ['Sesiones','Importe'])
        df_metodo.insert(0, "Mes", [i]*df_metodo.shape[0], True)
        metodo_data.append(df_metodo)
        df_servicio = pd.DataFrame.from_dict(mes_s, orient = 'index', columns = ['Importe', 'Nº Sesiones'])
        df_servicio.insert(0, "Mes", [i]*df_servicio.shape[0], True)
        servicio_data.append(df_servicio)
        
        for ii in mes_t.keys():
            prof = mes_t[ii]
            prof_data.append([i,ii,prof[0],prof[1],prof[3]])
            df_sesion = pd.DataFrame.from_dict(prof[2], orient = 'index', columns = ['sesiones','importe'])
            df_sesion.insert(0, "Mes", [i]*df_sesion.shape[0], True)
            df_sesion.insert(0, "Profesional", [ii]*df_sesion.shape[0], True)
            sesion_data.append(df_sesion)
            
            
    
    
    df_general = pd.DataFrame(general_data, index=resultados.keys(), columns = general)
    df_deudores = pd.concat(deudores_data, axis=0)
    df_deudores = df_deudores.reset_index()
    df_deudores = df_deudores.rename(columns={'index': 'Paciente'})
    df_metodo = pd.concat(metodo_data, axis=0)
    df_metodo = df_metodo.reset_index()
    df_metodo = df_metodo.rename(columns={'index': 'Método de pago'})
    df_prof = pd.DataFrame(prof_data, columns = ['Mes', 'Profesional', 'Importe', 'Sesiones', 'Importe (Precio Sesión)'])
    df_sesion =  pd.concat(sesion_data, axis=0)
    df_sesion = df_sesion.reset_index()
    df_sesion = df_sesion.rename(columns={'index': 'Sesión'})
    df_servicio = pd.concat(servicio_data, axis=0)
    df_servicio = df_servicio.reset_index()
    df_servicio = df_servicio.rename(columns={'index': 'Sesión'})
    
    st.write("Datos generales")
    st.dataframe(df_general)
    st.write("Deudores")
    st.dataframe(df_deudores)
    st.write("Métodos de pago")
    st.dataframe(df_metodo)
    st.write("Datos profesionales")
    st.dataframe(df_prof)
    st.write("Datos sesiones/profesionales")
    st.dataframe(df_sesion)
    st.write("Datos servicios")
    st.dataframe(df_servicio)

except:
    print('Introduce un archivo para mostrar datos')
