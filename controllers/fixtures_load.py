#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__, template_folder='templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    sql = ''' 
DROP TABLE IF EXISTS liste_envie,
historique,
commentaire,
note,
ligne_panier,
ligne_commande,
concerne,
declinaison_meuble,
meuble,
commande,
type_meuble,
materiau,
etat,
adresse,
utilisateur;
    '''
    mycursor.execute(sql)

    sql = '''
CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(255),
   email VARCHAR(255),
   nom_utilisateur VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   est_actif TINYINT,
   PRIMARY KEY(id_utilisateur)
);  
    '''
    mycursor.execute(sql) 

    sql = '''
CREATE TABLE adresse(
   id_adresse INT AUTO_INCREMENT,
   nom_adresse VARCHAR(255),
   rue VARCHAR(255),
   code_postal VARCHAR(5),
   ville VARCHAR(255),
   valide TINYINT,
   PRIMARY KEY(id_adresse)
);
    '''
    mycursor.execute(sql)

    sql = '''
CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(255),
   PRIMARY KEY(id_etat)
);
    '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE materiau(
   id_materiau INT AUTO_INCREMENT,
   libelle_materiau VARCHAR(255),
   PRIMARY KEY(id_materiau)
);
    '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE type_meuble(
   id_type_meuble INT AUTO_INCREMENT,
   libelle_type_meuble VARCHAR(255),
   PRIMARY KEY(id_type_meuble)
);
    '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATETIME,
  adresse_id_livr INT NOT NULL,
   etat_id INT NOT NULL,
   utilisateur_id  INT NOT NULL,
   adresse_id_fact  INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(adresse_id_livr) REFERENCES adresse(id_adresse),
   FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(adresse_id_fact) REFERENCES adresse(id_adresse)
);
     '''
    mycursor.execute(sql)
    
    sql = '''
CREATE TABLE meuble(
   id_meuble INT AUTO_INCREMENT,
   nom_meuble VARCHAR(255),
   disponible INT,
   prix_meuble DECIMAL(19,4),
   description_meuble VARCHAR(255),
   image_meuble VARCHAR(255),
   type_meuble_id INT NOT NULL,
   PRIMARY KEY(id_meuble),
   FOREIGN KEY(type_meuble_id) REFERENCES type_meuble(id_type_meuble)
);
    '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE declinaison_meuble(
   id_declinaison_meuble INT AUTO_INCREMENT,
   stock INT,
   prix_declinaison DECIMAL(19,4),
   image_declinaison VARCHAR(255),
   meuble_id INT NOT NULL,
   materiau_id  INT NOT NULL,
   PRIMARY KEY(id_declinaison_meuble),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble),
   FOREIGN KEY(materiau_id) REFERENCES materiau(id_materiau)
);
    '''
    mycursor.execute(sql)

    sql = '''
CREATE TABLE concerne(
   utilisateur_id  INT,
   adresse_id INT,
   PRIMARY KEY(utilisateur_id, adresse_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(adresse_id) REFERENCES adresse(id_adresse)
);
    '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE ligne_commande(
   commande_id  INT,
   declinaison_meuble_id INT,
   quantite_lc INT,
   prix_lc DECIMAL(19,4),
   PRIMARY KEY(commande_id, declinaison_meuble_id),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
   FOREIGN KEY(declinaison_meuble_id) REFERENCES declinaison_meuble(id_declinaison_meuble)
);
    '''
    mycursor.execute(sql)

    sql = '''
CREATE TABLE ligne_panier(
   utilisateur_id INT,
   declinaison_meuble_id INT,
   date_ajout DATETIME,
   quantite_lp INT,
   PRIMARY KEY(utilisateur_id, declinaison_meuble_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(declinaison_meuble_id) REFERENCES declinaison_meuble(id_declinaison_meuble)
);
    '''

    mycursor.execute(sql)

    sql = '''
CREATE TABLE note(
   utilisateur_id INT,
   meuble_id INT,
   note DECIMAL(2,1),
   PRIMARY KEY(utilisateur_id, meuble_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);
    '''

    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE commentaire(
   utilisateur_id INT,
   meuble_id INT,
   date_publication DATETIME,
   commentaire VARCHAR(255),
   valider INT,
   PRIMARY KEY(utilisateur_id, meuble_id, date_publication),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);
    '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE historique(
   utilisateur_id INT,
   meuble_id INT,
   date_consultation DATETIME,
   PRIMARY KEY(utilisateur_id, meuble_id, date_consultation),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);
    '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE liste_envie(
   utilisateur_id INT,
   meuble_id INT,
   date_update DATETIME,
   PRIMARY KEY(utilisateur_id, meuble_id, date_update),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);
        '''
    mycursor.execute(sql)


    sql = ''' 
INSERT INTO utilisateur (login,email,nom_utilisateur,password,`role`,est_actif) VALUES
	 ('admin','admin@admin.fr','Administrateur','pbkdf2:sha256:600000$828ij7RCZN24IWfq$3dbd14ea15999e9f5e340fe88278a45c1f41901ee6b2f56f320bf1fa6adb933d','ROLE_admin',1),
	 ('client','client@client.fr','Semih Remork','pbkdf2:sha256:600000$ik00jnCw52CsLSlr$9ac8f694a800bca6ee25de2ea2db9e5e0dac3f8b25b47336e8f4ef9b3de189f4','ROLE_client',1),
	 ('client2','client2@client2.fr','Jack Séparou','pbkdf2:sha256:600000$3YgdGN0QUT1jjZVN$baa9787abd4decedc328ed56d86939ce816c756ff6d94f4e4191ffc9bf357348','ROLE_client',1);
    '''
    mycursor.execute(sql)


    sql = '''
INSERT INTO adresse (nom_adresse,rue,code_postal,ville,valide) VALUES
	 ('Crêperie les Tonnelles','101 Av. du Maréchal Foch','93210','Saint-Cloud',1),
	 ('Residhome Paris Issy-les-Moulineaux','22-24 Rue du Passeur de Boulogne','92130','Issy-les-Moulineaux',1),
	 ('Jack Séparou Maison','Boulevard not','06401','Cdds',1),
	 ('DSI Group','41 Av. du Général Leclerc','90350','Le Plessis-Robinson',1);
        '''
    mycursor.execute(sql)


    sql = ''' 
INSERT INTO etat (libelle_etat) VALUES
	 ('En attente'),
	 ('Expédié'),
	 ('Validé'),
	 ('Confirmé');
        '''
    mycursor.execute(sql)

    sql = ''' 
INSERT INTO materiau (libelle_materiau) VALUES
	 ('Sheesham massif'),
	 ('Mélaminé blanc'),
	 ('Verre'),
	 ('Rotin'),
	 ('Violet'),
	 ('Rose'),
	 ('Rouge'),
	 ('Gris'),
	 ('Vert'),
	 ('Blanc'),
	 ('Orange'),
	 ('Noir'),
	 ('Bleu'),
	 ('Bleu foncé'),
	 ('Bleu clair'),
	 ('Hêtre massif'),
	 ('Chêne massif'),
	 ('Noyer massif'),
	 ('Pin massif'),
	 ('Eucalyptus'),
	 ('Chêne clair'),
	 ('Chêne foncé');
    '''
    mycursor.execute(sql)

    sql = ''' 
INSERT INTO type_meuble (libelle_type_meuble) VALUES
	 ('Étagère'),
	 ('Table'),
	 ('Buffet'),
	 ('Bibliothèque'),
	 ('Vitrine'),
	 ('Chaise'),
	 ('Pouf');
    '''
    mycursor.execute(sql)

    sql = '''
INSERT INTO commande (date_achat,adresse_id_livr,etat_id,utilisateur_id,adresse_id_fact) VALUES
	 ('2024-01-01 00:00:00',2,1,2,2),
	 ('2024-01-02 00:00:00',2,1,2,2),
	 ('2024-01-03 00:00:00',4,2,3,4),
	 ('2024-01-04 00:00:00',4,3,3,4),
	 ('2023-03-03 00:00:00',2,4,2,2),
     ('2023-03-03 00:00:00',3,4,2,3); 
    '''
    mycursor.execute(sql)

    sql = '''
INSERT INTO meuble (nom_meuble,disponible,prix_meuble,description_meuble,image_meuble,type_meuble_id) VALUES
	 ('Etagère déstructuré',1,819.0000,'Une étagère fort sympathique.','1.jpg',1),
	 ('Table en sheesham',1,419.0000,'C''est une table... et elle est en sheesham...','2.jpg',2),
	 ('Buffet 2 portes 3 tiroirs',1,799.0000,'Plus de porte que dans une voiture familiale.','3.jpg',3),
	 ('Bibliothèque personnalisable',1,976.0000,'On sait que vous ne lirez pas ce qu''il y a dedans.','4.jpg',4),
	 ('Vitrine en verre',1,700.0000,'Parce qu''on ne voyait pas à travers celle en bois.','13.jpg',5),
	 ('Banc TV',1,345.0000,'C''est pour la télé pas pour vous ! Enfin je crois...','14.jpg',2),
	 ('Vitrine figurine',1,518.0000,'En voilà un qui a un hobbie qui ne plait pas à sa femme.','15.jpg',5),
	 ('Chaise Venus',1,159.0000,'On voulait l''appeler Uranus mais ça sonnait pas aussi sérieux...','16.jpg',6),
	 ('Chaise en rotin',1,226.0000,'Et pas en pétin, ahahah...','18.jpg',6),
	 ('Chaise simple',1,56.0000,'Il faut vraiment que j''explique ce que c''est ?','19.jpg',6),
	 ('Chaise jardin',1,65.0000,'Une chaise mais à mettre dans le jardin... Ou pas, je m''en fiche','23.jpg',6),
	 ('Table longue',1,895.0000,'Vous pouvez surement vous allongez dessus aussi','29.jpg',2),
	 ('Table à manger',1,950.0000,'Cette table là, c''est uniquement pour manger !','30.jpg',2),
	 ('Table rustique',1,1450.0000,'Elle est vieille mais rustique c''est plus vendeur.','31.jpg',2),
	 ('Table ronde',1,425.0000,'Mais toujours pas de trace du graal... Quelqu''un a vu Perceval ?','32.jpg',2),
	 ('Table en dur',1,2250.0000,'Parce que les tables molles tiennent pas aussi bien.','33.jpg',2),
	 ('Table bar',1,1400.0000,'Pour un bon ricard !','34.jpg',2),
	 ('Bibliothèque escalier',1,750.0000,'Je crois qu''on peut monter dessus, j''ai juste pas d''étage chez moi','35.jpg',4),
	 ('Pouf plastique',1,75.0000,'Et non une femme de petite vertue ayant fait de la chirurgie esthétique','38.jpg',7),
	 ('Pouf Velour',1,150.0000,'C''est tout doux !','43.jpg',7);
    '''
    mycursor.execute(sql)

    sql = '''
INSERT INTO declinaison_meuble (stock,prix_declinaison,image_declinaison,meuble_id,materiau_id) VALUES
	 (8,819.0000,'1.jpg',1,1),
	 (2,419.2500,'2.jpg',2,1),
	 (3,799.0000,'3.jpg',3,1),
	 (12,976.5000,'4.jpg',4,2),
	 (1,1427.0000,'7.jpg',4,16),
	 (6,1725.0000,'10.jpg',4,17),
	 (13,700.0000,'13.jpg',5,3),
	 (12,345.0000,'14.jpg',6,3),
	 (2,518.0000,'15.jpg',7,3),
	 (2,159.0000,'16.jpg',8,17),
	 (5,159.5000,'17.jpg',8,18),
	 (3,226.0000,'18.jpg',9,4),
	 (25,56.0000,'19.jpg',10,5),
	 (16,56.0000,'20.jpg',10,6),
	 (11,57.0000,'21.jpg',10,8),
	 (7,56.9900,'22.jpg',10,9),
	 (7,65.0000,'23.jpg',11,8),
	 (4,65.2000,'24.jpg',11,9),
	 (2,64.0000,'25.jpg',11,10),
	 (1,66.0000,'26.jpg',11,11),
	 (5,66.0000,'27.jpg',11,12),
	 (6,65.0000,'28.jpg',11,13),
	 (21,895.9900,'29.jpg',12,17),
	 (2,950.0000,'30.jpg',13,17),
	 (5,1450.2500,'31.jpg',14,19),
	 (6,425.0000,'32.jpg',15,19),
	 (7,2250.0000,'33.jpg',16,20),
	 (16,1400.0000,'34.jpg',17,20),
	 (23,750.0000,'35.jpg',18,17),
	 (2,750.0000,'36.jpg',18,17),
	 (0,76.0000,'38.jpg',19,12),
	 (5,75.0000,'39.jpg',19,11),
	 (6,76.0000,'41.jpg',19,7),
	 (0,75.0000,'42.jpg',19,9),
	 (12,151.0000,'43.jpg',20,10),
	 (11,150.2500,'44.jpg',20,9),
	 (8,152.9900,'45.jpg',20,14),
	 (9,152.9900,'46.jpg',20,15),
	 (19,152.9900,'47.jpg',20,8),
	 (27,152.9900,'48.jpg',20,6);
    '''
    mycursor.execute(sql)
    
    sql = '''
INSERT INTO concerne (utilisateur_id,adresse_id) VALUES
	 (1,1),
	 (2,2),
	 (2,3),
	 (3,4);
    '''
    mycursor.execute(sql)
    
    sql = '''
INSERT INTO ligne_commande (commande_id,declinaison_meuble_id,quantite_lc,prix_lc) VALUES
	(1,1,2,819.0000),
	(1,2,1,419.0000),
	(2,3,3,799.0000),
	(3,1,1,819.0000),
	(4,1,11,819.0000),
	(4,2,5,419.0000),
	(4,3,4,799.0000),
	(4,4,12,976.0000),
	(4,5,6,1427.0000),
	(4,31,5,75.0000),
	(4,32,6,75.0000),
	(4,33,7,72.0000),
	(4,34,16,73.0000),
	(4,35,23,150.0000),
	(4,36,2,145.0000),
	(4,38,5,145.0000),
	(4,39,6,155.0000),
	(5,1,2,819.0000),
	(5,2,1,419.0000),
	(5,3,3,799.0000),
	(5,25,2,1445.0000),
	(5,34,11,75.0000),
    (5,35,12,150.0000),
    (6,31,2,75.0000),
    (6,32,1,75.0000),
    (6,33,3,72.0000);
    '''
    mycursor.execute(sql)
    
    sql = '''
INSERT INTO ligne_panier (utilisateur_id,declinaison_meuble_id,date_ajout,quantite_lp) VALUES
	 (1,1,'2024-01-01 00:00:00',2),
	 (1,3,'2024-01-01 00:00:00',1),
	 (2,1,'2024-01-02 00:00:00',3),
	 (2,2,'2024-01-02 00:00:00',3),
	 (3,1,'2024-01-03 00:00:00',1);
    '''
    mycursor.execute(sql)

   
    sql = '''
drop view if exists v_commande,
v_concerne,
v_declinaison_meuble,
v_historique,
v_ligne_commande,
v_ligne_panier,
v_liste_envie,
v_note;
    '''
    mycursor.execute(sql)
    
    sql = '''
create view v_declinaison_meuble as
select *
from declinaison_meuble dm
join meuble m on m.id_meuble = dm.meuble_id
join type_meuble tm on m.type_meuble_id = tm.id_type_meuble;
    '''
    mycursor.execute(sql)
    
    sql = '''
create view v_ligne_commande as
select *
from ligne_commande lc
join commande c on lc.commande_id = c.id_commande
join declinaison_meuble dm on lc.declinaison_meuble_id = dm.id_declinaison_meuble;
    '''
    mycursor.execute(sql)
    
    sql = '''
create view v_ligne_panier as
select *
from ligne_panier lp
join utilisateur u on u.id_utilisateur = lp.utilisateur_id
join declinaison_meuble dm on dm.id_declinaison_meuble = lp.declinaison_meuble_id;
    '''
    mycursor.execute(sql)

    sql = '''
create view v_concerne as
select *
from concerne
join utilisateur u on u.id_utilisateur = concerne.utilisateur_id
join adresse a on a.id_adresse = concerne.adresse_id;
    '''
    mycursor.execute(sql)
    
    sql = '''
create view v_liste_envie as
select *
from liste_envie
join utilisateur u on u.id_utilisateur = liste_envie.utilisateur_id
join meuble m on liste_envie.meuble_id = m.id_meuble;
    '''
    mycursor.execute(sql)
    
    sql = '''
create view v_historique as
select *
from historique
join utilisateur u on u.id_utilisateur = historique.utilisateur_id
join meuble m on m.id_meuble = historique.meuble_id;
    '''
    mycursor.execute(sql)
    
    sql = '''
create view v_note as
select *
from note n
join meuble m on m.id_meuble = n.meuble_id
join utilisateur u on u.id_utilisateur = n.utilisateur_id;
    '''
    mycursor.execute(sql)
    
    sql = '''
create view if not exists v_commande as
select `c`.`id_commande`     AS `id_commande`,
       `c`.`date_achat`      AS `date_achat`,
       `c`.`etat_id`         AS `etat_id`,
       `c`.`utilisateur_id`  AS `utilisateur_id`,
       `c`.`adresse_id_fact` AS `adresse_id_fact`,
       `a`.`id_adresse`      AS `id_adresse_fact`,
       `a`.`nom_adresse`     AS `nom_adresse_fact`,
       `a`.`rue`             AS `rue_adresse_fact`,
       `a`.`code_postal`     AS `code_postal_fact`,
       `a`.`ville`           AS `ville_fact`,
       `a`.`valide`          AS `valide_fact`,
       `c`.`adresse_id_livr` AS `adresse_id_livr`,
       `a2`.`id_adresse`     AS `id_adresse_livr`,
       `a2`.`nom_adresse`    AS `nom_adresse_livr`,
       `a2`.`rue`            AS `rue_livr`,
       `a2`.`code_postal`    AS `code_postal_livr`,
       `a2`.`ville`          AS `ville_livr`,
       `a2`.`valide`         AS `valide_livr`,
       `e`.`id_etat`         AS `id_etat`,
       `e`.`libelle_etat`    AS `libelle_etat`,
       `u`.`id_utilisateur`  AS `id_utilisateur`,
       `u`.`login`           AS `login`,
       `u`.`email`           AS `email`,
       `u`.`nom_utilisateur` AS `nom_utilisateur`,
       `u`.`password`        AS `password`,
       `u`.`role`            AS `role`,
       `u`.`est_actif`       AS `est_actif`
from ((((`commande` `c` join `adresse` `a`
         on (`c`.`adresse_id_fact` = `a`.`id_adresse`)) join `adresse` `a2`
        on (`a2`.`id_adresse` = `c`.`adresse_id_livr`)) join `etat` `e`
       on (`c`.`etat_id` = `e`.`id_etat`)) join `utilisateur` `u`
      on (`c`.`utilisateur_id` = `u`.`id_utilisateur`));
    '''
    mycursor.execute(sql)
    
    get_db().commit()
    return redirect('/')
