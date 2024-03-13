#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_meuble = Blueprint('client_meuble', __name__,
                          template_folder='templates')


@client_meuble.route('/client/index')
@client_meuble.route('/client/meuble/show')  # remplace /client
def client_meuble_show():  # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT *
    FROM v_declinaison_meuble'''
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "
    if 'filter_word' in session:
        sql = sql + " nom_meuble Like %s "
        recherche = "%" + session['filter_word'] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if 'filter_prix_min' in session or 'filter_prix_max' in session:
        sql = sql + condition_and + 'prix_declinaison BETWEEN %s AND %s'
        list_param.append(session['filter_prix_min'])
        list_param.append(session['filter_prix_max'])
        condition_and = " AND "
    if 'filter_types' in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + "type_meuble_id=%s"
            if item != last_item:
                sql = sql + " OR "
            list_param.append(item)
        sql = sql + ")"
    tuple_sql = tuple(list_param)
    print(tuple_sql)
    mycursor.execute(sql, tuple_sql)
    meubles = mycursor.fetchall()

    # pour le filtre
    sql = '''SELECT * FROM type_meuble'''
    mycursor.execute(sql)
    types_meuble = mycursor.fetchall()

    sql = '''
    SELECT m.nom_meuble AS nom, dm.prix_declinaison AS prix, dm.stock as stock, l.quantite_lp AS quantite, dm.id_declinaison_meuble
    FROM declinaison_meuble as dm
    JOIN meuble AS m ON dm.meuble_id = m.id_meuble
    JOIN ligne_panier AS l ON dm.id_declinaison_meuble = l.declinaison_meuble_id
    WHERE l.utilisateur_id = %s
    '''

    mycursor.execute(sql, id_client)
    meubles_panier = mycursor.fetchall()

    prix_total = None
    if len(meubles_panier) >= 1:
        sql = '''
        SELECT SUM(dm.prix_declinaison * l.quantite_lp) AS prix_total
        FROM ligne_panier AS l
        JOIN declinaison_meuble AS dm ON l.declinaison_meuble_id = dm.id_declinaison_meuble
        JOIN meuble AS m ON dm.meuble_id = m.id_meuble
        WHERE utilisateur_id = %s
        '''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()['prix_total']

    # TODO : FAUT FAIRE LA
    print(meubles_panier)

    return render_template('client/boutique/panier_meuble.html'
                           , meubles=meubles
                           , types_meuble=types_meuble
                           , meubles_panier=meubles_panier
                           , prix_total=prix_total
                           , items_filtre=types_meuble
                           )
