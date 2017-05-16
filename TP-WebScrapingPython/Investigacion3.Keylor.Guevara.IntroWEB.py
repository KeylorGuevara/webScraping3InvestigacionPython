# coding=utf-8
from urllib import *
import pymysql
from bs4 import BeautifulSoup
import re
import time

# Librerias que son necesarias
# Coneccion con la base de datos MySQL
c = pymysql.connect(host="webscraping2017.cwreudtoe38d.us-west-2.rds.amazonaws.com", user="masterUser",
                    db="webscraping2017", passwd="webscraping2017", use_unicode=True, charset="utf8")

########################################################################################################################
########################################################################################################################
############################################UNICIA WEB SCRAPING#########################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

n = 1
for i in range(100):
    url = "http://site.ebrary.com/lib/colecciones/search.action?p00=amor&sortBy=score&sortOrder=desc&viewType=detail" \
          "&page={0}".format(i)
    """Conexión inicial con la base de datos, para realizar primeramente el proceso de auditoria"""
    # CONExION CON LA BASE DE DATOS DESARROLLADA EN MYSQL
    paginaWeb= url
    fechaAuditoria=time.strftime("%x")
    numeroRegisto=n+13
    estado="Pendiente"
    error="No"
    try:
        with c.cursor() as cursor:
            sql = "INSERT INTO `auditoria` (`fecha`,`paginaWeb`,`numero_registro`,`estado`," \
                  "`error`) VALUES(%s,%s,%s,%s,%s) "
            cursor.execute(sql, [fechaAuditoria, paginaWeb, numeroRegisto, estado,
                                 error])
            c.commit()
    finally:
        pass

    html = urlopen(url)  # link de la pagina de la que tomaremos los datos
    bsObj = BeautifulSoup(html, "lxml")  # objeto de la clase bs4

    for child in bsObj.findAll("div", {"class": "book_item"}):  # para poder tomar la imagen del libro
        imagen = child.find("div", {"class": "book_cover"}).find("img", {"alt": "book cover"})
        listaDeInfo = child.find("div", {"class": "title_list_info"}).findAll("span", {"class": "label"})
        listaDeInfoString = child.find("div", {"class": "title_list_info"}).findAll(string=re.compile(":"))
        m = 0
        for valor in listaDeInfo:
            valorComparar = listaDeInfo[m].get_text()
            valordelString = listaDeInfoString[m]
            valordelString = valordelString.strip().lstrip()
            if 'documento' in valorComparar:
                identificacionDocumento = valordelString
            elif 'pISBN' in valorComparar:
                pISBN = valordelString
            elif 'eISBN' in valorComparar:
                eISBN = valordelString
            elif 'exclusivo' in valorComparar:
                precioExclusivo = valordelString
            elif 'Three' in valorComparar:
                threeUser = valordelString
            elif 'usuarios' in valorComparar:
                usuariosMultiples = valordelString

            m = m + 1

        titulo = child.find("div", {"class": "book_info_titlelist"}).find("a", {"class": "title"})  # TITULO_LIBRO
        nombreAutor = child.find("div", {"class": "book_info_titlelist"}).find("a", {
            "title": "Restringir la búsqueda a este Autor"})  # NOMBRE_AUTOR
        nombreEditorial = child.find("div", {"class": "book_info_titlelist"}).find("a", {
            "title": "Restringir la búsqueda a esta Editorial"})  # NOMBRE_EDITORIAL
        fechaPublicacion = child.find("div", {"class": "book_info_titlelist"}).find(
            string=re.compile("/"))# FECHA_PUBLICACION

        temaTratado = child.find("div", {"class": "book_info_titlelist"}).find("a", {
            "title": "Restringir la búsqueda a este Tema"})

        tituloString = titulo.get_text()
        nombreAutorSting = nombreAutor.get_text()
        nombreEditorialString = nombreEditorial.get_text()
        tipo= type(fechaPublicacion)
        if (str(tipo)== "<type 'NoneType'>"):
            print "Hola"
            fechaPublicacion="22/1996"
        fechaPublicacionSting = fechaPublicacion.encode('utf-8')
        temaTratadoString = temaTratado.get_text()
        identificacionDocumentoString = str(identificacionDocumento).lstrip(": ")
        pISBNString = str(pISBN).lstrip(": ")
        eISBNString = str(eISBN).lstrip(": ")
        precioExclusivoString2 = str(precioExclusivo)
        precioExclusivoString = " ".join(precioExclusivoString2.split()).lstrip(": ")
        threeUserString2 = str(threeUser)
        threeUserString = " ".join(threeUserString2.split()).lstrip(": ")
        usuariosMultiplesString2 = str(usuariosMultiples)
        usuariosMultiplesString = " ".join(usuariosMultiplesString2.split()).lstrip(": ")
        imagenString = str(imagen.get('src'))
        n = n + 1
        try:
            with c.cursor() as cursor:
                sql = "INSERT INTO `registros` (`titulo`,`nombreAutor`,`nombreEditorial`,`fechaPublicacion`," \
                      "`temaTratado`,`identificacionDocumento`,`pISBN`,`eISBN`,`precioExclusivo`,`threeUser`," \
                      "`multiplesUsuarios`,`imagenPortada`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                cursor.execute(sql, [
                    tituloString, nombreAutorSting, nombreEditorialString, fechaPublicacionSting, temaTratadoString,
                    identificacionDocumentoString, pISBNString, eISBNString, precioExclusivoString, threeUserString,
                    usuariosMultiplesString, imagenString])
            c.commit()
        finally:
            pass
        print (n, "------------------------------------------------------------------------------------------------")

    try:
        with c.cursor() as cursor:
            sql = "UPDATE `auditoria` SET `estado`='Finalizado' WHERE `paginaWeb`=%s;"
            cursor.execute(sql, [paginaWeb])
            c.commit()
    finally:
        pass
""""   print (titulo.get_text())
        print (nombreAutor.get_text())
        print (nombreEditorial.get_text())
        print (fechaPublicacion)
        print (temaTratado.get_text())
        print (identificacionDocumentoString)
        print (pISBNString)
        print (eISBNString)
        print (precioExclusivoString)
        print (threeUserString)
        print (usuariosMultiplesString)
        print imagenString
        print (n, "------------------------------------------------------------------------------------------------")"""


#CONECCION CON LA BASE DE DATOS DESARROLLADA EN MYSQL
