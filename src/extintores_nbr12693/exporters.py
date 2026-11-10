"""Exportadores técnicos: memorial descritivo, CSV sanitizado e ZIP determinístico."""

import csv
import io
import os
import zipfile
from fractions import Fraction
from typing import Optional

from extintores_nbr12693.codecs import exportar_resultado_json
from extintores_nbr12693.models import ResultadoDimensionamento


def _fmt(val: Fraction, casas: int = 2) -> str:
    """Formata fração para string decimal com número fixo de casas sem IEEE float."""
    num = val.numerator
    den = val.denominator
    if den == 1:
        return f"{num}.0" if casas > 0 else str(num)
    inteiro = num // den
    resto = abs(num % den)
    fator = 10**casas
    frac_parte = (resto * fator + den // 2) // den
    return f"{inteiro}.{frac_parte:0{casas}d}"


def _sanitizar_campo_csv(val: str) -> str:
    """Sanitiza strings contra injeção de fórmulas de planilhas."""
    if val and val[0] in ("=", "+", "-", "@", "\t", "\r"):
        return f"'{val}"
    return val


def gerar_relatorio_texto(res: ResultadoDimensionamento) -> str:
    """Gera memorial descritivo técnico detalhado de proteção por extintores."""
    linhas: list[str] = []
    w = 80
    linhas.append("=" * w)
    linhas.append("    LOFRANO TECNOLOGIA - ENGENHARIA DE SEGURANÇA CONTRA INCÊNDIO")
    linhas.append("    PROTEÇÃO POR EXTINTORES DE INCÊNDIO - ABNT NBR 12693:2021")
    linhas.append("=" * w)
    linhas.append(f"Edificação: {res.nome_edificacao}")
    linhas.append(f"Ocupação:   {res.ocupacao}")
    linhas.append(f"Área Total: {_fmt(res.area_total_m2, 2)} m²")
    linhas.append(f"Extintores: {res.total_extintores_edificacao} unidade(s) no total")
    linhas.append("-" * w)

    linhas.append("1. DISTRIBUIÇÃO E DIMENSIONAMENTO POR PAVIMENTO")
    for idx, p in enumerate(res.pavimentos, start=1):
        linhas.append(f"  [{idx}] {p.nome_pavimento}:")
        linhas.append(f"      - Área: {_fmt(p.area_m2, 2)} m² | Carga de Incêndio: {_fmt(p.carga_incendio_mj_m2, 0)} MJ/m²")
        linhas.append(f"      - Grau de Risco: {p.grau_risco.value.upper()} | Distância Máx. a Caminhar: {_fmt(p.distancia_maxima_caminhar_m, 0)} m")
        linhas.append(f"      - Capacidade Mínima Requerida: {p.capacidade_minima_a}-A : {p.capacidade_minima_b}-B:C")
        linhas.append(f"      - Unidades por Área: {p.unidades_por_area} | Unidades por Caminhamento: {p.unidades_por_caminhamento}")
        linhas.append(f"      - Extintores Polivalentes ABC (Base): {p.extintores_polivalentes_abc_adotados} unid.")
        if p.extintores_especificos_adotados > 0:
            linhas.append(f"      - Extintores de Proteção Específica: {p.extintores_especificos_adotados} unid.")
        linhas.append(f"      - Total no Pavimento: {p.total_extintores_pavimento} unid. (Área média: {_fmt(p.area_media_por_extintor_m2, 1)} m²/unid.)")

        if p.riscos_especificos:
            linhas.append("      - Riscos Específicos Localizados:")
            for r in p.riscos_especificos:
                status_txt = "CONFORME" if r.conforme_distancia else "NÃO CONFORME"
                linhas.append(
                    f"        * {r.identificador} ({r.tipo.value}): d={_fmt(r.distancia_instalada_m, 1)}m "
                    f"(Máx: {_fmt(r.distancia_maxima_permitida_m, 1)}m) [{status_txt}] -> Agente: {r.agente_adotado.value}"
                )
        linhas.append("-" * w)

    linhas.append("2. REQUISITOS DE INSTALAÇÃO E ERGONOMIA (NBR 12693, ITEM 5.4)")
    linhas.append("  - Altura máxima de fixação do suporte de parede: 1,60 m do piso acabado.")
    linhas.append("  - Suportes de piso: base mantida entre 0,10 m e 0,20 m do piso.")
    linhas.append("  - Sinalização de piso: pintura regulamentar de 1,00 m x 1,00 m com borda amarela.")
    linhas.append("  - Sinalização de parede: placa fotoluminescente (NBR 16820) a 1,80 m do piso.")
    linhas.append("-" * w)

    if res.alertas:
        linhas.append("3. ALERTAS E INCONFORMIDADES IDENTIFICADAS")
        for alerta in res.alertas:
            linhas.append(f"  [ALERTA] {alerta}")
        linhas.append("-" * w)

    linhas.append("4. DIRETRIZES TÉCNICAS E RECOMENDAÇÕES NORMATIVAS")
    for rec in res.recomendacoes:
        linhas.append(f"  * {rec}")
    linhas.append("=" * w)
    linhas.append("Emitido via Lofrano Tecnologia - Conforme ABNT NBR 12693:2021")
    linhas.append("=" * w)

    return "\n".join(linhas)


def gerar_csv_sanitizado(res: ResultadoDimensionamento) -> str:
    """Gera resumo tabular estruturado em CSV sanitizado contra injeção de fórmulas."""
    saida = io.StringIO()
    writer = csv.writer(saida, delimiter=";", lineterminator="\n")

    writer.writerow([
        _sanitizar_campo_csv("pavimento"),
        _sanitizar_campo_csv("area_m2"),
        _sanitizar_campo_csv("carga_incendio_mj_m2"),
        _sanitizar_campo_csv("grau_risco"),
        _sanitizar_campo_csv("dist_max_caminhar_m"),
        _sanitizar_campo_csv("capacidade_minima"),
        _sanitizar_campo_csv("extintores_abc"),
        _sanitizar_campo_csv("extintores_especificos"),
        _sanitizar_campo_csv("total_extintores"),
        _sanitizar_campo_csv("area_media_m2_unid"),
    ])

    for p in res.pavimentos:
        writer.writerow([
            _sanitizar_campo_csv(p.nome_pavimento),
            _fmt(p.area_m2, 2),
            _fmt(p.carga_incendio_mj_m2, 0),
            p.grau_risco.value,
            _fmt(p.distancia_maxima_caminhar_m, 0),
            f"{p.capacidade_minima_a}-A : {p.capacidade_minima_b}-B:C",
            str(p.extintores_polivalentes_abc_adotados),
            str(p.extintores_especificos_adotados),
            str(p.total_extintores_pavimento),
            _fmt(p.area_media_por_extintor_m2, 1),
        ])

    return saida.getvalue()


def gerar_pacote_zip(res: ResultadoDimensionamento, caminho_zip: str, svg_conteudo: Optional[str] = None) -> None:
    """Gera pacote determinístico ZIP com O_EXCL, evitando sobrescrita acidental."""
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
    fd = os.open(caminho_zip, flags, 0o644)
    fixed_time = (2026, 1, 1, 0, 0, 0)

    try:
        with open(fd, "wb", closefd=True) as f_out:
            with zipfile.ZipFile(f_out, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                # 1. Memorial descritivo
                txt = gerar_relatorio_texto(res).encode("utf-8")
                zi_txt = zipfile.ZipInfo(filename="memorial_descritivo.txt", date_time=fixed_time)
                zf.writestr(zi_txt, txt)

                # 2. Dados em JSON canônico
                js = exportar_resultado_json(res).encode("utf-8")
                zi_js = zipfile.ZipInfo(filename="dados_extintores.json", date_time=fixed_time)
                zf.writestr(zi_js, js)

                # 3. Planilha CSV sanitizada
                csv_data = gerar_csv_sanitizado(res).encode("utf-8")
                zi_csv = zipfile.ZipInfo(filename="resumo_extintores.csv", date_time=fixed_time)
                zf.writestr(zi_csv, csv_data)

                # 4. Painel vetorial SVG se disponível
                if svg_conteudo:
                    svg_bytes = svg_conteudo.encode("utf-8")
                    zi_svg = zipfile.ZipInfo(filename="painel_esquematico.svg", date_time=fixed_time)
                    zf.writestr(zi_svg, svg_bytes)
    except Exception:
        if os.path.exists(caminho_zip):
            try:
                os.remove(caminho_zip)
            except OSError:
                pass
        raise
