"""Motor de cálculo normativo para dimensionamento de extintores ABNT NBR 12693:2021."""

from fractions import Fraction
from extintores_nbr12693.constants import (
    ALTURA_MAXIMA_SUPORTE_PAREDE_M,
    ALTURA_MINIMA_BASE_PISO_M,
    ALTURA_SINALIZACAO_FOTOLUMINESCENTE_M,
    AREA_LIMITE_MEZANINO_UNIDADE_UNICA_M2,
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
    DISTANCIA_MAXIMA_RISCO_COZINHA_K_M,
    DISTANCIA_MAXIMA_RISCO_ELETRICO_M,
    DISTANCIA_MAXIMA_RISCO_LIQUIDO_GAS_M,
    LIMITE_CARGA_INCENDIO_BAIXO_MJ_M2,
    LIMITE_CARGA_INCENDIO_MEDIO_MJ_M2,
    MINIMO_UNIDADES_POR_PAVIMENTO,
)
from extintores_nbr12693.models import (
    DadosEdificacao,
    DadosPavimento,
    GrauRisco,
    ResultadoDimensionamento,
    ResultadoPavimento,
    ResultadoRiscoEspecifico,
    TipoAgenteExtintor,
    TipoRiscoEspecifico,
)


def _teto_fracao(frac: Fraction) -> int:
    """Calcula o teto inteiro exato de uma fração sem converter para float."""
    if frac.denominator == 1:
        return frac.numerator
    if frac.numerator > 0:
        return (frac.numerator // frac.denominator) + 1
    return frac.numerator // frac.denominator


def determinar_grau_risco(carga_incendio_mj_m2: Fraction) -> GrauRisco:
    """Classifica o grau de risco conforme a carga de incêndio específica."""
    if carga_incendio_mj_m2 <= LIMITE_CARGA_INCENDIO_BAIXO_MJ_M2:
        return GrauRisco.BAIXO
    elif carga_incendio_mj_m2 <= LIMITE_CARGA_INCENDIO_MEDIO_MJ_M2:
        return GrauRisco.MEDIO
    return GrauRisco.ALTO


def obter_distancia_maxima_risco_especifico(tipo: TipoRiscoEspecifico) -> Fraction:
    """Retorna a distância máxima regulamentar entre o risco específico e o extintor."""
    if tipo in (
        TipoRiscoEspecifico.QUADRO_ELETRICO_GERAL,
        TipoRiscoEspecifico.CABINE_SUBESTACAO,
        TipoRiscoEspecifico.GERADOR_ENERGIA,
        TipoRiscoEspecifico.CASA_BOMBAS,
    ):
        return DISTANCIA_MAXIMA_RISCO_ELETRICO_M  # 5 metros
    elif tipo in (
        TipoRiscoEspecifico.CENTRAL_GLP,
        TipoRiscoEspecifico.DEPOSITO_INFLAMAVEIS,
    ):
        return DISTANCIA_MAXIMA_RISCO_LIQUIDO_GAS_M  # 5 metros
    elif tipo == TipoRiscoEspecifico.COZINHA_PROFISSIONAL:
        return DISTANCIA_MAXIMA_RISCO_COZINHA_K_M  # 9 metros
    return DISTANCIA_MAXIMA_RISCO_ELETRICO_M


def dimensionar_pavimento(pav: DadosPavimento, alertas: list[str]) -> ResultadoPavimento:
    """Executa o dimensionamento da proteção por extintores em um pavimento."""
    grau_risco = determinar_grau_risco(pav.carga_incendio_mj_m2)

    if grau_risco == GrauRisco.BAIXO:
        dist_max_caminhar = DISTANCIA_MAXIMA_CAMINHAR_BAIXO_M
        area_max_unidade = AREA_MAXIMA_POR_UNIDADE_BAIXO_M2
        cap_a = CAPACIDADE_MINIMA_A_BAIXO
        cap_b = CAPACIDADE_MINIMA_B_BAIXO
    elif grau_risco == GrauRisco.MEDIO:
        dist_max_caminhar = DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M
        area_max_unidade = AREA_MAXIMA_POR_UNIDADE_MEDIO_M2
        cap_a = CAPACIDADE_MINIMA_A_MEDIO
        cap_b = CAPACIDADE_MINIMA_B_MEDIO
    else:
        dist_max_caminhar = DISTANCIA_MAXIMA_CAMINHAR_ALTO_M
        area_max_unidade = AREA_MAXIMA_POR_UNIDADE_ALTO_M2
        cap_a = CAPACIDADE_MINIMA_A_ALTO
        cap_b = CAPACIDADE_MINIMA_B_ALTO

    # 1. Unidades por área
    unidades_por_area = _teto_fracao(pav.area_m2 / area_max_unidade)

    # 2. Unidades por caminhamento
    unidades_por_caminhamento = _teto_fracao(pav.maior_distancia_caminhamento_m / dist_max_caminhar)

    # 3. Mínimo regulamentar por pavimento
    if pav.area_m2 <= AREA_LIMITE_MEZANINO_UNIDADE_UNICA_M2:
        minimo_pavimento = 1
    else:
        minimo_pavimento = MINIMO_UNIDADES_POR_PAVIMENTO

    unidades_adotadas = max(minimo_pavimento, unidades_por_area, unidades_por_caminhamento)

    # Alerta caso o caminhamento exceda a distância máxima com apenas 1 unidade
    if pav.maior_distancia_caminhamento_m > dist_max_caminhar and unidades_adotadas <= 1:
        alertas.append(
            f"Pavimento '{pav.nome_pavimento}': caminhamento de {pav.maior_distancia_caminhamento_m}m excede "
            f"o limite normativo de {dist_max_caminhar}m para risco {grau_risco.value}. Aumentada a proteção."
        )
        unidades_adotadas = max(unidades_adotadas, 2)

    # 4. Avaliação dos riscos específicos
    resultados_especificos: list[ResultadoRiscoEspecifico] = []
    extintores_adicionais_especificos = 0

    for risco in pav.riscos_especificos:
        dist_max_permitida = obter_distancia_maxima_risco_especifico(risco.tipo)
        conforme = risco.distancia_ao_extintor_m <= dist_max_permitida

        if not conforme:
            alertas.append(
                f"Risco específico '{risco.identificador}' ({risco.tipo.value}) no pavimento '{pav.nome_pavimento}': "
                f"distância instalada ({risco.distancia_ao_extintor_m}m) excede o limite máximo permitido de {dist_max_permitida}m."
            )

        resultados_especificos.append(
            ResultadoRiscoEspecifico(
                identificador=risco.identificador,
                tipo=risco.tipo,
                distancia_instalada_m=risco.distancia_ao_extintor_m,
                distancia_maxima_permitida_m=dist_max_permitida,
                conforme_distancia=conforme,
                agente_adotado=risco.agente_sugerido,
            )
        )
        extintores_adicionais_especificos += 1

    total_extintores = unidades_adotadas + extintores_adicionais_especificos
    area_media = pav.area_m2 / Fraction(total_extintores, 1)

    return ResultadoPavimento(
        nome_pavimento=pav.nome_pavimento,
        area_m2=pav.area_m2,
        carga_incendio_mj_m2=pav.carga_incendio_mj_m2,
        grau_risco=grau_risco,
        distancia_maxima_caminhar_m=dist_max_caminhar,
        capacidade_minima_a=cap_a,
        capacidade_minima_b=cap_b,
        unidades_por_area=unidades_por_area,
        unidades_por_caminhamento=unidades_por_caminhamento,
        unidades_minimas_adotadas=unidades_adotadas,
        extintores_polivalentes_abc_adotados=unidades_adotadas,
        extintores_especificos_adotados=extintores_adicionais_especificos,
        total_extintores_pavimento=total_extintores,
        area_media_por_extintor_m2=area_media,
        riscos_especificos=tuple(resultados_especificos),
    )


def dimensionar_extintores_edificacao(dados: DadosEdificacao) -> ResultadoDimensionamento:
    """Realiza o dimensionamento técnico completo do sistema de extintores NBR 12693:2021."""
    alertas: list[str] = []
    recomendacoes: list[str] = []

    res_pavimentos: list[ResultadoPavimento] = []
    area_total = Fraction(0, 1)
    total_extintores_global = 0

    for pav in dados.pavimentos:
        res_pav = dimensionar_pavimento(pav, alertas)
        res_pavimentos.append(res_pav)
        area_total += pav.area_m2
        total_extintores_global += res_pav.total_extintores_pavimento

    # Recomendações técnicas de engenharia
    recomendacoes.append(
        "Instalação dos extintores: altura máxima do suporte/alça a 1,60 m do piso acabado (Item 5.4.1 da ABNT NBR 12693:2021)."
    )
    recomendacoes.append(
        "Extintores sobre suporte de piso: base mantida entre 0,10 m e 0,20 m acima do piso acabado."
    )
    recomendacoes.append(
        "Sinalização de solo: demarcação obrigatória com quadrado de 1,00 m x 1,00 m, borda amarela de 0,15 m e campo central vermelho de 0,70 m x 0,70 m."
    )
    recomendacoes.append(
        "Sinalização de parede: placa de identificação fotoluminescente regulamentar (ABNT NBR 16820) fixada a 1,80 m do piso sobre o equipamento."
    )
    recomendacoes.append(
        "Inspeção e manutenção: inspeção visual mensal (nível 1), manutenção semestral/anual (nível 2) e ensaio hidrostático a cada 5 anos (nível 3) conforme NBR 12962 / NBR 13485."
    )

    return ResultadoDimensionamento(
        nome_edificacao=dados.nome_edificacao,
        ocupacao=dados.ocupacao,
        area_total_m2=area_total,
        total_extintores_edificacao=total_extintores_global,
        pavimentos=tuple(res_pavimentos),
        alertas=tuple(alertas),
        recomendacoes=tuple(recomendacoes),
    )
