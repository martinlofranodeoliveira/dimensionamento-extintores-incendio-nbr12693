"""Testes unitários dos exportadores da NBR 12693."""

import os
import tempfile
import unittest
from fractions import Fraction

from extintores_nbr12693.calculator import dimensionar_extintores_edificacao
from extintores_nbr12693.exporters import (
    _fmt,
    _sanitizar_campo_csv,
    gerar_csv_sanitizado,
    gerar_pacote_zip,
    gerar_relatorio_texto,
)
from extintores_nbr12693.models import DadosEdificacao, DadosPavimento


class TestExporters(unittest.TestCase):
    """Testa memorial de cálculo, CSV sanitizado e ZIP determinístico."""

    def setUp(self) -> None:
        pav = DadosPavimento(
            nome_pavimento="Térreo Corporativo",
            area_m2=Fraction(400, 1),
            carga_incendio_mj_m2=Fraction(300, 1),
            maior_distancia_caminhamento_m=Fraction(15, 1),
        )
        self.dados = DadosEdificacao(
            nome_edificacao="Empresarial Sul",
            ocupacao="Serviços",
            pavimentos=(pav,),
        )
        self.resultado = dimensionar_extintores_edificacao(self.dados)

    def test_fmt_sem_float(self) -> None:
        self.assertEqual(_fmt(Fraction(10, 1), 2), "10.0")
        self.assertEqual(_fmt(Fraction(10, 1), 0), "10")
        self.assertEqual(_fmt(Fraction(1, 2), 2), "0.50")
        self.assertEqual(_fmt(Fraction(1, 3), 2), "0.33")

    def test_sanitizar_campo_csv(self) -> None:
        self.assertEqual(_sanitizar_campo_csv("Normal"), "Normal")
        self.assertEqual(_sanitizar_campo_csv("=1+1"), "'=1+1")
        self.assertEqual(_sanitizar_campo_csv("+123"), "'+123")
        self.assertEqual(_sanitizar_campo_csv("-123"), "'-123")
        self.assertEqual(_sanitizar_campo_csv("@cmd"), "'@cmd")
        self.assertEqual(_sanitizar_campo_csv("\ttab"), "'\ttab")

    def test_gerar_relatorio_texto(self) -> None:
        txt = gerar_relatorio_texto(self.resultado)
        self.assertIn("LOFRANO TECNOLOGIA", txt)
        self.assertIn("ABNT NBR 12693:2021", txt)
        self.assertIn("Empresarial Sul", txt)
        self.assertIn("Térreo Corporativo", txt)
        self.assertIn("1. DISTRIBUIÇÃO E DIMENSIONAMENTO POR PAVIMENTO", txt)
        self.assertIn("2. REQUISITOS DE INSTALAÇÃO E ERGONOMIA", txt)

    def test_gerar_csv_sanitizado(self) -> None:
        csv_str = gerar_csv_sanitizado(self.resultado)
        self.assertIn("pavimento;area_m2;carga_incendio_mj_m2;grau_risco", csv_str)
        self.assertIn("Térreo Corporativo", csv_str)

    def test_gerar_pacote_zip_deterministico(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "pacote.zip")
            gerar_pacote_zip(self.resultado, zip_path, svg_conteudo="<svg></svg>")
            self.assertTrue(os.path.exists(zip_path))
            self.assertGreater(os.path.getsize(zip_path), 0)

            # Rejeição de sobrescrita (O_EXCL)
            with self.assertRaises(FileExistsError):
                gerar_pacote_zip(self.resultado, zip_path)


if __name__ == "__main__":
    unittest.main()
