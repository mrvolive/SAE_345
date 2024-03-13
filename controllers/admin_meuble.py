#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_meuble = Blueprint('admin_meuble', __name__,
                          template_folder='templates')


@admin_meuble.route('/admin/meuble/show')
def show_meuble():
    mycursor = get_db().cursor()
    sql = '''  SELECT *,stock FROM meuble
    INNER JOIN declinaison_meuble 
    WHERE meuble.id_meuble = declinaison_meuble.meuble_id
    '''
    mycursor.execute(sql)
    meubles = mycursor.fetchall()
    sql = '''SELECT meuble.id_meuble, COUNT(declinaison_meuble.meuble_id) AS nb_declinaisons
    FROM meuble 
    LEFT JOIN declinaison_meuble ON meuble.id_meuble = declinaison_meuble.meuble_id
    GROUP BY meuble.id_meuble;
'''
    mycursor.execute(sql)
    nb_declinaisons = mycursor.fetchall()
    print("aa",meubles)
    print(5,nb_declinaisons)
    return render_template('admin/meuble/show_meuble.html', meubles=meubles, nb_declinaisons=nb_declinaisons)


@admin_meuble.route('/admin/meuble/add', methods=['GET'])
def add_meuble():
    mycursor = get_db().cursor()

    return render_template('admin/meuble/add_meuble.html'
                           #,types_meuble=type_meuble,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_meuble.route('/admin/meuble/add', methods=['POST'])
def valid_add_meuble():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_meuble_id = request.form.get('type_meuble_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_meuble_2 '''

    tuple_add = (nom, filename, prix, type_meuble_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'meuble ajouté , nom: ', nom, ' - type_meuble:', type_meuble_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'meuble ajouté , nom:' + nom + '- type_meuble:' + type_meuble_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/meuble/show')


@admin_meuble.route('/admin/meuble/delete', methods=['GET'])
def delete_meuble():
    id_meuble=request.args.get('id_meuble')
    mycursor = get_db().cursor()
    sql = ''' requête admin_meuble_3 '''
    mycursor.execute(sql, id_meuble)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet meuble : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_meuble_4 '''
        mycursor.execute(sql, id_meuble)
        meuble = mycursor.fetchone()
        print(meuble)
        image = meuble['image']

        sql = ''' requête admin_meuble_5  '''
        mycursor.execute(sql, id_meuble)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un meuble supprimé, id :", id_meuble)
        message = u'un meuble supprimé, id : ' + id_meuble
        flash(message, 'alert-success')

    return redirect('/admin/meuble/show')


@admin_meuble.route('/admin/meuble/edit', methods=['GET'])
def edit_meuble():
    id_meuble=request.args.get('id_meuble')
    mycursor = get_db().cursor()
    sql = '''
    SELECT *,nom_meuble,image_meuble, prix_meuble AS prix, description_meuble AS description ,declinaison_meuble.stock
    FROM meuble 
    JOIN declinaison_meuble
    WHERE id_meuble = %s AND declinaison_meuble.meuble_id = meuble.id_meuble;  
    '''
    mycursor.execute(sql, id_meuble)
    meuble = mycursor.fetchone()
    print(meuble)
    sql = '''
    SELECT *, id_type_meuble, libelle_type_meuble AS libelle FROM type_meuble;  
    '''
    mycursor.execute(sql)
    types_meuble = mycursor.fetchall()
    print(types_meuble)

    # sql = '''
    # requête admin_meuble_6
    # '''
    # mycursor.execute(sql, id_meuble)
    # declinaisons_meuble = mycursor.fetchall()

    return render_template('admin/meuble/edit_meuble.html'
                           ,meuble=meuble
                           ,types_meuble=types_meuble
                         #  ,declinaisons_meuble=declinaisons_meuble
                           )


@admin_meuble.route('/admin/meuble/edit', methods=['POST'])
def valid_edit_meuble():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_meuble = request.form.get('id_meuble', '')
    image = request.files.get('image', '')
    type_meuble_id = request.form.get('type_meuble_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    stock = request.form.get('stock')
    sql_image = '''
        SELECT image_meuble
        FROM meuble 
        WHERE id_meuble = %s;
    '''
    mycursor.execute(sql_image, (id_meuble,))
    image_nom = mycursor.fetchone()
    if image_nom:
        image_nom = image_nom['image_meuble']
    if image:
        if image_nom and os.path.exists(os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
        image_nom = filename
    sql_update = '''  
        UPDATE meuble 
        SET nom_meuble = %s, image_meuble = %s, prix_meuble = %s, type_meuble_id = %s, stock_meuble = %s
        WHERE id_meuble = %s;
    '''
    mycursor.execute(sql_update, (nom, image_nom, prix, type_meuble_id, stock, id_meuble))
    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'Meuble modifié - Nom: ' + nom + ' - Type de meuble: ' + type_meuble_id + ' - Prix: ' + prix + ' - Image: ' + image_nom + ' - Description: ' + description + ' - Stock: ' + stock
    flash(message, 'alert-success')
    return redirect('/admin/meuble/show')


@admin_meuble.route('/admin/meuble/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    meuble=[]
    commentaires = {}
    return render_template('admin/meuble/show_avis.html'
                           , meuble=meuble
                           , commentaires=commentaires
                           )


@admin_meuble.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    meuble_id = request.form.get('idmeuble', None)
    userId = request.form.get('idUser', None)

    return admin_avis(meuble_id)
