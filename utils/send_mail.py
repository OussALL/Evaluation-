from flask_mail import Message
def send_mail(mail,student,prenom,nom,username,nouveau_mot_de_passe):
    mssg=Message("Renitialisation de mot de passe",
                 sender="isgaprojet@gmail.com",
                 recipients=[student])
    mssg.body= f"""
Objet : Réinitialisation de votre mot de passe

Bonjour {prenom} {nom},

Suite à votre demande (ou suite à une action de l’administrateur), votre mot de passe a été réinitialisé avec succès.

Voici vos nouvelles informations de connexion :

- Nom d'utilisateur : {username}
- Nouveau mot de passe : {nouveau_mot_de_passe}

⚠️ Nous vous recommandons de changer ce mot de passe dès votre première connexion pour garantir la sécurité de votre compte.



Si vous n'êtes pas à l'origine de cette demande ou si vous avez des questions, n'hésitez pas à nous contacter.

Cordialement,  
L'équipe pédagogique / Support technique
"""
    mail.send(mssg)