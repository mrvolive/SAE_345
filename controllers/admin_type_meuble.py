#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_meuble = Blueprint('admin_type_meuble', __name__,
                        template_folder='templates')

@admin_type_meuble.route('/admin/type-meuble/show')
def show_type_meuble():
    mycursor = get_db().cursor()
    # sql = '''         '''
    # mycursor.execute(sql)
    # types_meuble = mycursor.fetchall()
    types_meuble=[]
    return render_template('admin/type_meuble/show_type_meuble.html', types_meuble=types_meuble)

@admin_type_meuble.route('/admin/type-meuble/add', methods=['GET'])
def add_type_meuble():
    return render_template('admin/type_meuble/add_type_meuble.html')

@admin_type_meuble.route('/admin/type-meuble/add', methods=['POST'])
def valid_add_type_meuble():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    mycursor = get_db().cursor()
    sql = '''         '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-meuble/show') #url_for('show_type_meuble')

@admin_type_meuble.route('/admin/type-meuble/delete', methods=['GET'])
def delete_type_meuble():
    id_type_meuble = request.args.get('id_type_meuble', '')
    mycursor = get_db().cursor()

    flash(u'suppression type meuble , id : ' + id_type_meuble, 'alert-success')
    return redirect('/admin/type-meuble/show')

@admin_type_meuble.route('/admin/type-meuble/edit', methods=['GET'])
def edit_type_meuble():
    id_type_meuble = request.args.get('id_type_meuble', '')
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, (id_type_meuble,))
    type_meuble = mycursor.fetchone()
    return render_template('admin/type_meuble/edit_type_meuble.html', type_meuble=type_meuble)

@admin_type_meuble.route('/admin/type-meuble/edit', methods=['POST'])
def valid_edit_type_meuble():
    libelle = request.form['libelle']
    id_type_meuble = request.form.get('id_type_meuble', '')
    tuple_update = (libelle, id_type_meuble)
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type meuble modifié, id: ' + id_type_meuble + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-meuble/show')








