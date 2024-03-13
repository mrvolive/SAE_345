#! /usr/bin/python
# -*- coding:utf-8 -*-
import time

from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                          template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_meuble = request.form.get('id_declinaison_meuble')
    quantite = int(request.form.get('quantite'))
    # ---------
    # id_declinaison_meuble=request.form.get('id_declinaison_meuble',None)
    # id_declinaison_meuble = 1

    sql = """
        SELECT stock as quantite FROM declinaison_meuble
        where id_declinaison_meuble = %s
    """
    mycursor.execute(sql, id_declinaison_meuble)

    # check si la quantite est bonne
    if quantite >= 1 or quantite <= mycursor.fetchone()['quantite']:
        sql = """
            SELECT * FROM ligne_panier
            WHERE utilisateur_id = %s AND declinaison_meuble_id = %s
        """

        mycursor.execute(sql, (id_client, id_declinaison_meuble))
        ligne_panier = mycursor.fetchone()

        if ligne_panier is not None:
            sql = """
                UPDATE ligne_panier SET quantite_lp = quantite_lp + %s
                WHERE declinaison_meuble_id = %s AND utilisateur_id = %s
            """
            mycursor.execute(sql, (quantite, id_declinaison_meuble, id_client))
        else:
            sql = """
                INSERT INTO ligne_panier (declinaison_meuble_id, utilisateur_id, quantite_lp, date_ajout) 
                VALUES (%s, %s, %s, CURRENT_DATE)
            """

            mycursor.execute(sql, (id_declinaison_meuble, id_client, quantite))

        sql = """
            UPDATE declinaison_meuble SET stock = stock - %s WHERE id_declinaison_meuble = %s
        """

        mycursor.execute(sql, (quantite, id_declinaison_meuble))
    else:
        print("fraude dans la quantité demandé")
    # ajout dans le panier d'une déclinaison d'un meuble (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_declinaison_meuble))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_meuble = declinaisons[0]['id_declinaison_meuble']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_declinaison_meuble))
    #     meuble = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_meuble.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , meuble=meuble)
    # ajout dans le panier d'un meuble
    get_db().commit()
    return redirect('/client/meuble/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_meuble = request.form.get('id_declinaison_meuble', '')

    # ---------
    # partie 2 : on supprime une déclinaison de meuble
    # id_declinaison_meuble = request.form.get('id_declinaison_meuble', None)

    sql = '''
    SELECT * FROM ligne_panier
    WHERE declinaison_meuble_id = %s AND utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_declinaison_meuble, id_client))
    meuble_panier = mycursor.fetchone()

    quantite = meuble_panier['quantite_lp']

    if not (meuble_panier is None) and quantite > 1:
        sql = '''
        UPDATE ligne_panier SET quantite_lp = quantite_lp - 1
        WHERE declinaison_meuble_id = %s AND utilisateur_id = %s
        '''

        quantite = 1
    else:
        sql = '''
        DELETE FROM ligne_panier
        WHERE declinaison_meuble_id = %s AND utilisateur_id = %s
        '''

    mycursor.execute(sql, (id_declinaison_meuble, id_client))

    # mise à jour du stock de meuble disponible

    sql2 = '''UPDATE declinaison_meuble SET stock = stock + %s WHERE id_declinaison_meuble = %s '''
    mycursor.execute(sql2, (quantite, id_declinaison_meuble))

    get_db().commit()
    return redirect('/client/meuble/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, client_id)

    items_panier = mycursor.fetchall()
    for item in items_panier:
        meuble_id = item['declinaison_meuble_id']

        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND declinaison_meuble_id = %s'''
        mycursor.execute(sql, (client_id, meuble_id))

        sql2 = '''UPDATE declinaison_meuble SET stock = stock + %s WHERE id_declinaison_meuble = %s'''
        mycursor.execute(sql2, (item['quantite_lp'], meuble_id))

    get_db().commit()
    return redirect('/client/meuble/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_meuble = request.form.get('id_declinaison_meuble', '')
    data = (id_declinaison_meuble, id_client)

    # id_declinaison_meuble = request.form.get('id_declinaison_meuble')

    sql = '''
        SELECT quantite_lp FROM ligne_panier
        WHERE declinaison_meuble_id = %s AND utilisateur_id = %s
    '''

    mycursor.execute(sql, data)
    quantite = mycursor.fetchone()['quantite_lp']

    sql = '''
        DELETE FROM ligne_panier
        WHERE declinaison_meuble_id = %s AND utilisateur_id = %s
    '''

    mycursor.execute(sql, (id_declinaison_meuble, id_client))

    sql2 = '''UPDATE declinaison_meuble SET stock = stock + %s WHERE id_declinaison_meuble = %s '''
    mycursor.execute(sql2, (quantite, id_declinaison_meuble))

    get_db().commit()
    return redirect('/client/meuble/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables

    if filter_word or filter_word == '':
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash('Le mot doit être composé de lettres uniquement')
        else:
            if len(filter_word) == 1:
                flash('Le mot doit contenir au moins 2 lettres')
            else:
                session.pop('filter_word', None)

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash('Le prix minimum doit être inférieur au prix maximum')
        else:
            flash('Les prix doivent être des nombres entiers')
    if filter_types and filter_types != []:
        session['filter_types'] = filter_types

    print(session)
    return redirect('/client/meuble/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_types', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    print("suppr filtre")
    return redirect('/client/meuble/show')
