#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_meuble_stock():
    mycursor = get_db().cursor()
    sql = '''
    
           '''
    # mycursor.execute(sql)
    # datas_show = mycursor.fetchall()
    # labels = [str(row['libelle']) for row in datas_show]
    # values = [int(row['nbr_meubles']) for row in datas_show]

    # sql = '''
    #         
    #        '''
    datas_show=[]
    labels=[]
    values=[]
    sql = '''
        SELECT COUNT(DISTINCT commande_id) as nb_commandes,
        SUM(quantite_lc) as nb_meuble,
        SUM(quantite_lc * prix_lc) AS total,
        LEFT(code_postal_fact,2) as dep,
        SUM(quantite_lc * prix_lc) / SUM(quantite_lc) as prix_moyen_meuble,
        SUM(quantite_lc) / COUNT(DISTINCT commande_id) as nb_meuble_moyen,
        SUM(quantite_lc * prix_lc) / COUNT(DISTINCT commande_id) as panier_moyen
        FROM v_ligne_commande vlc
        JOIN v_commande vc ON vlc.commande_id = vc.id_commande
        JOIN utilisateur u ON vlc.utilisateur_id = u.id_utilisateur
        GROUP BY dep
        ;
        '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['dep']) for row in datas_show]
    values = [int(row['panier_moyen']) for row in datas_show]
    values2 = [int(row['total']) for row in datas_show]
    
    sql = '''
    SELECT commande_id,
    SUM(quantite_lc) as nb_meuble,
    SUM(quantite_lc * prix_lc) AS total
    FROM v_ligne_commande vlc
    JOIN v_commande vc ON vlc.commande_id = vc.id_commande
    GROUP BY commande_id
    ;
    '''
    mycursor.execute(sql)
    datas_show2 = mycursor.fetchall()
    labels2 = [str(row['commande_id']) for row in datas_show2]
    
    values3 = ""
    for row in datas_show2:
        if values3 == "":
            values3 = ("{x: "+str(row['total']+1)+", y: "+str(row['nb_meuble'])+"},")
        else:
            values3 = values3 + ("{x: "+str(row['total']+1)+", y: "+str(row['nb_meuble'])+"},")
    values3 = values3[:-1]
    values3 = "["+values3+"]"
    
    print("datas_show = " + str(datas_show))
    print("labels = " + str(labels))
    print("values = " + str(values))
    print("values2 = " + str(values2))
    print("datas_show2 = " + str(datas_show2))
    print("labels2 = " + str(labels2))
    print("values3 = " + str(values3))
   

    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values
                           , values2=values2
                           , datas_show2=datas_show2
                           , labels2=labels2
                           , values3=values3)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    mycursor = get_db().cursor()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    sql = '''
    SELECT LEFT(code_postal,2) as dep, COUNT(code_postal) AS nbr_dept
    FROM adresse
    GROUP BY dep
    '''
    mycursor.execute(sql)
    adresses = mycursor.fetchall()

    # recherche de la valeur maxi "nombre" dans les départements
    maxAddress = 0
    
    for element in adresses:
        if element['nbr_dept'] > maxAddress:
            maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    if maxAddress != 0:
        for element in adresses:
            indice = element['nbr_dept'] / maxAddress
            element['indice'] = round(indice,2)

    print(maxAddress)
    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


