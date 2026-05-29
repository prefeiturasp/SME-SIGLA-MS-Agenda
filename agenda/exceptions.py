class AgendaOnlineJaExisteException(Exception):
    """Indica que uma agenda online já existe para o processo e cargo."""

    def __init__(self, processo_nome, cargo_nome):
        self.processo_nome = processo_nome
        self.cargo_nome = cargo_nome
        super().__init__(
            f"Agenda online já existe para o processo "
            f"{processo_nome} e cargo {cargo_nome}"
        )
