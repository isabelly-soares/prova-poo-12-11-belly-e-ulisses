from dataclasses import FrozenInstanceError

from arquivos import (
    Agenda,
    AgendaError,
    Atendimento,
    Consulta,
    Exame,
    Paciente,
    Vacinacao,
)


def main() -> None:
    maria: Paciente = Paciente("Maria Silva", "123456789012345")
    joao: Paciente = Paciente("João Souza", "987654321098765")
    ana: Paciente = Paciente("Ana Lima", "111222333444555")
    pedro: Paciente = Paciente("Pedro Rocha", "555444333222111")

    print("Pacientes iguais:", maria == Paciente("Maria Silva", "123456789012345"))

    try:
        maria.nome = "Outro Nome"  # type: ignore[misc]
    except FrozenInstanceError:
        print("Erro: não é possível alterar um paciente após criado.")

    try:
        Atendimento(maria)  # type: ignore[abstract]
    except TypeError:
        print("Erro: não é possível instanciar Atendimento diretamente.")

    agenda: Agenda = Agenda(limite_minutos=90)

    novos_atendimentos: list[Atendimento] = [
        Consulta(maria, "Clínica Geral"),
        Exame(joao, "Hemograma", jejum=True),
        Consulta(maria, "Cardiologia", retorno=True),
        Vacinacao(ana, "Gripe", doses=1),
        Vacinacao(pedro, "Hepatite B", doses=3),
    ]

    for atendimento in novos_atendimentos:
        try:
            agenda.agendar(atendimento)
            print(f"Agendado: {atendimento}")
        except AgendaError as erro:
            print(f"Falha ao agendar: {erro}")

    print("\nAtendimentos agendados:")
    for atendimento in agenda.atendimentos:
        print(f"- {atendimento}")

    print(f"\nMinutos ocupados: {agenda.minutos_ocupados}/{agenda.limite_minutos}")


if __name__ == "__main__":
    main()