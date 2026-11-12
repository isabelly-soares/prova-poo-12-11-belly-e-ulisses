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

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} - Paciente: {self.paciente.nome} - "
            f"Duração: {self.duracao_minutos()} min"
        )


class Consulta(Atendimento):
    def __init__(self, paciente: Paciente, especialidade: str, retorno: bool = False) -> None:
        super().__init__(paciente)
        self.especialidade: str = especialidade
        self.retorno: bool = retorno

    def duracao_minutos(self) -> int:
        return 15 if self.retorno else 30


class Exame(Atendimento):
    def __init__(self, paciente: Paciente, tipo: str, jejum: bool = False) -> None:
        super().__init__(paciente)
        self.tipo: str = tipo
        self.jejum: bool = jejum

    def duracao_minutos(self) -> int:
        return 30 if self.jejum else 20


class Vacinacao(Atendimento):
    def __init__(self, paciente: Paciente, vacina: str, doses: int = 1) -> None:
        super().__init__(paciente)
        self.vacina: str = vacina
        self.doses: int = doses

    def duracao_minutos(self) -> int:
        return 10 * self.doses

class AgendaError(Exception):
    pass


class HorarioIndisponivelError(AgendaError):
    pass


class PacienteJaAgendadoError(AgendaError):
    pass

# d) Agenda (20 pts):

class Agenda:
    def __init__(self, limite_minutos: int = 240) -> None:
        self._limite_minutos: int = limite_minutos
        self._atendimentos: list[Atendimento] = []

    @property
    def limite_minutos(self) -> int:
        return self._limite_minutos

    @property
    def atendimentos(self) -> tuple[Atendimento, ...]:
        return tuple(self._atendimentos)

    @property
    def minutos_ocupados(self) -> int:
        return sum(atendimento.duracao_minutos() for atendimento in self._atendimentos)

    @property
    def minutos_livres(self) -> int:
        return self._limite_minutos - self.minutos_ocupados

    def agendar(self, atendimento: Atendimento) -> None:
        for agendado in self._atendimentos:
            if agendado.paciente == atendimento.paciente:
                raise PacienteJaAgendadoError(
                    f"O paciente {atendimento.paciente.nome} "
                    f"(cartão SUS {atendimento.paciente.cartao_sus}) já possui atendimento na agenda."
                )
        if atendimento.duracao_minutos() > self.minutos_livres:
            raise HorarioIndisponivelError(
                f"Não há horário disponível: o atendimento requer {atendimento.duracao_minutos()} min, "
                f"mas restam apenas {self.minutos_livres} min livres na agenda."
            )
        self._atendimentos.append(atendimento)