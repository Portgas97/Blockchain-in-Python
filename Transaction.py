import time


class Transaction:
    def __init__(self, sender, amount, receiver, timestamp=time.time()):
        """
        Crea una nuova transazione.
        Parametri:
        - sender (str) è l'account del mittente
        - receiver (str) è l'account del destinatario
        - amount (float) è l'ammontare da trasferire
        """
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp
        self.amount = amount

    def validate(self):
        """
        Controlla se una transazione è valida, ritorna un booleano
        """

        if int(self.amount) < 0:
            return False

        return True
