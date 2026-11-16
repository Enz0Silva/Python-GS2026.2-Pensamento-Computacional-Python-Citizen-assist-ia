"""Orientações de energia do Citizen Assist AI.

Contribuição da disciplina Soluções em Energias Renováveis e Sustentáveis (SERS).
Os números vêm do estudo do grupo no repositório GS-SERS (notebooks 01, 02 e 03):
casa de 4 pessoas em São Paulo, 150,4 kWh por mês, tarifa B1 da Enel SP
(TUSD + TE = R$ 0,78938/kWh, vigência 04/07/2026 a 03/07/2027, dados da ANEEL).

Este módulo reaproveita as classes do assistente: as orientações ficam em
data/energia.json, no mesmo formato da base principal, e são carregadas por
uma BaseConhecimento própria. Cada consulta é registrada no histórico com
origem "energia", então entra nos indicadores e no CSV.
"""
import time

from base_conhecimento import BaseConhecimento

TARIFA_REFERENCIA = 0.78938      # R$/kWh, TUSD + TE, sem tributos nem bandeiras
POTENCIA_PADRAO_W = 5500         # chuveiro do estudo
DIAS_NO_MES = 30


def consumo_chuveiro_kwh_mes(potencia_w, minutos_por_dia):
    """Energia do chuveiro no mês: potência (kW) x horas por dia x 30 dias."""
    return potencia_w / 1000 * minutos_por_dia / 60 * DIAS_NO_MES


def calcular_economia_banho(potencia_w, minutos_hoje, minutos_reduzidos):
    """Devolve um dicionário com consumo atual, consumo novo e economia."""
    antes = consumo_chuveiro_kwh_mes(potencia_w, minutos_hoje)
    depois = consumo_chuveiro_kwh_mes(potencia_w, minutos_hoje - minutos_reduzidos)
    economia = antes - depois
    return {
        "antes_kwh": round(antes, 1),
        "depois_kwh": round(depois, 1),
        "economia_kwh_mes": round(economia, 1),
        "economia_reais_mes": round(economia * TARIFA_REFERENCIA, 2),
        "economia_reais_ano": round(economia * TARIFA_REFERENCIA * 12, 2),
    }


def _br(valor, casas=1):
    """Número no formato brasileiro: 1234.5 -> 1.234,5"""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def _calculadora_banho(assistente):
    inicio = time.time()
    print("\n=== Quanto o banho mais curto economiza ===")
    print("Não precisa informar nenhum dado pessoal. Digite 0 para voltar.")
    minutos = assistente._ler_numero(
        "Minutos de chuveiro ligado por dia, somando todos da casa (1 a 600): ",
        0, 600)
    if minutos == 0:
        return
    while True:
        texto = input("Potência do chuveiro em watts, na etiqueta "
                      f"(Enter = {POTENCIA_PADRAO_W}): ").strip()
        if texto == "":
            potencia = POTENCIA_PADRAO_W
            break
        if texto.isdigit() and 1000 <= int(texto) <= 9000:
            potencia = int(texto)
            break
        print("Valor inválido. Digite um número de 1000 a 9000 ou só Enter.")
    reduzir = assistente._ler_numero(
        f"Quantos minutos por dia a casa pode reduzir (0 a {minutos})? ",
        0, minutos)
    r = calcular_economia_banho(potencia, minutos, reduzir)
    print(f"\nHoje o chuveiro gasta cerca de {_br(r['antes_kwh'])} kWh por mês.")
    print(f"Com {reduzir} minutos a menos por dia: {_br(r['depois_kwh'])} kWh por mês.")
    print(f"Economia estimada: {_br(r['economia_kwh_mes'])} kWh por mês, "
          f"cerca de R$ {_br(r['economia_reais_mes'], 2)} por mês "
          f"(R$ {_br(r['economia_reais_ano'], 2)} por ano).")
    print("Conta feita com a tarifa da Enel SP sem impostos (R$ 0,78938/kWh). "
          "Na sua distribuidora o valor muda, e a economia não é garantida.")
    print("Fonte: estudo do grupo GS-SERS (notebook 02) com tarifa da ANEEL.")
    print("Aviso: este assistente NÃO é um canal oficial.")
    ajudou = assistente._ler_sim_nao("\nEsse cálculo ajudou? (S/N): ")
    assistente.registrar("energia", "calculadora do banho", "EN02", True,
                         ajudou, 1, round(time.time() - inicio, 1))


def menu(assistente, caminho="data/energia.json"):
    """Tela de energia, ligada ao menu principal pelo main.py."""
    base = BaseConhecimento(caminho)
    if not base.carregar():
        print("As orientações de energia não estão disponíveis agora.")
        return
    orientacoes = base.orientacoes
    while True:
        print("\n=== Energia: gastar menos na conta ===")
        print("Estimativas do estudo do grupo, não da sua conta real.")
        for numero, orientacao in enumerate(orientacoes, start=1):
            print(f" {numero}. {orientacao.titulo}")
        calc = len(orientacoes) + 1
        print(f" {calc}. Calcular a economia do banho na minha casa")
        print(" 0. Voltar")
        escolha = assistente._ler_numero("Escolha uma opção: ", 0, calc)
        if escolha == 0:
            return
        if escolha == calc:
            _calculadora_banho(assistente)
            continue
        inicio = time.time()
        orientacao = orientacoes[escolha - 1]
        print()
        orientacao.exibir()
        ajudou = assistente._ler_sim_nao(
            "\nEssa orientação respondeu sua dúvida? (S/N): ")
        assistente.registrar("energia", orientacao.titulo, orientacao.id,
                             True, ajudou, 1, round(time.time() - inicio, 1))
