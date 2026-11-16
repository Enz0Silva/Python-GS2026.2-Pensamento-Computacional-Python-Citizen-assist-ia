"""Consulta a fila virtual do mutirão (integração com Computer Organization).

A fila virtual roda num servidor separado (repositório fila-virtual-citizen-assist).
Este módulo só lê o estado pela rede, com a biblioteca padrão (urllib), e
mostra ao cidadão quantas pessoas estão esperando e a espera estimada.
Se o servidor estiver desligado, o assistente avisa e continua funcionando.
"""
import json
from urllib.error import URLError
from urllib.request import urlopen

ENDERECO = "http://127.0.0.1:5000/api/estado"


def consultar(endereco=ENDERECO, tempo_limite=2):
    """Devolve o dicionário do estado da fila ou None se não conectar."""
    try:
        with urlopen(endereco, timeout=tempo_limite) as resposta:
            return json.loads(resposta.read().decode("utf-8"))
    except (URLError, OSError, ValueError):
        return None


def mostrar():
    estado = consultar()
    print("\n=== Fila do mutirão (Posto Cidadão) ===")
    if estado is None:
        print("A fila virtual não está disponível agora. "
              "Tente mais tarde ou confira no próprio posto.")
        return
    print(f"Pessoas esperando: {estado['na_fila']}")
    print(f"Atendimentos concluídos hoje: {estado['atendidos']}")
    espera = estado.get("espera_nova_senha_min")
    if espera is not None:
        print(f"Quem pegar senha agora espera cerca de {espera:.0f} minutos "
              f"(estimativa por {estado.get('metodo_principal', 'regressão linear')}).")
    print(f"Senhas restantes hoje: {estado['senhas_restantes']}")
    print("A espera é uma estimativa e pode mudar. "
          "Este assistente NÃO é um canal oficial.")
