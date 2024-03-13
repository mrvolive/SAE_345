#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/meuble/details', methods=['GET'])
def client_meuble_details():
    mycursor = get_db().cursor()
    id_meuble =  request.args.get('id_meuble', None)
    id_client = session['id_user']

    ## partie 4
    # client_historique_add(id_meuble, id_client)

    sql = '''SELECT * FROM meuble 
    WHERE id_meuble = %s;'''
    mycursor.execute(sql, id_meuble)
    meuble = mycursor.fetchone()
    #meuble=[]
    commandes_meubles=[]
    nb_commentaires=[]
    if meuble is None:
        abort(404, "pb id meuble")
    # sql = '''
    #
    # '''
    # mycursor.execute(sql, ( id_meuble))
    # commentaires = mycursor.fetchall()
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_meuble))
    # commandes_meubles = mycursor.fetchone()
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_meuble))
    # note = mycursor.fetchone()
    # print('note',note)
    # if note:
    #     note=note['note']
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_meuble))
    # nb_commentaires = mycursor.fetchone()
    return render_template('client/meuble_info/meuble_details.html'
                           , meuble=meuble
                           # , commentaires=commentaires
                           , commandes_meubles=commandes_meubles
                           # , note=note
                            , nb_commentaires=nb_commentaires
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_meuble = request.form.get('id_meuble', None)
    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/meuble/details?id_meuble='+id_meuble)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/meuble/details?id_meuble='+id_meuble)

    tuple_insert = (commentaire, id_client, id_meuble)
    print(tuple_insert)
    sql = '''  '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/meuble/details?id_meuble='+id_meuble)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_meuble = request.form.get('id_meuble', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''   '''
    tuple_delete=(id_client,id_meuble,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/meuble/details?id_meuble='+id_meuble)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_meuble = request.form.get('id_meuble', None)
    tuple_insert = (note, id_client, id_meuble)
    print(tuple_insert)
    sql = '''   '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/meuble/details?id_meuble='+id_meuble)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_meuble = request.form.get('id_meuble', None)
    tuple_update = (note, id_client, id_meuble)
    print(tuple_update)
    sql = '''  '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/meuble/details?id_meuble='+id_meuble)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_meuble = request.form.get('id_meuble', None)
    tuple_delete = (id_client, id_meuble)
    print(tuple_delete)
    sql = '''  '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/meuble/details?id_meuble='+id_meuble)
