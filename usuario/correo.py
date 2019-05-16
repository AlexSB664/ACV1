from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings

class Correo:

	def enviarCorreo(self,correo,nombre_completo):
		subject = 'Confirmacion de pago'
		message = 'Gracias por u confianza '+nombre_completo+ '		se ah confirmado el pago por medio de OXXOPAY' 
		message = message + '<br> Atte:Ayuda Contable'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [correo]
		send_mail(subject,message,email_from,recipient_list)
		msg = EmailMultiAlternatives(subject, message, email_from, recipient_list)

