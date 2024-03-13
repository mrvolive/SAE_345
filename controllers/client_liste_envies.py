#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_liste_envies = Blueprint('client_liste_envies', __name__,
                        template_folder='templates')


@client_liste_envies.route('/client/envie/add', methods=['get'])
def client_liste_envies_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_meuble = request.args.get('id_meuble')
    return redirect('/client/meuble/show')

@client_liste_envies.route('/client/envie/delete', methods=['get'])
def client_liste_envies_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_meuble = request.args.get('id_meuble')
    return redirect('/client/envies/show')

@client_liste_envies.route('/client/envies/show', methods=['get'])
def client_liste_envies_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    meubles_liste_envies = []
    meubles_historique = []
    return render_template('client/liste_envies/liste_envies_show.html'
                           ,meubles_liste_envies=meubles_liste_envies
                           , meubles_historique=meubles_historique
                           #, nb_liste_envies= nb_liste_envies
                           )



def client_historique_add(meuble_id, client_id):
    mycursor = get_db().cursor()
    client_id = session['id_user']
    # rechercher si le meuble pour cet utilisateur est dans l'historique
    # si oui mettre
    sql ='''   '''
    mycursor.execute(sql, (meuble_id, client_id))
    historique_produit = mycursor.fetchall()
    sql ='''   '''
    mycursor.execute(sql, (client_id))
    historiques = mycursor.fetchall()


@client_liste_envies.route('/client/envies/up', methods=['get'])
@client_liste_envies.route('/client/envies/down', methods=['get'])
@client_liste_envies.route('/client/envies/last', methods=['get'])
@client_liste_envies.route('/client/envies/first', methods=['get'])
def client_liste_envies_meuble_move():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_meuble = request.args.get('id_meuble')
  
    return redirect('/client/envies/show')
