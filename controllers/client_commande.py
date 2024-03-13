#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
        SELECT * FROM ligne_panier
        WHERE utilisateur_id = %s;
    '''
    meubles_panier = []
    if len(meubles_panier) >= 1:
        sql = '''
            SELECT SUM(prix_declinaison * quantite_lp) AS prix_total
            FROM ligne_panier
            JOIN declinaison_meuble ON ligne_panier.declinaison_meuble_id = declinaison_meuble.id_declinaison_meuble
            WHERE utilisateur_id = %s;
        '''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()
    else:
        prix_total = None
        
    # etape 2 : selection des adresses
    sql = '''
        SELECT * 
        FROM adresse
        JOIN concerne ON adresse.id_adresse = concerne.adresse_id
        WHERE utilisateur_id = %s AND adresse.valide = '1';
    '''
    mycursor.execute(sql, id_client)
    adresses = mycursor.fetchall()
    
    # etape 3 : selection de la dernière adresse de livraison et de facturation
    sql = '''
    SELECT adresse_id_livr, adresse_id_fact
    FROM v_commande
    WHERE id_commande = (SELECT MAX(id_commande) FROM commande WHERE utilisateur_id = %s) AND valide_livr = '1' AND valide_fact = '1'
    '''
    mycursor.execute(sql, id_client)
    id_adresse_fav = mycursor.fetchone()
    print("id_adresse_fav : " + str(id_adresse_fav))
    # etape 3-1 : si la dernière adresse de livraison et de facturation n'existe pas, on prend celle étant dans le plus de commandes
    if id_adresse_fav is None:
        # Toutes les combinaisons d'adresses de livraison et de facturation sont listés, puis on la combinaison la plus fréquente
        sql = '''
        SELECT adresse_id_livr, adresse_id_fact, COUNT(*) AS nb_commandes
        FROM v_commande
        WHERE valide_livr = '1' AND valide_fact = '1'
        GROUP BY adresse_id_livr, adresse_id_fact
        ORDER BY nb_commandes DESC
        '''
        mycursor.execute(sql)
        id_adresse_fav = mycursor.fetchone()
        print("id_adresse_fav : " + str(id_adresse_fav))
   

        
    
    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , meubles_panier=meubles_panier
                           , prix_total= prix_total
                           , validation=1
                           , id_adresse_fav=id_adresse_fav 
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
        
    mycursor = get_db().cursor()
    id_client = session['id_user']
    adresse_id_livr = request.form['id_adresse_livraison']
    print("adresse_id_livr : " + adresse_id_livr)

    ###
    # Vérifier si l'adresse de livraison est la même que l'adresse de facturation mais que la checkbox n'est pas cochée
    ###
    adresse_identique = request.form.get('adresse_identique')
    if adresse_identique != None:
        adresse_id_fact = adresse_id_livr
    else:
        adresse_id_fact = request.form['id_adresse_facturation']
    print("adresse_id_fact : " + adresse_id_fact)
    
    ###
    # empecher la validation et message flash si l'adresse de livraison et de facturation sont les mêmes
    ###
    adresse_identique = request.form.get('adresse_identique')
    print("adresse_identique : " + str(adresse_identique))
    if adresse_identique == None and (adresse_id_fact == adresse_id_livr):
        flash(u'Adresse de livraison et de facturation identiques, veuillez utilisez la checkbox','alert-warning')
        return redirect('/client/meuble/show')

    sql = "SELECT * FROM v_ligne_panier WHERE id_utilisateur=%s"
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le panier')
        return redirect('/client/article/show')

    tuple_insert = (id_client, '1', adresse_id_fact, adresse_id_livr)  # 1 : état de commande : "en cours" ou "validé"
    sql = "INSERT INTO commande(date_achat, utilisateur_id, etat_id, adresse_id_fact, adresse_id_livr) VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s)"
    mycursor.execute(sql, tuple_insert)
    sql = "SELECT last_insert_id() as last_insert_id"
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()

    for item in items_ligne_panier:
        sql = "DELETE FROM ligne_panier WHERE utilisateur_id = %s AND declinaison_meuble_id = %s"
        mycursor.execute(sql, (item['utilisateur_id'], item['declinaison_meuble_id']))

        sql = "INSERT INTO ligne_commande (commande_id, declinaison_meuble_id, prix_lc, quantite_lc) VALUES (%s, %s, %s, %s)"
        tuple_insert = (commande_id['last_insert_id'], item['declinaison_meuble_id'], item['prix_declinaison'], item['quantite_lp'])
        mycursor.execute(sql, tuple_insert)

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/meuble/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    print("id_client : " + str(id_client))
    # sql = '''
    #     SELECT c.id_commande,
    #         date_achat,
    #         SUM(lc.quantite_lc) AS nbr_meubles,
    #         SUM(lc.prix * lc.quantite_lc) AS prix_total,
    #         etat_id,
    #         libelle_etat AS libelle
    #     FROM ligne_commande lc
    #     JOIN commande c ON lc.commande_id = c.id_commande
    #     JOIN meuble m ON lc.meuble_id = m.id_meuble
    #     JOIN etat e ON c.etat_id = e.id_etat
    #     WHERE c.utilisateur_id = %s
    #     GROUP BY c.id_commande, c.date_achat, c.etat_id, e.libelle_etat
    #     ORDER BY etat_id,
    #         date_achat DESC;
    # '''
    sql = '''
    SELECT * ,
    date_achat,
    libelle_etat AS libelle,
    SUM(quantite_lc) AS nbr_meubles,
    SUM(prix_lc * quantite_lc) AS prix_total
    FROM v_ligne_commande
    JOIN etat ON v_ligne_commande.etat_id = etat.id_etat
    WHERE utilisateur_id = %s
    GROUP BY id_commande, date_achat, etat_id, libelle_etat, id_etat
    '''
    mycursor.execute(sql, str(id_client))
    commandes = mycursor.fetchall()
    
    meubles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print("id_commande : " + id_commande)
        # sql = '''
        #     SELECT lc.quantite_lc,
        #         lc.prix,
        #         m.nom_meuble AS nom,
        #         m.prix_meuble AS prix,
        #         lc.prix * lc.quantite_lc AS prix_ligne
        #     FROM ligne_commande lc
        #         JOIN meuble m ON lc.meuble_id = m.id_meuble
        #     WHERE lc.commande_id = %s;
        # '''
        sql = '''
        SELECT nom_meuble AS nom,
            vl.prix_lc AS prix,
            vl.quantite_lc as quantite,
            prix_lc * quantite_lc AS prix_ligne
        FROM v_ligne_commande vl
        JOIN v_declinaison_meuble vd ON vl.declinaison_meuble_id = vd.id_declinaison_meuble
        WHERE id_commande = %s
        '''
        mycursor.execute(sql, str(id_commande))
        meubles_commande = mycursor.fetchall()
        print("meubles_commande : " + str(meubles_commande))
        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = '''
        SELECT nom_adresse_livr AS nom_livraison,
        rue_livr AS rue_livraison,
        code_postal_livr AS code_postal_livraison,
        ville_livr AS ville_livraison,
        nom_adresse_fact AS nom_facturation,
        rue_adresse_fact AS rue_facturation,
        code_postal_fact AS code_postal_facturation,
        ville_fact AS ville_facturation
        FROM v_commande WHERE id_commande = %s
        '''
        mycursor.execute(sql, str(id_commande))
        commande_adresses = mycursor.fetchone()
        print("commande_adresses : " + str(commande_adresses))


    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , meubles_commande=meubles_commande
                           , commande_adresses=commande_adresses
                           )
