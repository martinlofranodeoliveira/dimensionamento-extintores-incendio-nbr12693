"""Testes unitários das constantes normativas da ABNT NBR 12693:2021."""

import unittest
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


class TestConstants(unittest.TestCase):
    """Verifica limites e coerência das constantes da NBR 12693:2021."""

    def test_limites_carga_incendio(self) -> None:
        self.assertEqual(LIMITE_CARGA_INCENDIO_BAIXO_MJ_M2, Fraction(300, 1))
        self.assertEqual(LIMITE_CARGA_INCENDIO_MEDIO_MJ_M2, Fraction(1200, 1))
        self.assertLess(LIMITE_CARGA_INCENDIO_BAIXO_MJ_M2, LIMITE_CARGA_INCENDIO_MEDIO_MJ_M2)

    def test_distancias_maximas_caminhamento(self) -> None:
        self.assertEqual(DISTANCIA_MAXIMA_CAMINHAR_BAIXO_M, Fraction(20, 1))
        self.assertEqual(DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M, Fraction(15, 1))
        self.assertEqual(DISTANCIA_MAXIMA_CAMINHAR_ALTO_M, Fraction(10, 1))
        # Risco mais alto exige menor distância a caminhar
        self.assertGreater(DISTANCIA_MAXIMA_CAMINHAR_BAIXO_M, DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M)
        self.assertGreater(DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M, DISTANCIA_MAXIMA_CAMINHAR_ALTO_M)

    def test_areas_maximas_por_unidade(self) -> None:
        self.assertEqual(AREA_MAXIMA_POR_UNIDADE_BAIXO_M2, Fraction(250, 1))
        self.assertEqual(AREA_MAXIMA_POR_UNIDADE_MEDIO_M2, Fraction(150, 1))
        self.assertEqual(AREA_MAXIMA_POR_UNIDADE_ALTO_M2, Fraction(100, 1))
        self.assertGreater(AREA_MAXIMA_POR_UNIDADE_BAIXO_M2, AREA_MAXIMA_POR_UNIDADE_MEDIO_M2)
        self.assertGreater(AREA_MAXIMA_POR_UNIDADE_MEDIO_M2, AREA_MAXIMA_POR_UNIDADE_ALTO_M2)

    def test_capacidades_minimas_extintoras(self) -> None:
        self.assertEqual(CAPACIDADE_MINIMA_A_BAIXO, 2)
        self.assertEqual(CAPACIDADE_MINIMA_B_BAIXO, 20)
        self.assertEqual(CAPACIDADE_MINIMA_A_MEDIO, 2)
        self.assertEqual(CAPACIDADE_MINIMA_B_MEDIO, 40)
        self.assertEqual(CAPACIDADE_MINIMA_A_ALTO, 4)
        self.assertEqual(CAPACIDADE_MINIMA_B_ALTO, 80)

    def test_regras_gerais_e_riscos_especificos(self) -> None:
        self.assertEqual(MINIMO_UNIDADES_POR_PAVIMENTO, 2)
        self.assertEqual(AREA_LIMITE_MEZANINO_UNIDADE_UNICA_M2, Fraction(50, 1))
        self.assertEqual(DISTANCIA_MAXIMA_RISCO_ELETRICO_M, Fraction(5, 1))
        self.assertEqual(DISTANCIA_MAXIMA_RISCO_LIQUIDO_GAS_M, Fraction(5, 1))
        self.assertEqual(DISTANCIA_MAXIMA_RISCO_COZINHA_K_M, Fraction(9, 1))

    def test_alturas_instalacao_e_sinalizacao(self) -> None:
        self.assertEqual(ALTURA_MAXIMA_SUPORTE_PAREDE_M, Fraction(16, 10))
        self.assertEqual(ALTURA_MINIMA_BASE_PISO_M, Fraction(1, 10))
        self.assertEqual(ALTURA_SINALIZACAO_FOTOLUMINESCENTE_M, Fraction(18, 10))


if __name__ == "__main__":
    unittest.main()
