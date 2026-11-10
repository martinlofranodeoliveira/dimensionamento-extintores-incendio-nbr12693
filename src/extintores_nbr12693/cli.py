"""Interface de Linha de Comando (CLI) para dimensionamento de extintores NBR 12693."""

import argparse
import sys
from typing import Sequence

from extintores_nbr12693 import __version__
from extintores_nbr12693.calculator import dimensionar_extintores_edificacao
from extintores_nbr12693.codecs import carregar_dados_extintores_json, exportar_resultado_json
from extintores_nbr12693.exporters import gerar_csv_sanitizado, gerar_pacote_zip, gerar_relatorio_texto
from extintores_nbr12693.svg_generator import gerar_painel_svg


def _comando_calcular(args: argparse.Namespace) -> int:
    try:
        with open(args.arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as err:
        print(f"Erro ao ler arquivo de entrada: {err}", file=sys.stderr)
        return 1

    try:
        dados = carregar_dados_extintores_json(conteudo)
    except Exception as err:
        print(f"Erro ao processar JSON: {err}", file=sys.stderr)
        return 1

    resultado = dimensionar_extintores_edificacao(dados)

    # Geração do pacote ZIP determinístico se solicitado
    if args.pacote_zip:
        try:
            svg_conteudo = gerar_painel_svg(resultado)
            gerar_pacote_zip(resultado, args.pacote_zip, svg_conteudo)
            print(f"[ZIP] Pacote determinístico gerado com sucesso em '{args.pacote_zip}'")
        except Exception as err:
            print(f"Erro ao gerar pacote ZIP: {err}", file=sys.stderr)
            return 1

    # Formatação da saída solicitada
    formato = args.formato.lower()
    if formato == "json":
        saida_str = exportar_resultado_json(resultado)
    elif formato == "csv":
        saida_str = gerar_csv_sanitizado(resultado)
    elif formato == "svg":
        saida_str = gerar_painel_svg(resultado)
    else:
        saida_str = gerar_relatorio_texto(resultado)

    if args.saida:
        try:
            with open(args.saida, "w", encoding="utf-8") as f:
                f.write(saida_str)
            print(f"[OK] Saída ({formato}) salva com sucesso em '{args.saida}'")
        except Exception as err:
            print(f"Erro ao salvar arquivo de saída: {err}", file=sys.stderr)
            return 1
    else:
        print(saida_str)

    return 0


def _comando_catalogo(args: argparse.Namespace) -> int:
    print("=" * 80)
    print("    LOFRANO TECNOLOGIA - PARÂMETROS NORMATIVOS DA ABNT NBR 12693:2021")
    print("=" * 80)
    print("1. CLASSIFICAÇÃO DE RISCOS (CARGA DE INCÊNDIO ESPECÍFICA 'q')")
    print("  - Risco Baixo:    q <= 300 MJ/m²    | Distância máxima a caminhar: 20 m")
    print("                    Capacidade mínima: 2-A : 20-B:C | Área máx./unid: 250 m²")
    print("  - Risco Médio:    300 < q <= 1200 MJ/m² | Distância máxima a caminhar: 15 m")
    print("                    Capacidade mínima: 2-A : 40-B:C | Área máx./unid: 150 m²")
    print("  - Risco Alto:     q > 1200 MJ/m²    | Distância máxima a caminhar: 10 m")
    print("                    Capacidade mínima: 4-A : 80-B:C | Área máx./unid: 100 m²")
    print("-" * 80)
    print("2. REGRAS GERAIS DE DISTRIBUIÇÃO E COMPARTIMENTAÇÃO")
    print("  - Mínimo de 2 unidades extintoras por pavimento ou compartimento.")
    print("  - Exceção: mezaninos ou áreas <= 50 m² aceitam 1 unidade extintora ABC.")
    print("  - Riscos elétricos (QGBT, transformadores, cabines): extintor a no máx. 5 m.")
    print("  - Líquidos/gases inflamáveis (GLP, depósitos): extintor a no máx. 5 m.")
    print("  - Cozinhas profissionais/comerciais (Classe K): extintor a no máx. 9 m.")
    print("-" * 80)
    print("3. REQUISITOS DE INSTALAÇÃO E ERGONOMIA (ITEM 5.4)")
    print("  - Altura máxima de fixação do suporte de parede: 1,60 m do piso acabado.")
    print("  - Suportes de piso: base mantida entre 0,10 m e 0,20 m do piso acabado.")
    print("  - Sinalização de piso: pintura regulamentar de 1,00 m x 1,00 m (borda amarela).")
    print("  - Sinalização de parede: placa fotoluminescente (NBR 16820) a 1,80 m do piso.")
    print("=" * 80)
    return 0


def _comando_gerar_exemplo(args: argparse.Namespace) -> int:
    exemplo_json = """{
  "nome_edificacao": "Edifício Comercial Centro Empresarial",
  "ocupacao": "Comercial e Serviços",
  "pavimentos": [
    {
      "nome_pavimento": "Térreo - Hall e Acesso",
      "area_m2": 450,
      "carga_incendio_mj_m2": 250,
      "maior_distancia_caminhamento_m": 18,
      "riscos_especificos": [
        {
          "identificador": "QGBT - Entrada Geral",
          "tipo": "quadro_eletrico_geral",
          "distancia_ao_extintor_m": 3,
          "agente_sugerido": "dioxido_carbono_co2"
        }
      ]
    },
    {
      "nome_pavimento": "1º ao 10º Pavimento Tipo",
      "area_m2": 380,
      "carga_incendio_mj_m2": 450,
      "maior_distancia_caminhamento_m": 14,
      "riscos_especificos": []
    }
  ]
}
"""
    if args.saida:
        try:
            with open(args.saida, "w", encoding="utf-8") as f:
                f.write(exemplo_json)
            print(f"[OK] Modelo de exemplo gravado em '{args.saida}'")
        except Exception as err:
            print(f"Erro ao gravar arquivo de exemplo: {err}", file=sys.stderr)
            return 1
    else:
        print(exemplo_json)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Ponto de entrada principal da CLI."""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="extintores-nbr12693",
        description="Dimensionamento de Sistemas de Proteção por Extintores de Incêndio (ABNT NBR 12693:2021) - Lofrano Tecnologia",
        add_help=False,
    )

    parser.add_argument("-h", "--help", "--ajuda", action="help", help="Exibe esta mensagem de ajuda e encerra.")
    parser.add_argument("-v", "--version", "--versao", action="version", version=f"%(prog)s {__version__}", help="Exibe a versão do programa.")

    subparsers = parser.add_subparsers(dest="subcomando", title="Subcomandos Disponíveis")

    # Subcomando 'calcular'
    parser_calc = subparsers.add_parser("calcular", help="Dimensiona a proteção por extintores a partir de arquivo JSON.")
    parser_calc.add_argument("arquivo", help="Caminho do arquivo JSON de entrada.")
    parser_calc.add_argument(
        "--formato",
        choices=["texto", "json", "csv", "svg"],
        default="texto",
        help="Formato de saída dos resultados (padrão: texto).",
    )
    parser_calc.add_argument("--saida", help="Arquivo de destino para salvar a saída.")
    parser_calc.add_argument("--pacote-zip", help="Gera pacote ZIP determinístico completo no caminho especificado.")

    # Subcomando 'catalogo'
    subparsers.add_parser("catalogo", help="Exibe o catálogo de referências e critérios normativos da NBR 12693:2021.")

    # Subcomando 'gerar-exemplo'
    parser_ex = subparsers.add_parser("gerar-exemplo", help="Gera arquivo JSON modelo de exemplo para preenchimento.")
    parser_ex.add_argument("--saida", help="Arquivo de destino para gravar o JSON de exemplo.")

    args = parser.parse_args(argv)

    if not args.subcomando:
        parser.print_help()
        return 0

    if args.subcomando == "calcular":
        return _comando_calcular(args)
    elif args.subcomando == "catalogo":
        return _comando_catalogo(args)
    elif args.subcomando == "gerar-exemplo":
        return _comando_gerar_exemplo(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
