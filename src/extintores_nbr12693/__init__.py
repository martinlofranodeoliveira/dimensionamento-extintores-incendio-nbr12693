"""Pacote para dimensionamento de sistemas de proteção por extintores de incêndio (ABNT NBR 12693:2021).

Desenvolvido segundo as diretrizes de engenharia de software da Lofrano Tecnologia:
- 100% em português brasileiro (pt-BR);
- Zero dependências externas em tempo de execução;
- Aritmética racional exata (fractions.Fraction) sem IEEE float;
- Codecs JSON RFC 8259 estritos e relatórios com proteção contra injeção CSV.
"""

from extintores_nbr12693.calculator import (
    determinar_grau_risco,
    dimensionar_extintores_edificacao,
    dimensionar_pavimento,
)
from extintores_nbr12693.codecs import (
    carregar_dados_extintores_json,
    exportar_resultado_json,
)
from extintores_nbr12693.constants import (
    AREA_MAXIMA_POR_UNIDADE_ALTO_M2,
    AREA_MAXIMA_POR_UNIDADE_BAIXO_M2,
    AREA_MAXIMA_POR_UNIDADE_MEDIO_M2,
    CAPACIDADE_MINIMA_A_ALTO,
    CAPACIDADE_MINIMA_A_BAIXO,
    CAPACIDADE_MINIMA_A_MEDIO,
    CAPACIDADE_MINIMA_B_ALTO,
    CAPACIDADE_MINIMA_B_BAIXO,
    CAPACIDADE_MINIMA_B_MEDIO,
    DISTANCIA_MAXIMA_CAMINHAR_ALTO_M,
    DISTANCIA_MAXIMA_CAMINHAR_BAIXO_M,
    DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M,
    MINIMO_UNIDADES_POR_PAVIMENTO,
)
from extintores_nbr12693.exporters import (
    gerar_csv_sanitizado,
    gerar_pacote_zip,
    gerar_relatorio_texto,
)
from extintores_nbr12693.models import (
    ClasseFogo,
    DadosEdificacao,
    DadosPavimento,
    GrauRisco,
    ResultadoDimensionamento,
    ResultadoPavimento,
    ResultadoRiscoEspecifico,
    RiscoEspecifico,
    TipoAgenteExtintor,
    TipoRiscoEspecifico,
)
from extintores_nbr12693.svg_generator import gerar_painel_svg

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "determinar_grau_risco",
    "dimensionar_extintores_edificacao",
    "dimensionar_pavimento",
    "carregar_dados_extintores_json",
    "exportar_resultado_json",
    "gerar_relatorio_texto",
    "gerar_csv_sanitizado",
    "gerar_pacote_zip",
    "gerar_painel_svg",
    "ClasseFogo",
    "GrauRisco",
    "TipoAgenteExtintor",
    "TipoRiscoEspecifico",
    "RiscoEspecifico",
    "DadosPavimento",
    "DadosEdificacao",
    "ResultadoRiscoEspecifico",
    "ResultadoPavimento",
    "ResultadoDimensionamento",
    "AREA_MAXIMA_POR_UNIDADE_BAIXO_M2",
    "AREA_MAXIMA_POR_UNIDADE_MEDIO_M2",
    "AREA_MAXIMA_POR_UNIDADE_ALTO_M2",
    "CAPACIDADE_MINIMA_A_BAIXO",
    "CAPACIDADE_MINIMA_A_MEDIO",
    "CAPACIDADE_MINIMA_A_ALTO",
    "CAPACIDADE_MINIMA_B_BAIXO",
    "CAPACIDADE_MINIMA_B_MEDIO",
    "CAPACIDADE_MINIMA_B_ALTO",
    "DISTANCIA_MAXIMA_CAMINHAR_BAIXO_M",
    "DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M",
    "DISTANCIA_MAXIMA_CAMINHAR_ALTO_M",
    "MINIMO_UNIDADES_POR_PAVIMENTO",
]
