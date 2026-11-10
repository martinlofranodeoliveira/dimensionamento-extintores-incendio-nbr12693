"""Testes unitários do motor de cálculo de extintores NBR 12693."""

import unittest
from fractions import Fraction

from extintores_nbr12693.calculator import (
    _teto_fracao,
    determinar_grau_risco,
    dimensionar_extintores_edificacao,
    dimensionar_pavimento,
    obter_distancia_maxima_risco_especifico,
)
from extintores_nbr12693.constants import (
    DISTANCIA_MAXIMA_CAMINHAR_ALTO_M,
    DISTANCIA_MAXIMA_CAMINHAR_BAIXO_M,
    DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M,
    DISTANCIA_MAXIMA_RISCO_COZINHA_K_M,
    DISTANCIA_MAXIMA_RISCO_ELETRICO_M,
    DISTANCIA_MAXIMA_RISCO_LIQUIDO_GAS_M,
)
from extintores_nbr12693.models import (
    DadosEdificacao,
    DadosPavimento,
    GrauRisco,
    RiscoEspecifico,
    TipoAgenteExtintor,
    TipoRiscoEspecifico,
)


class TestCalculator(unittest.TestCase):
    """Testa os cálculos de distribuição, áreas, caminhamento e riscos especiais."""

    def test_teto_fracao(self) -> None:
        self.assertEqual(_teto_fracao(Fraction(10, 1)), 10)
        self.assertEqual(_teto_fracao(Fraction(0, 1)), 0)
        self.assertEqual(_teto_fracao(Fraction(7, 2)), 4)
        self.assertEqual(_teto_fracao(Fraction(1, 10)), 1)
        self.assertEqual(_teto_fracao(Fraction(25, 4)), 7)

    def test_determinar_grau_risco(self) -> None:
        self.assertEqual(determinar_grau_risco(Fraction(150, 1)), GrauRisco.BAIXO)
        self.assertEqual(determinar_grau_risco(Fraction(300, 1)), GrauRisco.BAIXO)
        self.assertEqual(determinar_grau_risco(Fraction(301, 1)), GrauRisco.MEDIO)
        self.assertEqual(determinar_grau_risco(Fraction(1200, 1)), GrauRisco.MEDIO)
        self.assertEqual(determinar_grau_risco(Fraction(1201, 1)), GrauRisco.ALTO)
        self.assertEqual(determinar_grau_risco(Fraction(2000, 1)), GrauRisco.ALTO)

    def test_obter_distancia_maxima_risco_especifico(self) -> None:
        self.assertEqual(
            obter_distancia_maxima_risco_especifico(TipoRiscoEspecifico.QUADRO_ELETRICO_GERAL),
            DISTANCIA_MAXIMA_RISCO_ELETRICO_M,
        )
        self.assertEqual(
            obter_distancia_maxima_risco_especifico(TipoRiscoEspecifico.CENTRAL_GLP),
            DISTANCIA_MAXIMA_RISCO_LIQUIDO_GAS_M,
        )
        self.assertEqual(
            obter_distancia_maxima_risco_especifico(TipoRiscoEspecifico.COZINHA_PROFISSIONAL),
            DISTANCIA_MAXIMA_RISCO_COZINHA_K_M,
        )

    def test_dimensionar_pavimento_risco_baixo(self) -> None:
        alertas: list[str] = []
        pav = DadosPavimento(
            nome_pavimento="Térreo Comercial",
            area_m2=Fraction(480, 1),
            carga_incendio_mj_m2=Fraction(250, 1),
            maior_distancia_caminhamento_m=Fraction(18, 1),
        )
        res = dimensionar_pavimento(pav, alertas)
        self.assertEqual(res.grau_risco, GrauRisco.BAIXO)
        self.assertEqual(res.distancia_maxima_caminhar_m, DISTANCIA_MAXIMA_CAMINHAR_BAIXO_M)
        # 480 / 250 = 1.92 -> 2 unidades por área
        self.assertEqual(res.unidades_por_area, 2)
        # 18 / 20 = 0.9 -> 1 unidade por caminhamento
        self.assertEqual(res.unidades_por_caminhamento, 1)
        # Mínimo regulamentar é 2 unidades
        self.assertEqual(res.unidades_minimas_adotadas, 2)
        self.assertEqual(res.total_extintores_pavimento, 2)
        self.assertEqual(res.capacidade_minima_a, 2)
        self.assertEqual(res.capacidade_minima_b, 20)

    def test_dimensionar_pavimento_risco_medio(self) -> None:
        alertas: list[str] = []
        pav = DadosPavimento(
            nome_pavimento="Escritórios",
            area_m2=Fraction(400, 1),
            carga_incendio_mj_m2=Fraction(500, 1),
            maior_distancia_caminhamento_m=Fraction(14, 1),
        )
        res = dimensionar_pavimento(pav, alertas)
        self.assertEqual(res.grau_risco, GrauRisco.MEDIO)
        self.assertEqual(res.distancia_maxima_caminhar_m, DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M)
        # 400 / 150 = 2.66 -> 3 unidades por área
        self.assertEqual(res.unidades_por_area, 3)
        self.assertEqual(res.unidades_minimas_adotadas, 3)
        self.assertEqual(res.capacidade_minima_a, 2)
        self.assertEqual(res.capacidade_minima_b, 40)

    def test_dimensionar_pavimento_risco_alto(self) -> None:
        alertas: list[str] = []
        pav = DadosPavimento(
            nome_pavimento="Galpão Químico",
            area_m2=Fraction(500, 1),
            carga_incendio_mj_m2=Fraction(1800, 1),
            maior_distancia_caminhamento_m=Fraction(9, 1),
        )
        res = dimensionar_pavimento(pav, alertas)
        self.assertEqual(res.grau_risco, GrauRisco.ALTO)
        self.assertEqual(res.distancia_maxima_caminhar_m, DISTANCIA_MAXIMA_CAMINHAR_ALTO_M)
        # 500 / 100 = 5 unidades por área
        self.assertEqual(res.unidades_por_area, 5)
        self.assertEqual(res.unidades_minimas_adotadas, 5)
        self.assertEqual(res.capacidade_minima_a, 4)
        self.assertEqual(res.capacidade_minima_b, 80)

    def test_mezanino_ate_50m2_aceita_uma_unidade(self) -> None:
        alertas: list[str] = []
        pav = DadosPavimento(
            nome_pavimento="Mezanino Técnico",
            area_m2=Fraction(45, 1),
            carga_incendio_mj_m2=Fraction(200, 1),
            maior_distancia_caminhamento_m=Fraction(10, 1),
        )
        res = dimensionar_pavimento(pav, alertas)
        self.assertEqual(res.unidades_minimas_adotadas, 1)
        self.assertEqual(res.total_extintores_pavimento, 1)

    def test_risco_especifico_emite_alerta_se_distancia_excedida(self) -> None:
        alertas: list[str] = []
        risco_distante = RiscoEspecifico(
            identificador="QGBT Afastado",
            tipo=TipoRiscoEspecifico.QUADRO_ELETRICO_GERAL,
            distancia_ao_extintor_m=Fraction(8, 1),  # Máx é 5m
            agente_sugerido=TipoAgenteExtintor.DIOXIDO_CARBONO,
        )
        pav = DadosPavimento(
            nome_pavimento="Térreo",
            area_m2=Fraction(200, 1),
            carga_incendio_mj_m2=Fraction(200, 1),
            maior_distancia_caminhamento_m=Fraction(10, 1),
            riscos_especificos=(risco_distante,),
        )
        res = dimensionar_pavimento(pav, alertas)
        self.assertFalse(res.riscos_especificos[0].conforme_distancia)
        self.assertTrue(len(alertas) > 0)
        self.assertTrue(any("excede o limite máximo permitido de 5m" in a for a in alertas))


if __name__ == "__main__":
    unittest.main()
