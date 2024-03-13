#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')


@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']  # FIXME variable inutilisé

    id_commande = request.args.get('id_commande', None)
    commande_adresses = None
    meubles_commande = None

    sql = '''
    SELECT commande.id_commande, utilisateur.login, commande.date_achat, 
    SUM(ligne_commande.quantite_lc) AS nbr_meubles, 
    SUM(ligne_commande.prix_lc * ligne_commande.quantite_lc) AS prix_total,
    etat.libelle_etat AS libelle 
    FROM commande
    JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
    JOIN etat ON commande.etat_id = etat.id_etat
    JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
    GROUP BY commande.id_commande, utilisateur.login, commande.date_achat,etat.libelle_etat;
    '''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    if id_commande is not None:
        sql = '''
                SELECT meuble.nom_meuble AS nom, ligne_commande.quantite_lc AS quantite, 
                (ligne_commande.prix_lc * ligne_commande.quantite_lc) AS prix_ligne, ligne_commande.prix_lc AS prix
                FROM meuble 
                JOIN ligne_commande ON meuble.id_meuble = ligne_commande.declinaison_meuble_id
                WHERE ligne_commande.commande_id = %s
            '''

        mycursor.execute(sql, (id_commande,))
        meubles_commande = mycursor.fetchall()
        # (ADMIN) si l’administrateur consulte une commande il peut voir l’adresse d’expédition et l’adresse de facturation
        sql_commande_details = '''SELECT nom_adresse_fact as nom_facturation,
        rue_adresse_fact as rue_facturation,
        code_postal_fact as code_postal_facturation,
        ville_fact as ville_facturation,
        nom_adresse_livr as nom_livraison,
        rue_livr as rue_livraison,
        code_postal_livr as code_postal_livraison,
        ville_livr as ville_livraison
        FROM v_commande 
        WHERE id_commande = %s
        '''
        mycursor.execute(sql_commande_details, (id_commande,))
        commande_adresses = mycursor.fetchone()

    return render_template('admin/commandes/show.html',
                           commandes=commandes,
                           meubles_commande=meubles_commande,
                           commande_adresses=commande_adresses)


@admin_commande.route('/admin/commande/valider', methods=['get', 'post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id is not None:
        print(commande_id)
        sql = '''UPDATE commande SET etat_id = 3 WHERE id_commande = %s'''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()
    return redirect('/admin/commande/show')
