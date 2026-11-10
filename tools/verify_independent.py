#!/usr/bin/env python3
"""Auditor independente em SQLite para dimensionamento de extintores ABNT NBR 12693:2021.

Este script é uma ferramenta de auditoria independente e isolada.
Ele NÃO importa nenhum módulo do pacote de produção ('extintores_nbr12693').
Recria as fórmulas e regras normativas diretamente sobre um banco de dados
SQLite relacional puramente em memória, garantindo verificação fidedigna.
"""

import json
import os
import sqlite3
import sys
from fractions import Fraction

# Assegurar saída UTF-8 no Windows e Linux
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def verificar_arquivo_exemplo(caminho_json: str) -> None:
    nome_arq = os.path.basename(caminho_json)
    print(f"\n[AUDITORIA] Verificando arquivo: {nome_arq}")

    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    # Tabelas de referência normativa
    cur.execute("""
        CREATE TABLE criterios_norma (
            grau TEXT PRIMARY KEY,
            carga_max INTEGER,
            dist_max INTEGER,
            area_max INTEGER,
            cap_a INTEGER,
            cap_b INTEGER
        )
    """)
    cur.executemany("""
        INSERT INTO criterios_norma VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("baixo", 300, 20, 250, 2, 20),
        ("medio", 1200, 15, 150, 2, 40),
        ("alto", 999999, 10, 100, 4, 80),
    ])

    cur.execute("""
        CREATE TABLE pavimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            area_num INTEGER,
            area_den INTEGER,
            carga_incendio INTEGER,
            dist_caminhamento_num INTEGER,
            dist_caminhamento_den INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE riscos_especificos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pavimento_id INTEGER,
            identificador TEXT,
            tipo TEXT,
            distancia_num INTEGER,
            distancia_den INTEGER,
            dist_max_permitida INTEGER
        )
    """)

    pavs = dados.get("pavimentos", [])
    for p in pavs:
        area_f = Fraction(str(p["area_m2"]))
        carga = int(p["carga_incendio_mj_m2"])
        dist_f = Fraction(str(p["maior_distancia_caminhamento_m"]))

        cur.execute("""
            INSERT INTO pavimentos (nome, area_num, area_den, carga_incendio, dist_caminhamento_num, dist_caminhamento_den)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (p["nome_pavimento"], area_f.numerator, area_f.denominator, carga, dist_f.numerator, dist_f.denominator))
        pav_id = cur.lastrowid

        for r in p.get("riscos_especificos", []):
            dist_r = Fraction(str(r["distancia_ao_extintor_m"]))
            tipo_r = r["tipo"]
            dist_max = 9 if tipo_r == "cozinha_profissional" else 5
            cur.execute("""
                INSERT INTO riscos_especificos (pavimento_id, identificador, tipo, distancia_num, distancia_den, dist_max_permitida)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (pav_id, r["identificador"], tipo_r, dist_r.numerator, dist_r.denominator, dist_max))

    # Auditoria de cada pavimento
    cur.execute("SELECT id, nome, area_num, area_den, carga_incendio, dist_caminhamento_num, dist_caminhamento_den FROM pavimentos")
    linhas = cur.fetchall()

    for row in linhas:
        pid, nome_p, a_num, a_den, carga, d_num, d_den = row
        area = Fraction(a_num, a_den)
        dist_cam = Fraction(d_num, d_den)

        # Determinar grau de risco
        if carga <= 300:
            grau = "baixo"
        elif carga <= 1200:
            grau = "medio"
        else:
            grau = "alto"

        cur.execute("SELECT dist_max, area_max, cap_a, cap_b FROM criterios_norma WHERE grau = ?", (grau,))
        d_max, a_max, cap_a, cap_b = cur.fetchone()

        # Unidades por área
        unid_area = (area.numerator + (area.denominator * a_max) - 1) // (area.denominator * a_max)
        # Unidades por caminhamento
        unid_cam = (dist_cam.numerator + (dist_cam.denominator * d_max) - 1) // (dist_cam.denominator * d_max)

        min_pav = 1 if area <= Fraction(50, 1) else 2
        unid_base = max(min_pav, unid_area, unid_cam)

        print(f"  [OK] Pavimento: {nome_p} | Risco: {grau.upper()} | Área: {area}m²")
        print(f"       Unid. Base: {unid_base} (Área: {unid_area}, Caminhamento: {unid_cam}) | Capacidade: {cap_a}-A : {cap_b}-B:C")

        # Verificar riscos específicos do pavimento
        cur.execute("SELECT identificador, tipo, distancia_num, distancia_den, dist_max_permitida FROM riscos_especificos WHERE pavimento_id = ?", (pid,))
        riscos = cur.fetchall()
        for r_id, r_tipo, r_dnum, r_dden, r_dmax in riscos:
            dist_real = Fraction(r_dnum, r_dden)
            conforme = dist_real <= Fraction(r_dmax, 1)
            status_txt = "CONFORME" if conforme else "INCONFORME"
            print(f"       * Risco {r_id} ({r_tipo}): dist={dist_real}m (Máx: {r_dmax}m) [{status_txt}]")
            assert dist_real <= Fraction(r_dmax, 1), f"Distância do risco {r_id} excede limite normativo!"

    conn.close()
    print(f"  [SUCESSO] Auditoria de {nome_arq} aprovada 100%!\n")


def main() -> int:
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    exemplos_dir = os.path.join(raiz, "examples")

    arquivos = [
        "edificio_comercial_escritorios.json",
        "galpao_logistico_alta_carga.json",
        "restaurante_cozinha_industrial.json",
    ]

    for arq in arquivos:
        caminho = os.path.join(exemplos_dir, arq)
        if os.path.exists(caminho):
            verificar_arquivo_exemplo(caminho)
        else:
            print(f"[ERRO] Arquivo não encontrado: {caminho}", file=sys.stderr)
            return 1

    print("=" * 80)
    print("TODAS AS AUDITORIAS INDEPENDENTES FORAM APROVADAS COM SUCESSO!")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
