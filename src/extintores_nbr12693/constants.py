"""Constantes e parâmetros normativos da ABNT NBR 12693:2021.

ABNT NBR 12693:2021 - Sistemas de proteção por extintores de incêndio.
Estabelece requisitos para projeto, seleção, instalação e distribuição de extintores
portáteis e sobre rodas para a proteção de edificações e áreas de risco.
"""

from fractions import Fraction
from typing import Final

# Limites de Carga de Incêndio Específica 'q' (MJ/m²) - ABNT NBR 12693 / IT CB
LIMITE_CARGA_INCENDIO_BAIXO_MJ_M2: Final[Fraction] = Fraction(300, 1)    # q <= 300 MJ/m²
LIMITE_CARGA_INCENDIO_MEDIO_MJ_M2: Final[Fraction] = Fraction(1200, 1)   # 300 < q <= 1200 MJ/m²
# q > 1200 MJ/m² -> Risco Alto

# Distâncias máximas a caminhar regulamentares (metros)
DISTANCIA_MAXIMA_CAMINHAR_BAIXO_M: Final[Fraction] = Fraction(20, 1)  # 20 metros
DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M: Final[Fraction] = Fraction(15, 1)  # 15 metros
DISTANCIA_MAXIMA_CAMINHAR_ALTO_M: Final[Fraction] = Fraction(10, 1)   # 10 metros

# Área máxima de proteção por unidade extintora de Classe A (m²)
AREA_MAXIMA_POR_UNIDADE_BAIXO_M2: Final[Fraction] = Fraction(250, 1)  # 250 m²
AREA_MAXIMA_POR_UNIDADE_MEDIO_M2: Final[Fraction] = Fraction(150, 1)  # 150 m²
AREA_MAXIMA_POR_UNIDADE_ALTO_M2: Final[Fraction] = Fraction(100, 1)   # 100 m²

# Capacidade extintora mínima por unidade extintora
CAPACIDADE_MINIMA_A_BAIXO: Final[int] = 2   # 2-A
CAPACIDADE_MINIMA_B_BAIXO: Final[int] = 20  # 20-B

CAPACIDADE_MINIMA_A_MEDIO: Final[int] = 2   # 2-A
CAPACIDADE_MINIMA_B_MEDIO: Final[int] = 40  # 40-B

CAPACIDADE_MINIMA_A_ALTO: Final[int] = 4    # 4-A
CAPACIDADE_MINIMA_B_ALTO: Final[int] = 80   # 80-B

# Quantidade mínima de unidades extintoras por pavimento ou compartimentação
MINIMO_UNIDADES_POR_PAVIMENTO: Final[int] = 2
AREA_LIMITE_MEZANINO_UNIDADE_UNICA_M2: Final[Fraction] = Fraction(50, 1)  # Até 50 m² aceita 1 extintor ABC

# Distâncias máximas de alcance a riscos específicos (metros)
DISTANCIA_MAXIMA_RISCO_ELETRICO_M: Final[Fraction] = Fraction(5, 1)     # Transformadores, QGBT, Subestação
DISTANCIA_MAXIMA_RISCO_LIQUIDO_GAS_M: Final[Fraction] = Fraction(5, 1)  # Depósito inflamáveis, Central GLP
DISTANCIA_MAXIMA_RISCO_COZINHA_K_M: Final[Fraction] = Fraction(9, 1)    # Cozinha profissional (Classe K)

# Requisitos de Instalação e Ergonomia (Item 5.4 da NBR 12693)
ALTURA_MAXIMA_SUPORTE_PAREDE_M: Final[Fraction] = Fraction(16, 10)  # 1.60 m do piso à alça/suporte
ALTURA_MINIMA_BASE_PISO_M: Final[Fraction] = Fraction(1, 10)       # 0.10 m (suporte de piso)
ALTURA_MAXIMA_BASE_PISO_M: Final[Fraction] = Fraction(2, 10)       # 0.20 m (suporte de piso)
ALTURA_SINALIZACAO_FOTOLUMINESCENTE_M: Final[Fraction] = Fraction(18, 10)  # 1.80 m (NBR 16820)

# Dimensões da demarcação de solo regulamentar (metros)
LARGURA_DEMARCACAO_PISO_M: Final[Fraction] = Fraction(1, 1)        # 1.00 m
COMPRIMENTO_DEMARCACAO_PISO_M: Final[Fraction] = Fraction(1, 1)    # 1.00 m
LARGURA_FAIXA_AMARELA_M: Final[Fraction] = Fraction(15, 100)       # 0.15 m
LADO_QUADRADO_VERMELHO_M: Final[Fraction] = Fraction(7, 10)        # 0.70 m
