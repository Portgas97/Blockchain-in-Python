import time


class Transaction:

    def __init__(self, sender, amount, receiver, sign, timestamp=time.time()):
        """
        Crea una nuova transazione.
        Parametri:
        - sender (str) è l'account del mittente
        - amount (float) è l'ammontare da trasferire
        - receiver (str) è l'account del destinatario
        """
        self.sender = sender
        self.amount = amount
        self.receiver = receiver
        self.timestamp = timestamp
        self.sign = sign

        #aggiungere controllo firma
    def validate(self):
        """
        Controlla se una transazione è valida, ritorna un booleano
        """
        if int(self.amount) < 0:
            return False

        return True
