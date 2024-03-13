#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/meuble/commentaires', methods=['GET'])
def admin_meuble_details():
    mycursor = get_db().cursor()
    id_meuble =  request.args.get('id_meuble', None)
    sql = '''    requête admin_type_meuble_1    '''
    commentaires = {}
    sql = '''   requête admin_type_meuble_1_bis   '''
    meuble = []
    return render_template('admin/meuble/show_meuble_commentaires.html'
                           , commentaires=commentaires
                           , meuble=meuble
                           )

@admin_commentaire.route('/admin/meuble/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_meuble = request.form.get('id_meuble', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''    requête admin_type_meuble_2   '''
    tuple_delete=(id_utilisateur,id_meuble,date_publication)
    get_db().commit()
    return redirect('/admin/meuble/commentaires?id_meuble='+id_meuble)


@admin_commentaire.route('/admin/meuble/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_meuble = request.args.get('id_meuble', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/meuble/add_commentaire.html',id_utilisateur=id_utilisateur,id_meuble=id_meuble,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_meuble = request.form.get('id_meuble', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_meuble_3   '''
    get_db().commit()
    return redirect('/admin/meuble/commentaires?id_meuble='+id_meuble)


@admin_commentaire.route('/admin/meuble/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_meuble = request.args.get('id_meuble', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_type_meuble_4   '''
    get_db().commit()
    return redirect('/admin/meuble/commentaires?id_meuble='+id_meuble)