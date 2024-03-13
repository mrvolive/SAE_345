#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    utilisateur=[]
    nb_adresses = 0

    sql = '''
    SELECT login, nom_utilisateur as nom, email
    FROM utilisateur WHERE id_utilisateur = %s
    '''
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchone()
    print(utilisateur)

    sql = '''
    SELECT *, nom_adresse as nom
    FROM adresse
    JOIN concerne ON adresse.id_adresse = concerne.adresse_id
    WHERE utilisateur_id = %s 
    '''
    mycursor.execute(sql, id_client)
    adresses = mycursor.fetchall()
    
    # Compter le nombre d'adresses de l'utilisateur
    sql = '''
    SELECT COUNT(*) as nb_adresses
    FROM adresse
    JOIN concerne ON adresse.id_adresse = concerne.adresse_id
    WHERE utilisateur_id = %s and valide = '1'
    '''
    mycursor.execute(sql, id_client)
    nb_adresses = mycursor.fetchone() # Récupérer le nombre d'adresses sous forme de dictionnaire
    nb_adresses = nb_adresses['nb_adresses'] # Récupérer la valeur du nombre d'adresses dans le dictionnaire pour récupérer un int
    print(nb_adresses)

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                           , nb_adresses=nb_adresses
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
    SELECT login, nom_utilisateur as nom, email
    FROM utilisateur
    WHERE id_utilisateur = %s
    '''
    mycursor.execute(sql,id_client)
    utilisateur=mycursor.fetchone()

    return render_template('client/coordonnee/edit_coordonnee.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')
    utilisateur = []

    sql = '''
    SELECT *
    FROM utilisateur
    WHERE (login = %s OR nom_utilisateur = %s OR email = %s) AND id_utilisateur != %s
    '''
    tuple = (login,nom,email,id_client)
    mycursor.execute(sql,tuple)

    user = mycursor.fetchone()
    print("user = " + str(user))
    if user:
        flash(u'votre cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                               ,utilisateur=utilisateur
                               )
    
    sql = '''
    UPDATE utilisateur
    SET nom_utilisateur = %s, login = %s, email = %s
    WHERE id_utilisateur = %s;
    '''
    tuple = (nom,login,email,id_client)
    mycursor.execute(sql,tuple)

    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')

    # Vérifier si l'adresse est actuellement dans une commande
    sql = '''
    SELECT *
    FROM commande
    WHERE adresse_id_livr = %s OR adresse_id_fact = %s
    '''
    tuple = (id_adresse,id_adresse)
    mycursor.execute(sql,tuple)
    adresse_block = mycursor.fetchone()
    print("adresse_block = " + str(adresse_block))
    
    # Si l'adresse est actuellement dans une commande, on la désactive
    if adresse_block:
        flash(u'Cette adresse est actuellement dans une commande','alert-warning')
        
        sql = '''
        UPDATE adresse
        SET valide = '0'
        WHERE id_adresse = %s
        '''
        mycursor.execute(sql,id_adresse)
        get_db().commit()
    
        return redirect('/client/coordonnee/show')
 
    # Sinon on la supprime dans concerne en premier pour pouvoir la supprimer dans adresse   
    sql = '''
    DELETE FROM concerne
    WHERE adresse_id = %s
    '''
    mycursor.execute(sql,id_adresse)
    get_db().commit()

    sql = '''
    DELETE FROM adresse
    WHERE id_adresse = %s
    '''
    mycursor.execute(sql,id_adresse)
    get_db().commit()

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
    SELECT nom_utilisateur as nom, login
    FROM adresse
    JOIN concerne ON adresse.id_adresse = concerne.adresse_id
    JOIN utilisateur ON concerne.utilisateur_id = utilisateur.id_utilisateur
    WHERE utilisateur_id = %s
    '''

    mycursor.execute(sql,id_client)
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/add_adresse.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')

    # Ne pas ajouter d'adresse si l'utilisateur en a déjà quatres
    sql = '''
    SELECT COUNT(*) as nb_adresses
    FROM adresse
    JOIN concerne ON adresse.id_adresse = concerne.adresse_id
    WHERE utilisateur_id = %s and valide = '1'
    '''
    mycursor.execute(sql,id_client)
    nb_adresses = mycursor.fetchone()
    print(nb_adresses)
    if nb_adresses['nb_adresses'] >= 4:
        flash(u'Vous avez déjà quatres adresses', 'alert-warning')
        return redirect('/client/coordonnee/show')
    
    sql = '''
    INSERT INTO adresse(nom_adresse,code_postal,ville,rue,valide)
    VALUES(%s,%s,%s,%s,'1');
    '''
    tuple = (nom,code_postal,ville,rue)
    mycursor.execute(sql,tuple)
    get_db().commit()

    
    sql = '''
    INSERT INTO concerne (utilisateur_id,adresse_id)
    VALUES(%s,(SELECT MAX(id_adresse) FROM adresse));
    '''

    mycursor.execute(sql,id_client)
    get_db().commit()
    
    

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    # Vérifier si l'adresse est actuellement dans une commande
    sql = '''
    SELECT *
    FROM commande
    WHERE adresse_id_livr = %s OR adresse_id_fact = %s
    '''
    tuple = (id_adresse,id_adresse)
    mycursor.execute(sql,tuple)
    adresse_block = mycursor.fetchone()
    print("adresse_block = " + str(adresse_block))
    if adresse_block:
        flash(u'Cette adresse est actuellement dans une commande','alert-warning')
        # Créer un doublon de l'adresse qui a été bloquée pour pouvoir la modifier
        # En sélectionnant l'adresse précédente pour en récupérer les informations
        sql = '''
        INSERT INTO adresse(nom_adresse,code_postal,ville,rue,valide)
        SELECT nom_adresse,code_postal,ville,rue,valide
        FROM adresse
        WHERE id_adresse = %s
        '''
        mycursor.execute(sql,id_adresse)
        sql = '''
        INSERT INTO concerne (utilisateur_id,adresse_id)
        VALUES(%s,(SELECT MAX(id_adresse) FROM adresse));
        '''
        mycursor.execute(sql,id_client)
        get_db().commit()
        # Rendre l'adresse précédente non-valide
        sql = '''
        UPDATE adresse
        SET valide = '0'
        WHERE id_adresse = %s
        '''
        mycursor.execute(sql,id_adresse)
        get_db().commit()
        
        return redirect('/client/coordonnee/show')
    
    # Afficher l'adresse à modifier
    sql = '''
    SELECT nom_adresse AS nom,code_postal,ville,rue,id_adresse
    FROM adresse
    WHERE id_adresse = %s
    '''
    mycursor.execute(sql,id_adresse)
    adresse = mycursor.fetchone()
    
    sql = '''
    SELECT *
    FROM utilisateur
    WHERE id_utilisateur = %s
    '''
    mycursor.execute(sql,id_client)
    utilisateur = mycursor.fetchone()

    return render_template('/client/coordonnee/edit_adresse.html'
                           ,utilisateur=utilisateur
                           ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    sql = '''
    UPDATE adresse
    SET nom_adresse = %s, code_postal = %s, ville = %s, rue = %s
    WHERE id_adresse = %s;
    '''
    tuple = (nom,code_postal,ville,rue,id_adresse)
    print(tuple)
    mycursor.execute(sql,tuple)
    get_db().commit()

    return redirect('/client/coordonnee/show')
