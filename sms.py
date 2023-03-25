from twilio.rest import Client

account_sid = 'sid da sua conta do twilio'
auth_token = 'seu token do twilio'

def enviar_mensagem(valor):    
    client = Client(account_sid, auth_token)
    client.messages.create(from_='numero do twilio', to='seu numero', body=f'O valor das moedas solicitadas:\n{valor}')
    