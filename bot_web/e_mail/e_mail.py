from botcity.plugins.email import BotEmailPlugin

def enviar_email_anexo(destinatario, assunto, conteudo, arquivo_anexo):
   # Instanciar o plugin de e-mail
   email = BotEmailPlugin()
   # Configurar IMAP e SMTP com o servidor Gmail
   email.configure_imap("imap.gmail.com", 993)
   email.configure_smtp("smtp.gmail.com", 587)
   # Login com a conta do emissor
   email.login(email="botcityifam@gmail.com",password="licp pjdk zdet japu")

   # Definir os atributos da mensagem
   to = [destinatario]
   subject = assunto
   body = conteudo
   files = [arquivo_anexo]

   # Enviar mensagem
   email.send_message(subject, body, to, attachments=files, use_html=True)
   # Fechar a conexão com os servidores IMAP e SMTP
   email.disconnect()
