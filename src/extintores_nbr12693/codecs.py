"""Codec JSON canônico RFC 8259 para dimensionamento de extintores NBR 12693:2021."""

import json
from enum import Enum
from fractions import Fraction
from typing import Any

from extintores_nbr12693.models import (
    DadosEdificacao,
    DadosPavimento,
    ResultadoDimensionamento,
    RiscoEspecifico,
    TipoAgenteExtintor,
    TipoRiscoEspecifico,
)


def _rejeitar_float(valor: str) -> None:
    raise ValueError(f"Ponto flutuante ({valor}) não é permitido. Utilize inteiros ou strings decimais exatas.")


def _rejeitar_chaves_duplicadas(pares: list[tuple[str, Any]]) -> dict[str, Any]:
    resultado: dict[str, Any] = {}
    for chave, valor in pares:
        if chave in resultado:
            raise ValueError(f"Chave duplicada encontrada no JSON: '{chave}'")
        resultado[chave] = valor
    return resultado


def _verificar_profundidade(obj: Any, profundidade: int = 1, limite: int = 32) -> None:
    if profundidade > limite:
        raise ValueError(f"Profundidade da estrutura JSON ({profundidade}) excede o limite máximo permitido de {limite}.")
    if isinstance(obj, dict):
        for v in obj.values():
            _verificar_profundidade(v, profundidade + 1, limite)
    elif isinstance(obj, list):
        for elem in obj:
            _verificar_profundidade(elem, profundidade + 1, limite)


def _para_fracao(val: Any) -> Fraction:
    if isinstance(val, (int, str)):
        return Fraction(val)
    if isinstance(val, Fraction):
        return val
    raise ValueError(f"Tipo inválido para conversão fracionária: {type(val).__name__} ({val})")


def carregar_dados_extintores_json(conteudo: str) -> DadosEdificacao:
    """Carrega e valida os dados de extintores em JSON canônico sem float."""
    if conteudo.startswith(("\ufeff", "\xef\xbb\xbf")):
        raise ValueError("Byte Order Mark (BOM) detectado. O arquivo deve ser codificado estritamente em UTF-8 puro.")

    try:
        dados = json.loads(
            conteudo,
            object_pairs_hook=_rejeitar_chaves_duplicadas,
            parse_float=_rejeitar_float,
        )
    except json.JSONDecodeError as err:
        raise ValueError(f"Erro de decodificação JSON: {err}") from err

    _verificar_profundidade(dados)

    if not isinstance(dados, dict):
        raise ValueError("O JSON raiz deve ser um objeto dicionário.")

    nome = str(dados.get("nome_edificacao", "Edifício"))
    ocupacao = str(dados.get("ocupacao", "Comercial / Serviços"))

    lista_pavs_raw = dados.get("pavimentos", [])
    if not isinstance(lista_pavs_raw, list):
        raise ValueError("O campo 'pavimentos' deve ser uma lista.")

    pavimentos_parsed: list[DadosPavimento] = []
    for idx, p_dict in enumerate(lista_pavs_raw):
        if not isinstance(p_dict, dict):
            raise ValueError(f"Pavimento no índice {idx} deve ser um dicionário.")

        nome_p = str(p_dict.get("nome_pavimento", f"Pavimento {idx + 1}"))
        area = _para_fracao(p_dict.get("area_m2", "100.0"))
        carga_inc = _para_fracao(p_dict.get("carga_incendio_mj_m2", "300"))
        dist_cam = _para_fracao(p_dict.get("maior_distancia_caminhamento_m", "15.0"))

        riscos_raw = p_dict.get("riscos_especificos", [])
        if not isinstance(riscos_raw, list):
            raise ValueError(f"Campo 'riscos_especificos' no pavimento '{nome_p}' deve ser uma lista.")

        riscos_parsed: list[RiscoEspecifico] = []
        for r_idx, r_dict in enumerate(riscos_raw):
            if not isinstance(r_dict, dict):
                raise ValueError(f"Risco específico {r_idx} no pavimento '{nome_p}' deve ser um dicionário.")

            r_id = str(r_dict.get("identificador", f"Risco {r_idx + 1}"))
            r_tipo_str = str(r_dict.get("tipo", "quadro_eletrico_geral")).lower()
            try:
                r_tipo = TipoRiscoEspecifico(r_tipo_str)
            except ValueError:
                r_tipo = TipoRiscoEspecifico.QUADRO_ELETRICO_GERAL

            r_dist = _para_fracao(r_dict.get("distancia_ao_extintor_m", "3.0"))
            r_agente_str = str(r_dict.get("agente_sugerido", "dioxido_carbono_co2")).lower()
            try:
                r_agente = TipoAgenteExtintor(r_agente_str)
            except ValueError:
                r_agente = TipoAgenteExtintor.DIOXIDO_CARBONO

            riscos_parsed.append(
                RiscoEspecifico(
                    identificador=r_id,
                    tipo=r_tipo,
                    distancia_ao_extintor_m=r_dist,
                    agente_sugerido=r_agente,
                )
            )

        pavimentos_parsed.append(
            DadosPavimento(
                nome_pavimento=nome_p,
                area_m2=area,
                carga_incendio_mj_m2=carga_inc,
                maior_distancia_caminhamento_m=dist_cam,
                riscos_especificos=tuple(riscos_parsed),
            )
        )

    return DadosEdificacao(
        nome_edificacao=nome,
        ocupacao=ocupacao,
        pavimentos=tuple(pavimentos_parsed),
    )


def _serializar_valor(val: Any) -> Any:
    if isinstance(val, Fraction):
        if val.denominator == 1:
            return val.numerator
        return f"{val.numerator}/{val.denominator}"
    if isinstance(val, Enum):
        return val.value
    if isinstance(val, tuple):
        return [_serializar_valor(x) for x in val]
    if isinstance(val, dict):
        return {k: _serializar_valor(v) for k, v in val.items()}
    return val


def exportar_resultado_json(res: ResultadoDimensionamento) -> str:
    """Serializa o resultado em JSON canônico RFC 8259 determinístico."""
    dados: dict[str, Any] = {
        "norma": "ABNT NBR 12693:2021",
        "nome_edificacao": res.nome_edificacao,
        "ocupacao": res.ocupacao,
        "area_total_m2": _serializar_valor(res.area_total_m2),
        "total_extintores_edificacao": res.total_extintores_edificacao,
        "pavimentos": [
            {
                "nome_pavimento": p.nome_pavimento,
                "area_m2": _serializar_valor(p.area_m2),
                "carga_incendio_mj_m2": _serializar_valor(p.carga_incendio_mj_m2),
                "grau_risco": p.grau_risco.value,
                "distancia_maxima_caminhar_m": _serializar_valor(p.distancia_maxima_caminhar_m),
                "capacidade_minima_a": p.capacidade_minima_a,
                "capacidade_minima_b": p.capacidade_minima_b,
                "unidades_por_area": p.unidades_por_area,
                "unidades_por_caminhamento": p.unidades_por_caminhamento,
                "unidades_minimas_adotadas": p.unidades_minimas_adotadas,
                "extintores_polivalentes_abc": p.extintores_polivalentes_abc_adotados,
                "extintores_especificos": p.extintores_especificos_adotados,
                "total_extintores_pavimento": p.total_extintores_pavimento,
                "area_media_por_extintor_m2": _serializar_valor(p.area_media_por_extintor_m2),
                "riscos_especificos": [
                    {
                        "identificador": r.identificador,
                        "tipo": r.tipo.value,
                        "distancia_instalada_m": _serializar_valor(r.distancia_instalada_m),
                        "distancia_maxima_permitida_m": _serializar_valor(r.distancia_maxima_permitida_m),
                        "conforme_distancia": r.conforme_distancia,
                        "agente_adotado": r.agente_adotado.value,
                    }
                    for r in p.riscos_especificos
                ],
            }
            for p in res.pavimentos
        ],
        "alertas": list(res.alertas),
        "recomendacoes": list(res.recomendacoes),
    }

    return json.dumps(dados, ensure_ascii=False, indent=2, sort_keys=True)
