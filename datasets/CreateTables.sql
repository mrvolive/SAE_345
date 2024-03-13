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

CREATE TABLE adresse(
   id_adresse INT AUTO_INCREMENT,
   nom_adresse VARCHAR(255),
   rue VARCHAR(255),
   code_postal VARCHAR(5),
   ville VARCHAR(255),
   valide TINYINT,
   PRIMARY KEY(id_adresse)
);

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(255),
   PRIMARY KEY(id_etat)
);

CREATE TABLE materiau(
   id_materiau INT AUTO_INCREMENT,
   libelle_materiau VARCHAR(255),
   PRIMARY KEY(id_materiau)
);

CREATE TABLE type_meuble(
   id_type_meuble INT AUTO_INCREMENT,
   libelle_type_meuble VARCHAR(255),
   PRIMARY KEY(id_type_meuble)
);

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

CREATE TABLE concerne(
   utilisateur_id  INT,
   adresse_id INT,
   PRIMARY KEY(utilisateur_id, adresse_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(adresse_id) REFERENCES adresse(id_adresse)
);

CREATE TABLE ligne_commande(
   commande_id  INT,
   declinaison_meuble_id INT,
   quantite_lc INT,
   prix_lc DECIMAL(19,4),
   PRIMARY KEY(commande_id, declinaison_meuble_id),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
   FOREIGN KEY(declinaison_meuble_id) REFERENCES declinaison_meuble(id_declinaison_meuble)
);

CREATE TABLE ligne_panier(
   utilisateur_id INT,
   declinaison_meuble_id INT,
   date_ajout DATETIME,
   quantite_lp INT,
   PRIMARY KEY(utilisateur_id, declinaison_meuble_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(declinaison_meuble_id) REFERENCES declinaison_meuble(id_declinaison_meuble)
);

CREATE TABLE note(
   utilisateur_id INT,
   meuble_id INT,
   note DECIMAL(2,1),
   PRIMARY KEY(utilisateur_id, meuble_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);

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

CREATE TABLE historique(
   utilisateur_id INT,
   meuble_id INT,
   date_consultation DATETIME,
   PRIMARY KEY(utilisateur_id, meuble_id, date_consultation),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);

CREATE TABLE liste_envie(
   utilisateur_id INT,
   meuble_id INT,
   date_update DATETIME,
   PRIMARY KEY(utilisateur_id, meuble_id, date_update),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);
