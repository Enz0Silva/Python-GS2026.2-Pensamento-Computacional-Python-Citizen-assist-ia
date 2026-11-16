from base_conhecimento import BaseConhecimento
from assistente import Assistente
import energia
import fila_mutirao


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível carregar a base de conhecimento.")
        print("Verifique o arquivo data/base_conhecimento.json")
        return

    # Melhoria do teste com usuários (16/11): a busca livre também procura nas
    # orientações de energia. Antes, "vale a pena colocar placa solar..." caía
    # na orientação de corte, porque a energia solar só existia no menu 5.
    base_energia = BaseConhecimento("data/energia.json")
    if base_energia.carregar():
        base.orientacoes.extend(base_energia.orientacoes)

    assistente = Assistente("Citizen Assist AI", base)

    # Integrações com outras disciplinas (explicadas no README)
    # Energias Renováveis: orientações calculadas no estudo GS-SERS
    assistente.adicionar_opcao("Orientações de energia (gastar menos na conta)",
                               lambda: energia.menu(assistente))
    # Computer Organization: estado da fila virtual do mutirão, lido pela rede
    assistente.adicionar_opcao("Ver a fila do mutirão (Posto Cidadão)",
                               fila_mutirao.mostrar)
    # Computer Science: a triagem S = A(B + C) + D entra aqui quando o módulo
    # triagem.py estiver pronto. A lógica e os testes são escritos pelo grupo
    # (regra de IA da disciplina).
    # import triagem
    # assistente.adicionar_opcao("Triagem de dívidas", triagem.executar)

    try:
        assistente.executar()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")


if __name__ == "__main__":
    main()
