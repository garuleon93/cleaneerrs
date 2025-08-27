from docxtpl import DocxTemplate
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from num2words import num2words
from docx2pdf import convert
import os
import win32com.client
import openpyxl
import math
import calendar
import win32com.client



class Generar_Docs:
    def __init__(self,listaDocs,listaWP,administrador,contratista,factura,facturas_contratisa):
        self.acta_entrega=listaDocs[0]
        self.informe_administrador=listaDocs[1]
        self.modelo_quipux=listaDocs[2]
        self.word=listaWP[0]
        self.pdf=listaWP[1]
        self.excel=listaWP[2]
        self.administrador=administrador
        self.contratista=contratista
        self.factura=factura
        self.facturas_contratisa=facturas_contratisa
        

    def obtener_fecha_fin_mes(self, mes, anio):
        # Diccionario para convertir el nombre del mes a su número correspondiente
        meses = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
            "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
            "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }

        # Convertir el año a entero
        try:
            anio = int(anio)
        except ValueError:
            return "Año inválido"

        # Obtener el número del mes
        numero_mes = meses.get(mes.capitalize())  # Capitaliza para evitar errores con minúsculas
        
        if not numero_mes:
            return "Mes inválido"

        # Obtener el último día del mes
        ultimo_dia = calendar.monthrange(anio, numero_mes)[1]

        # Formatear la fecha en "DD-MM-AAAA"
        return f"{ultimo_dia:02d}-{numero_mes:02d}-{anio}"


    def cifra_a_texto(self,monto):
        
        # Convertir monto a float si es una cadena
        monto = float(monto)
        
        # Obtener parte entera y decimal
        parte_entera, parte_decimal = f"{monto:.2f}".split(".")
        
        # Convertir parte entera a palabras
        parte_entera_texto = num2words(int(parte_entera), lang="es")

        # Formatear resultado
        resultado = f"{parte_entera_texto} con {parte_decimal}/100 dólares de los Estados Unidos de América"
        return resultado


    def fecha_a_texto(self,f,fecha):
        fecha_texto="DD-MM-AAAA"
        # Diccionario de meses en español
        meses = {
            "01": "enero", "02": "febrero", "03": "marzo", "04": "abril", "05": "mayo", "06": "junio",
            "07": "julio", "08": "agosto", "09": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"
        }

        # Convertir la fecha en un objeto datetime
        fecha_dt = datetime.strptime(fecha, "%d-%m-%Y")

        # Extraer día, mes y año
        dia = fecha_dt.day
        mes = meses[fecha_dt.strftime("%m")]  # Obtener el nombre del mes
        año = fecha_dt.year
        if f=="f1":
            fecha_texto=f"{dia:02} días del mes de {mes} de {año}"
        elif f=="f2":
            fecha_texto=f"{dia:02} de {mes} del {año}"
        # Retornar la fecha en el formato deseado
        return fecha_texto

    def obtener_planilla(self):
        # Diccionario de meses con su número correspondiente (hay que desarrollar para más meses el contrato, surgira el mes 13 Enero)
        meses = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
            "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }

        # Convertir la fecha de inicio a un objeto datetime
        fecha_dt = datetime.strptime(self.contratista[4], "%d-%m-%Y")
        
        # Obtener el mes de inicio del contrato
        mes_inicio = fecha_dt.month

        # Obtener el número del mes de pago
        mes_pago_num = meses.get(self.factura[4])
        print("FACTURA:")
        print(self.factura)
        print("mes pago:"+str(mes_pago_num))
        print("mes inicio :"+str(mes_inicio))
        
        numero_planilla = (mes_pago_num - mes_inicio + 12) % 12 + 1

        return f"{numero_planilla:02}"
    

    
    def generar_acta_entrega(self):
        docActaEntrega = DocxTemplate("aplicacion\plantillas\ACTA DE ENTREGA RECEPCIÓN PARCIAL.docx")
        contenido = {
            'monto_contrato_a_texto':self.cifra_a_texto(self.contratista[3]),
            'costo_mensual_a_texto':self.cifra_a_texto(self.factura[7]),
            'nro_planilla':self.obtener_planilla(),
            'administrador':self.administrador,
            'fecha_hoy': self.fecha_a_texto("f1",datetime.today().strftime('%d-%m-%Y')),
            'provincia':self.contratista[11],
            'localidades':self.contratista[10],
            'nro_factura':self.factura[2],
            'orden': self.contratista[1].replace('\n', '').strip(),
            'fecha': self.factura[3],
            'empresa': self.contratista[2].replace('\n', '').strip(),
            'mes_pago': self.factura[4],
            'anio_pago':self.factura[5],
            'monto_contrato': self.contratista[3],
            'costo_mensual': self.factura[7],
            'fecha_inicio': self.fecha_a_texto("f2",self.contratista[4]),
            'ruc': self.contratista[8].replace('\n', '').strip(),
            'ficha':self.contratista[12],
            'periodo_pago': f"del {int(self.factura[9]):02d} al {int(self.factura[10]):02d} de {self.factura[4]} del {self.factura[5]}",
        }
        docActaEntrega.render(contenido)
        return docActaEntrega
    
    def generar_informe_administrador(self):
        documento = DocxTemplate("aplicacion\plantillas\Informe adminsitrador.docx")
        contenido = {
            'monto_contrato_a_texto':self.cifra_a_texto(self.contratista[3]),
            'costo_mensual_a_texto':self.cifra_a_texto(self.contratista[9]),
            'nro_planilla':self.obtener_planilla(),
            'administrador':self.administrador,
            'fecha_hoy': self.fecha_a_texto("f2",datetime.today().strftime('%d-%m-%Y')),
            'localidades':self.contratista[10],
            'orden': self.contratista[1],
            'empresa': self.contratista[2],
            'mes_pago': self.factura[4],
            'anio_pago':self.factura[5],
            'monto_contrato': self.contratista[3],
            'costo_mensual': self.contratista[9],
            'fecha_inicio': self.fecha_a_texto("f2",self.contratista[4]),
            'ficha':self.contratista[12],
            'provincia':self.contratista[11],
        }
        documento.render(contenido)
        return documento
    
    def generar_modelo_quipux(self):
        documento = DocxTemplate("aplicacion\plantillas\Modelo Quipux.docx")
        contenido = {
            'costo_mensual_a_texto':self.cifra_a_texto(self.factura[7]),
            'administrador':self.administrador,
            'localidades':self.contratista[10],
            'orden': self.contratista[1],
            'empresa': self.contratista[2],
            'mes_pago': self.factura[4],
            'anio_pago':self.factura[5],
            'costo_mensual': self.factura[7],
            'provincia':self.contratista[11],
            
        }
        documento.render(contenido)
        return documento




    ####### FUNCIONES QUE ME SIRVEN PARA GENERAR EL EXCEL  
    # 
    # 
    # 
    #  

    def obtener_factura_anterior(self):
        """
        Busca la factura del mes anterior en la lista de facturas del contratista.
        
        :param facturas_contratista: Lista de facturas del contratista.
        :param factura_actual: La factura actual (objeto con índice 4 como mes y 5 como año).
        :return: La factura del mes anterior si existe, de lo contrario, None.
        """
        if len(self.facturas_contratisa) <= 1:
            return None  # No hay facturas anteriores
        
        # Obtener mes y año de la factura actual
        mes_actual = self.factura[4]
        año_actual = int(self.factura[5])

        # Diccionario de meses para convertir nombres a números
        meses = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
            "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
            "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }
        
        # Obtener el número del mes anterior
        mes_actual_num = meses.get(mes_actual)
        if not mes_actual_num:
            return None  # Mes inválido

        if mes_actual_num == 1:  # Si es enero, el mes anterior es diciembre del año anterior
            mes_anterior_num = 12
            año_anterior = año_actual - 1
        else:
            mes_anterior_num = mes_actual_num - 1
            año_anterior = año_actual

        # Convertir número de mes a nombre
        mes_anterior = next((nombre for nombre, num in meses.items() if num == mes_anterior_num), None)
        
        # Buscar la factura del mes anterior en la lista
        for fact in self.facturas_contratisa:
            if fact[4] == mes_anterior and int(fact[5]) == año_anterior:
                return fact  # Factura encontrada
        
        return None  # No se encontró una factura del mes anterior     

    def obtener_total_facturas_anteriores(self):
        """
        Suma los valores planillados (fact[7]) de todas las facturas anteriores a la factura actual.
        """
        total = 0.0
        mes_actual = self.factura[4]
        anio_actual = int(self.factura[5])

        meses = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
            "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }

        mes_actual_num = meses.get(mes_actual)

        for fact in self.facturas_contratisa:
            mes_fact_num = meses.get(fact[4])
            anio_fact = int(fact[5])

            if (anio_fact < anio_actual) or (anio_fact == anio_actual and mes_fact_num < mes_actual_num):
                total += fact[7]

        return total
    

    #----- Imprimir pdf de hoja de multas

    def exportar_hoja_multas_pdf(self, ruta_excel, nombre_pdf="Multas.pdf"):
        try:
            # Iniciar Excel
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False

            # Abrir archivo Excel
            wb = excel.Workbooks.Open(ruta_excel)

            # Verificar si la hoja "Multas" existe
            hoja_multas = None
            for hoja in wb.Sheets:
                if hoja.Name.strip().lower() == "multas":
                    hoja_multas = hoja
                    break

            if hoja_multas is None:
                raise ValueError("La hoja 'Multas' no existe en el archivo Excel.")

            # Seleccionar hoja y exportar
            hoja_multas.Select()
            ruta_pdf = os.path.normpath(os.path.splitext(ruta_excel)[0] + "Analisis de multas.pdf")

            print(f"Exportando a: {ruta_pdf}")
            hoja_multas.ExportAsFixedFormat(0, ruta_pdf)

            # Cerrar Excel correctamente
            wb.Close(SaveChanges=False)
            excel.Quit()

            print("✅ PDF generado exitosamente en:", ruta_pdf)

        except Exception as e:
            print("❌ Error al exportar hoja Multas a PDF:", e)
            try:
                excel.Quit()
            except:
                pass  # Por si ya está cerrado

    def generar_excel(self):
        print("generando excel")
        wb = openpyxl.load_workbook("aplicacion\plantillas\PlantilaPagoExcel.xlsx")
        
        #----------------------------------------------------------------------------
        #  HOJA PPAGO
        hojaPpago = wb["Ppago"]
        #-----------------------------------------------------------------------------
        

        #-----------------ENCABEZADO --------------------

        hojaPpago["C13"] = self.contratista[2]                      #empresa
        hojaPpago["C14"] = "$"+str(self.contratista[3])             #monto contrato
        hojaPpago["C15"] = "SERVICIO DE LIMPIEZA TIPO III, DE ACUERDO A LA ORDEN DE COMPRA "+self.contratista[1]            #Obra + orden de compra
        hojaPpago["C16"] = self.contratista[4]                      #fecha inicio
        hojaPpago["C17"] = self.contratista[5]                      #fecha fin


        hojaPpago["E13"] = "DAF-"+self.contratista[12]              #ficha contrato
        hojaPpago["E14"] = self.factura[2]                          #nro factura
        hojaPpago["E17"] = datetime.today().strftime("%d/%m/%Y")    #fecha informe
        
        hojaPpago["G10"] = self.obtener_planilla()                  #nro planilla
        hojaPpago["G11"] = datetime.today().strftime("%d/%m/%Y")    #fecha de hoy
        hojaPpago["G13"] = self.contratista[6]                      #fecha emision
        hojaPpago["G14"] = datetime.today().strftime("%d/%m/%Y")    #fecha fact

        #-----------------DESCRIPCION --------------------

        hojaPpago["B21"]="Planilla mensual "+self.factura[4]+" por limpieza de edificios"
        hojaPpago["E21"] = self.factura[7]                         #valor planillado                      
        hojaPpago["E31"] = self.factura[7]                          #HAY QUE SUMAR LAS LOCALIDADES 
        hojaPpago["G33"] = self.factura[7]                        #total planillado
        hojaPpago["G34"] = math.trunc((self.factura[7]*0.15)*100)/100      #IVA
        hojaPpago["G35"]=math.trunc((float(hojaPpago["G33"].value)+float(hojaPpago["G34"].value))*100)/100          #Total factura

        #-----------------DESCUENTOS --------------------
        # --CAmbio esta linea de codigo--hojaPpago["F38"]=math.trunc((float(hojaPpago["E21"].value)*0.1)*100)/100
             
        try:
            anticipo_entregado = float(self.contratista[13])  # valor entregado como anticipo
            valor_contrato = float(self.contratista[3])       #monto del contrato
            valor_anticipo = float(self.contratista[13])
            if anticipo_entregado > 0 and valor_contrato > 0:
                porcentaje_anticipo = anticipo_entregado / valor_contrato
            else:
                porcentaje_anticipo = 0.0
        except (TypeError, ValueError):
            porcentaje_anticipo = 0.0
        hojaPpago["F38"] = math.trunc((float(hojaPpago["E21"].value) * porcentaje_anticipo) * 100) / 100                       #Anticipo 10%
        hojaPpago["F39"]=math.trunc((float(hojaPpago["G33"].value)*0.0275)*100)/100                    #Impuesto a la renta 2.75%
        hojaPpago["F40"]=math.trunc((float(hojaPpago["G34"].value)*0.7)*100)/100                      #Retencion al Iva 70%
        hojaPpago["F41"]=0.0  #Multas

        hojaPpago["G43"]=math.trunc((float(hojaPpago["F38"].value)+float(hojaPpago["F39"].value)+float(hojaPpago["F40"].value)+float(hojaPpago["F41"].value))*100)/100 #Total descuentos
        #Valor liquido
        hojaPpago["G47"]=math.trunc((float(hojaPpago["G35"].value)-float(hojaPpago["G43"].value))*100)/100
        #descripcion
        hojaPpago["B50"]="Son: "+ self.cifra_a_texto(math.trunc(float(hojaPpago["G47"].value)*100)/100)
        #observaciones
        hojaPpago["B53"]="Observaciones: Se adjunta documentación de soporte de factura No. "+self.factura[2]+" e informe de Fiscalización de fecha "+datetime.today().strftime("%d/%m/%Y")+" correspondiente a la planilla Nro. "+self.obtener_planilla()
        
        #----------------------------------------------------------------------------
              #  HOJA ESTADO
        hojaEstado = wb["Estado"]
        #-----------------------------------------------------------------------------
        
        #-----------------ENCABEZADO --------------------

        hojaEstado["G12"] = self.obtener_planilla()                 #nro planilla
        hojaEstado["G13"] = datetime.today().strftime("%d/%m/%Y")   #fecha hoy
        hojaEstado["C16"] = self.contratista[2]                     #contrato
        hojaEstado["E16"] = "DAF-"+self.contratista[12]             #ficha contrato
        hojaEstado["G16"] = self.contratista[6]                     #ficha contrato
        hojaEstado["C17"] = "SERVICIO DE LIMPIEZA TIPO III, DE ACUERDO A LA ORDEN DE COMPRA "+self.contratista[1]            #Obra + orden de compra
        hojaEstado["C19"] = "$"+str(self.contratista[3])             #monto contrato
        hojaEstado["C21"] = "$"+str(self.contratista[3])

        #-----------------Valor ejecutado hasta la fecha --------------------
        factura_anterior=self.obtener_factura_anterior()
        if factura_anterior==None:
            hojaEstado["F24"]=str(self.factura[7])              #valor ejecutado hasta la fecha
            hojaEstado["G24"]= str(math.trunc(float((self.factura[7]/self.contratista[3])*100)*100)/100)+"%"   #porcentaje
            hojaEstado["F25"]=math.trunc((0*100))/100                            #valor ejecutado en el estado anterior
            hojaEstado["G26"]=self.factura[7]              #valor de la presente planilla
            hojaEstado["G27"]=math.trunc((self.factura[7]*0.15)*100)/100   #iva 15%
            hojaEstado["G28"]=math.trunc((float(hojaPpago["G33"].value)+float(hojaPpago["G34"].value))*100)/100 #valor total
            hojaEstado["F31"]=hojaPpago["F38"].value   #retenido
            hojaEstado["F34"]=hojaPpago["F38"].value   #anticipo total
            hojaEstado["F35"]=hojaPpago["F39"].value   #impuesto a la renta
            hojaEstado["F36"]=hojaPpago["F40"].value    #retencion iva
            hojaEstado["F37"]=hojaPpago["F41"].value   #multas
            hojaEstado["G39"]=hojaPpago["G43"].value    #total retencones
            hojaEstado["G40"]=hojaPpago["G47"].value    #valor liquido
            #cuadro de devoluciones de anticipos
            # hojaEstado["F43"]= math.trunc((self.contratista[3]*0.1)*100)/100    #anticipo entregado
            hojaEstado["F43"]= self.contratista[13]                         #anticipo entregado
            hojaEstado["F44"]=hojaEstado["F31"].value                           #anticipos en la presente planilla
            hojaEstado["F45"]=math.trunc((0)*100)/100                           #anticipos en la planilla anterior
            hojaEstado["F46"]=hojaEstado["F44"].value                           #anticipo toal a la fecha
            hojaEstado["F48"]=hojaEstado["G40"].value                                 #saldo total a cancelar

        else:
    # Calcular suma de valores planillados anteriores a la factura actual
            
            hojaEstado["F24"]=self.factura[7]+self.obtener_total_facturas_anteriores()              #valor ejecutado hasta la fecha
            hojaEstado["G24"]= str(math.trunc(float((float(hojaEstado["F24"].value)/self.contratista[3])*100)*100)/100)+"%"   #porcentaje
            hojaEstado["F25"]=self.obtener_total_facturas_anteriores()         #valor ejecutado en el estado anterior
            hojaEstado["G26"]=self.factura[7]              #valor de la presente planilla
            hojaEstado["G27"]=math.trunc((self.factura[7]*0.15)*100)/100   #iva 15%
            hojaEstado["G28"]=math.trunc((float(hojaPpago["G33"].value)+float(hojaPpago["G34"].value))*100)/100 #valor total
            #amortizacion de anticipo
            hojaEstado["F31"]=math.trunc(float(hojaPpago["E21"].value) * porcentaje_anticipo * 100) / 100   #retenido
            hojaEstado["F34"]=hojaPpago["F38"].value   #anticipo total
            hojaEstado["F35"]=hojaPpago["F39"].value   #impuesto a la renta
            hojaEstado["F36"]=hojaPpago["F40"].value    #retencion iva
            hojaEstado["F37"]=hojaPpago["F41"].value   #multas
            hojaEstado["G39"]=hojaPpago["G43"].value    #total retencones
            hojaEstado["G40"]=hojaPpago["G47"].value    #valor liquido
            #cuadro de devoluciones danticipo_entregadoe anticipos
            # corregir porque los anticipos varian de uno a otro esto es urgente arreglar
            nro_planilla = int(self.obtener_planilla())  # transformar numero de planilla de str a floar
            valor_anticipo_mensual = float(hojaEstado["F31"].value)  #valor mensual amortizado en float para texto
            valor_amortizado = (nro_planilla - 1) * valor_anticipo_mensual #valor amortizado hasta la planilla anterior
            hojaEstado["F43"]=  anticipo_entregado #anticipo entregado
            hojaEstado["F44"]=hojaEstado["F31"].value                           #anticipos en la presente planilla
            hojaEstado["F45"]=math.trunc(valor_amortizado)                           #anticipos en la planilla anterior
            hojaEstado["F46"]=hojaEstado["F31"].value+hojaEstado["F45"].value                          #anticipo toal a la fecha
            hojaEstado["F48"]=hojaEstado["G40"].value                                 #saldo total a cancelar

#  HOJA MULTAS
        hojaMulta = wb["Multas"]
        #-----------------------------------------------------------------------------
        
        #-----------------ENCABEZADO --------------------

        hojaMulta["A8"] = "ANÁLISIS DE MULTAS PARA EL" \
        " SEERVICIO DE LIMPIEZA TIPO III, DE ACUERDO A LA ORDEN DE COMPRA: "+self.contratista[1]

        fecha_inicio_mes = f"01-{self.obtener_fecha_fin_mes(self.factura[4], self.factura[5])[3:]}"
        hojaMulta["C13"] = self.fecha_a_texto("f2", fecha_inicio_mes)
        #hojaMulta["C13"] = self.fecha_a_texto("f2",self.contratista[4])
        hojaMulta["C14"] = self.fecha_a_texto("f2",self.obtener_fecha_fin_mes(self.factura[4],self.factura[5]))
        hojaMulta["C15"] = self.fecha_a_texto("f2",self.obtener_fecha_fin_mes(self.factura[4],self.factura[5]))
        hojaMulta["C16"]=  str(self.factura[8])+" días"
        hojaMulta["A29"]=  self.administrador

         #----------------------------------------------------------------------------
        #hojas = wb._sheets
        #hojas.sort(key=lambda hoja: ["Ppago", "Estado", "Multas"].index(hoja.title))

        return wb

    def generar(self):
        valor=False
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal
        root.attributes('-topmost', True)  # Asegurar que esté al frente
        root.update()  # Refrescar la ventana antes de abrir el diálogo

        carpeta_seleccionada = filedialog.askdirectory(title="Selecciona una carpeta")

        if carpeta_seleccionada:
            if self.acta_entrega==True:
                docActaEntrega=self.generar_acta_entrega()
                ruta_word = os.path.join(carpeta_seleccionada, "Acta_Entrega.docx")

                if self.pdf==self.word==True:
                    docActaEntrega.save(ruta_word)
                    ruta_pdf = os.path.join(carpeta_seleccionada, "Acta_Entrega.pdf")
                    convert(ruta_word, ruta_pdf)
                    print("Word y Pdf generados")
                    
                elif self.pdf==False and self.word==True:
                    docActaEntrega.save(ruta_word)
                    print("Se genero solo el Word")
                elif self.pdf==True and self.word==False:
                    docActaEntrega.save(ruta_word)
                    ruta_pdf = os.path.join(carpeta_seleccionada, "Acta_Entrega.pdf")
                    convert(ruta_word, ruta_pdf)
                    os.remove(ruta_word)
                    print("Solo Pdf generados")
            

            if self.informe_administrador==True:
                docInformeAdministrador=self.generar_informe_administrador()
                ruta_word = os.path.join(carpeta_seleccionada, "Informe_Administrador.docx")

                if self.pdf==self.word==True:
                    docInformeAdministrador.save(ruta_word)
                    ruta_pdf = os.path.join(carpeta_seleccionada, "Informe_Administrador.pdf")
                    convert(ruta_word, ruta_pdf)
                    print("Word y Pdf generados")
                elif self.pdf==False and self.word==True:
                    docInformeAdministrador.save(ruta_word)
                    print("Se genero solo el Word")
                elif self.pdf==True and self.word==False:
                    docInformeAdministrador.save(ruta_word)
                    ruta_pdf = os.path.join(carpeta_seleccionada, "Informe_Administrador.pdf")
                    convert(ruta_word, ruta_pdf)
                    os.remove(ruta_word)
                    print("Solo Pdf generados")

            if self.modelo_quipux==True:
                
                docModeloQuipux=self.generar_modelo_quipux()
                ruta_word = os.path.join(carpeta_seleccionada, "Modelo_Quipux.docx")

                if self.pdf==self.word==True:
                    docModeloQuipux.save(ruta_word)
                    ruta_pdf = os.path.join(carpeta_seleccionada, "Modelo_Quipux.pdf")
                    convert(ruta_word, ruta_pdf)
                    print("Word y Pdf generados")
                elif self.pdf==False and self.word==True:
                    docModeloQuipux.save(ruta_word)
                    print("Se genero solo el Word")
                elif self.pdf==True and self.word==False:
                    docModeloQuipux.save(ruta_word)
                    ruta_pdf = os.path.join(carpeta_seleccionada, "Modelo_Quipux.pdf")
                    convert(ruta_word, ruta_pdf)
                    os.remove(ruta_word)
                    print("Solo Pdf generados")

            if self.excel==True:
                docExcelPago=self.generar_excel()
                ruta_guardado = os.path.join(carpeta_seleccionada, "resultado.xlsx")
                docExcelPago.save(ruta_guardado)
                # Solo si también se quiere PDF
                if self.pdf == True:
                    self.exportar_hoja_multas_pdf(ruta_guardado)
            valor=True
        return valor



                
        

