# Checkpoint - Arquivos e JSON | Passagem de plantão
# Integrante 1: Arthur de Sá Lopes - RM569526
# Integrante 2: Mateus Alves Borges - RM571424
# Turma: 1ESPQ
# Contexto: Arsenal de Skins - Valorant (busca, api de skins, detalhes, coleções...)

import json

ARQUIVO_JSON = "ocorrencias.json"
ARQUIVO_DIARIO = "diario.txt"
ARQUIVO_PASSAGEM = "passagem.txt"
CONTEXTO = "Arsenal de Skins - Valorant"


def carregar_ocorrencias():
    """Retorna a lista salva, [] se o arquivo não existir ou None se o JSON for inválido."""
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arq:
            return json.load(arq)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("ocorrencias.json está inválido. Corrija o arquivo e tente novamente.")
        return None


def salvar_ocorrencias(lista):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arq:
        json.dump(lista, arq, ensure_ascii=False, indent=4)


def pedir_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("O campo não pode ficar vazio.")


def pedir_opcao(mensagem, validas):
    while True:
        valor = input(mensagem).strip().lower()
        if valor in validas:
            return valor
        print(f"Opção inválida. Use: {', '.join(validas)}.")


def registrar_ocorrencia():
    ocorrencias = carregar_ocorrencias()
    if ocorrencias is None:
        return  # JSON inválido: cadastro suspenso

    servico = pedir_texto("Serviço afetado (ex.: busca, api de skins, detalhes): ")
    descricao = pedir_texto("Descrição do problema: ")
    prioridade = pedir_opcao("Prioridade (alta/media/baixa): ", ["alta", "media", "baixa"])
    status = pedir_opcao("Status (aberto/resolvido): ", ["aberto", "resolvido"])

    if status == "resolvido":
        proxima_acao = "nenhuma"
    else:
        proxima_acao = pedir_texto("Próxima ação para a próxima equipe: ")

    ocorrencias.append({
        "servico": servico,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": status,
        "proxima_acao": proxima_acao,
    })
    salvar_ocorrencias(ocorrencias)
    print("Ocorrência registrada.")


def consultar_ocorrencias():
    ocorrencias = carregar_ocorrencias()
    if ocorrencias is None:
        return  # JSON inválido: consulta suspensa
    if not ocorrencias:
        print("Não há ocorrências.")
        return

    for i, oc in enumerate(ocorrencias, start=1):
        print(f"\nOcorrência {i}")
        print(f"  Serviço: {oc['servico']}")
        print(f"  Descrição: {oc['descricao']}")
        print(f"  Prioridade: {oc['prioridade']}")
        print(f"  Status: {oc['status']}")
        print(f"  Próxima ação: {oc['proxima_acao']}")


def registrar_diario():
    servico = pedir_texto("Serviço: ")
    anotacao = pedir_texto("Anotação: ")
    with open(ARQUIVO_DIARIO, "a", encoding="utf-8") as arq:
        arq.write(f"{servico} — {anotacao}\n")
    print("Anotação registrada no diário.")


def consultar_diario():
    try:
        with open(ARQUIVO_DIARIO, "r", encoding="utf-8") as arq:
            conteudo = arq.read()
    except FileNotFoundError:
        print("Nenhuma anotação registrada.")
        return
    if not conteudo.strip():
        print("Nenhuma anotação registrada.")
        return
    print("\n=== Diário ===")
    print(conteudo)


def gerar_passagem():
    ocorrencias = carregar_ocorrencias()
    if ocorrencias is None:
        return  # JSON inválido: resumo suspenso, passagem.txt anterior preservado

    abertas = []
    altas = 0
    for oc in ocorrencias:
        if oc["status"] == "aberto":
            abertas.append(oc)
            if oc["prioridade"] == "alta":
                altas += 1

    with open(ARQUIVO_PASSAGEM, "w", encoding="utf-8") as arq:
        arq.write(f"PASSAGEM DE PLANTÃO - {CONTEXTO}\n")
        arq.write(f"Ocorrências abertas: {len(abertas)}\n")
        arq.write(f"Abertas com prioridade alta: {altas}\n\n")
        if not abertas:
            arq.write("Nenhuma pendência para o próximo plantão\n")
        for i, oc in enumerate(abertas, start=1):
            arq.write(f"{i}) Serviço: {oc['servico']}\n")
            arq.write(f"   Descrição: {oc['descricao']}\n")
            arq.write(f"   Prioridade: {oc['prioridade']}\n")
            arq.write(f"   Próxima ação: {oc['proxima_acao']}\n")

    with open(ARQUIVO_PASSAGEM, "r", encoding="utf-8") as arq:
        print("\n" + arq.read())


def main():
    while True:
        print(f"\n=== {CONTEXTO} ===")
        print("1 - Registrar ocorrência")
        print("2 - Consultar ocorrências")
        print("3 - Registrar anotação no diário")
        print("4 - Consultar diário")
        print("5 - Gerar passagem de plantão")
        print("6 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            registrar_ocorrencia()
        elif opcao == "2":
            consultar_ocorrencias()
        elif opcao == "3":
            registrar_diario()
        elif opcao == "4":
            consultar_diario()
        elif opcao == "5":
            gerar_passagem()
        elif opcao == "6":
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")


main()
