"""Testes unitários do gerador vetorial SVG da NBR 12693."""

import unittest
from fractions import Fraction

from extintores_nbr12693.calculator import dimensionar_extintores_edificacao
from extintores_nbr12693.models import DadosEdificacao, DadosPavimento, RiscoEspecifico, TipoAgenteExtintor, TipoRiscoEspecifico
from extintores_nbr12693.svg_generator import gerar_painel_svg


class TestSVG(unittest.TestCase):
    """Verifica geração e atributos do painel esquemático SVG."""

    def setUp(self) -> None:
        risco = RiscoEspecifico(
            identificador="QGBT Principal",
            tipo=TipoRiscoEspecifico.QUADRO_ELETRICO_GERAL,
            distancia_ao_extintor_m=Fraction(3, 1),
            agente_sugerido=TipoAgenteExtintor.DIOXIDO_CARBONO,
        )
        pav = DadosPavimento(
            nome_pavimento="Térreo Central",
            area_m2=Fraction(500, 1),
            carga_incendio_mj_m2=Fraction(350, 1),
            maior_distancia_caminhamento_m=Fraction(14, 1),
            riscos_especificos=(risco,),
        )
        self.dados = DadosEdificacao(
            nome_edificacao="Torre SVG",
            ocupacao="Comercial",
            pavimentos=(pav,),
        )
        self.resultado = dimensionar_extintores_edificacao(self.dados)

    def test_dimensoes_e_namespaces(self) -> None:
        svg = gerar_painel_svg(self.resultado)
        self.assertIn('viewBox="0 0 1440 900"', svg)
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', svg)
        self.assertTrue(svg.strip().endswith("</svg>"))

    def test_elementos_obrigatorios(self) -> None:
        svg = gerar_painel_svg(self.resultado)
        self.assertIn("LOFRANO TECNOLOGIA", svg)
        self.assertIn("ABNT NBR 12693:2021", svg)
        self.assertIn("Torre SVG", svg)
        self.assertIn("SINALIZAÇÃO DE PISO REGULAMENTAR", svg)
        self.assertIn("h ≤ 1,60 m", svg)
        self.assertIn("h = 1,80 m", svg)
        self.assertIn("Térreo Central", svg)


if __name__ == "__main__":
    unittest.main()
