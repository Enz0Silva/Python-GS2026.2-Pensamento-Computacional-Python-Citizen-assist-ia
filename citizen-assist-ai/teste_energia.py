"""Confere se o módulo de energia reproduz os números do estudo GS-SERS.

Uso: python teste_energia.py
"""
from base_conhecimento import BaseConhecimento
import energia

# Cenário do estudo: chuveiro de 5.500 W, 30 min por dia na casa, redução de 20%
r = energia.calcular_economia_banho(5500, 30, 6)
assert r["antes_kwh"] == 82.5, r            # notebook 01: 82,50 kWh/mês
assert r["depois_kwh"] == 66.0, r           # notebook 02: 66,00 kWh/mês
assert r["economia_kwh_mes"] == 16.5, r     # 16,50 kWh/mês
assert r["economia_reais_ano"] == 156.3, r  # R$ 156,30 por ano

# Sem redução, a economia é zero
assert energia.calcular_economia_banho(5500, 30, 0)["economia_kwh_mes"] == 0

# As 3 orientações de energia carregam com os 9 campos da base principal
base = BaseConhecimento("data/energia.json")
assert base.carregar()
assert [o.id for o in base.orientacoes] == ["EN01", "EN02", "EN03"]
for o in base.orientacoes:
    assert len(o.palavras_chave) >= 3 and o.fonte and o.verificado_em

# A pergunta da alteração ao vivo do vídeo continua sem resposta aqui também
assert base.buscar("minha luz foi desligada") == []

# Melhoria do teste com usuários: a busca livre (base principal + energia)
# leva a pergunta sobre placa solar à EN03, e "desligada" continua sem resposta
completa = BaseConhecimento("data/base_conhecimento.json")
assert completa.carregar()
completa.orientacoes.extend(base.orientacoes)
melhor = completa.buscar("Vale a pena colocar placa solar para quem está com a conta atrasada?")[0]
assert melhor[1].id == "EN03", melhor
assert all(p < 3 for p, _ in completa.buscar("minha luz foi desligada"))

print("Todos os testes de energia passaram!")