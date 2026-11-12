from dataclasses import dataclass
from abc import ABC, abstractmethod

# a) Paciente (5 pts):

@dataclass(frozen=True)
class Paciente:
    nome: str
    cartao_sus: str

# b) Atendimento e suas especializações (15 pts):

class Atendimento(ABC):
    def __init__(self, paciente: Paciente) -> None:
        self._paciente: Paciente = paciente

    @property
    def paciente(self) -> Paciente:
        return self._paciente

    @abstractmethod
    def duracao_minutos(self) -> int:
        pass