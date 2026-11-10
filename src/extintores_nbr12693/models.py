"""Modelos de dados e estruturas imutáveis para proteção por extintores NBR 12693."""

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction


class ClasseFogo(str, Enum):
    """Classificação das classes de fogo segundo o combustível envolvido."""
    CLASSE_A = "A"  # Materiais sólidos combustíveis que deixam resíduos/brasas
    CLASSE_B = "B"  # Líquidos e gases inflamáveis, graxas
    CLASSE_C = "C"  # Equipamentos elétricos energizados
    CLASSE_D = "D"  # Metais pirofóricos e combustíveis
    CLASSE_K = "K"  # Óleos vegetais e gorduras animais em cozinhas profissionais


class GrauRisco(str, Enum):
    """Classificação do grau de risco da edificação ou compartimento."""
    BAIXO = "baixo"    # q <= 300 MJ/m²
    MEDIO = "medio"    # 300 < q <= 1200 MJ/m²
    ALTO = "alto"      # q > 1200 MJ/m²


class TipoAgenteExtintor(str, Enum):
    """Tipologia do agente extintor e capacidade comercial de referência."""
    AGUA_PRESSURIZADA = "agua_pressurizada"         # AP 10L (2-A)
    PO_ABC = "po_quimico_abc"                       # Pó ABC 4kg/6kg (2-A:20-B:C ou 4-A:40-B:C)
    PO_BC = "po_quimico_bc"                         # Pó BC 4kg/6kg (20-B:C ou 40-B:C)
    DIOXIDO_CARBONO = "dioxido_carbono_co2"         # CO2 4kg/6kg (5-B:C)
    ESPUMA_MECANICA = "espuma_mecanica"             # EM 10L (2-A:10-B)
    CLASSE_K_ACETATO = "classe_k_acetato_potassio"  # Acetato de Potássio 6L (1-A:K)


class TipoRiscoEspecifico(str, Enum):
    """Riscos especiais localizados que demandam proteção dedicada."""
    QUADRO_ELETRICO_GERAL = "quadro_eletrico_geral"
    CABINE_SUBESTACAO = "cabine_subestacao"
    GERADOR_ENERGIA = "gerador_energia"
    CENTRAL_GLP = "central_glp"
    DEPOSITO_INFLAMAVEIS = "deposito_inflamaveis"
    COZINHA_PROFISSIONAL = "cozinha_profissional"
    CASA_BOMBAS = "casa_bombas"


@dataclass(frozen=True)
class RiscoEspecifico:
    """Parâmetros de um risco especial localizado."""
    identificador: str
    tipo: TipoRiscoEspecifico
    distancia_ao_extintor_m: Fraction
    agente_sugerido: TipoAgenteExtintor

    def __post_init__(self) -> None:
        if not self.identificador or not self.identificador.strip():
            raise ValueError("O identificador do risco específico não pode ser vazio.")
        if self.distancia_ao_extintor_m < Fraction(0, 1):
            raise ValueError(f"Distância ao extintor ({self.distancia_ao_extintor_m}m) não pode ser negativa.")


@dataclass(frozen=True)
class DadosPavimento:
    """Dados arquitetônicos e de carga de incêndio de um pavimento."""
    nome_pavimento: str
    area_m2: Fraction
    carga_incendio_mj_m2: Fraction
    maior_distancia_caminhamento_m: Fraction
    riscos_especificos: tuple[RiscoEspecifico, ...] = ()

    def __post_init__(self) -> None:
        if not self.nome_pavimento or not self.nome_pavimento.strip():
            raise ValueError("O nome do pavimento não pode ser vazio.")
        if self.area_m2 <= Fraction(0, 1):
            raise ValueError(f"Área do pavimento ({self.area_m2}m²) deve ser estritamente positiva.")
        if self.carga_incendio_mj_m2 < Fraction(0, 1):
            raise ValueError(f"Carga de incêndio ({self.carga_incendio_mj_m2} MJ/m²) não pode ser negativa.")
        if self.maior_distancia_caminhamento_m <= Fraction(0, 1):
            raise ValueError(f"Maior distância a caminhar ({self.maior_distancia_caminhamento_m}m) deve ser positiva.")


@dataclass(frozen=True)
class DadosEdificacao:
    """Conjunto completo de dados da edificação para dimensionamento NBR 12693."""
    nome_edificacao: str
    ocupacao: str
    pavimentos: tuple[DadosPavimento, ...]

    def __post_init__(self) -> None:
        if not self.nome_edificacao or not self.nome_edificacao.strip():
            raise ValueError("O nome da edificação não pode ser vazio.")
        if not self.ocupacao or not self.ocupacao.strip():
            raise ValueError("A ocupação da edificação não pode ser vazia.")
        if not self.pavimentos:
            raise ValueError("A edificação deve conter ao menos um pavimento cadastrado.")


@dataclass(frozen=True)
class ResultadoRiscoEspecifico:
    """Conformidade normativa de proteção a um risco específico localizado."""
    identificador: str
    tipo: TipoRiscoEspecifico
    distancia_instalada_m: Fraction
    distancia_maxima_permitida_m: Fraction
    conforme_distancia: bool
    agente_adotado: TipoAgenteExtintor


@dataclass(frozen=True)
class ResultadoPavimento:
    """Dimensionamento técnico e distribuição de extintores por pavimento."""
    nome_pavimento: str
    area_m2: Fraction
    carga_incendio_mj_m2: Fraction
    grau_risco: GrauRisco
    distancia_maxima_caminhar_m: Fraction
    capacidade_minima_a: int
    capacidade_minima_b: int
    unidades_por_area: int
    unidades_por_caminhamento: int
    unidades_minimas_adotadas: int
    extintores_polivalentes_abc_adotados: int
    extintores_especificos_adotados: int
    total_extintores_pavimento: int
    area_media_por_extintor_m2: Fraction
    riscos_especificos: tuple[ResultadoRiscoEspecifico, ...]


@dataclass(frozen=True)
class ResultadoDimensionamento:
    """Resultado técnico consolidado do sistema de extintores NBR 12693:2021."""
    nome_edificacao: str
    ocupacao: str
    area_total_m2: Fraction
    total_extintores_edificacao: int
    pavimentos: tuple[ResultadoPavimento, ...]
    alertas: tuple[str, ...]
    recomendacoes: tuple[str, ...]
