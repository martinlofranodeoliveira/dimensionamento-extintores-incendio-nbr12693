"""Testes de casos avançados, limites e conformidades da ABNT NBR 12693:2021."""

import unittest
from fractions import Fraction

from extintores_nbr12693.calculator import dimensionar_extintores_edificacao, dimensionar_pavimento
from extintores_nbr12693.constants import (
    AREA_MAXIMA_POR_UNIDADE_ALTO_M2,
    AREA_MAXIMA_POR_UNIDADE_BAIXO_M2,
    AREA_MAXIMA_POR_UNIDADE_MEDIO_M2,
    DISTANCIA_MAXIMA_CAMINHAR_ALTO_M,
    DISTANCIA_MAXIMA_CAMINHAR_BAIXO_M,
    DISTANCIA_MAXIMA_CAMINHAR_MEDIO_M,
)
from extintores_nbr12693.models import (
    DadosEdificacao,
    DadosPavimento,
    GrauRisco,
    RiscoEspecifico,
    TipoAgenteExtintor,
    TipoRiscoEspecifico,
)


class TestCasosAvancados(unittest.TestCase):
    """Testes avançados de conformidade com a NBR 12693:2021."""

    def test_caminhamento_critico_provoca_unidades_adicionais(self) -> None:
        """Pavimento com área reduzida mas corredor longo (> 20m) exige mais de 1 extintor."""
        alertas: list[str] = []
        pav = DadosPavimento(
            nome_pavimento="Corredor Estreito Longo",
            area_m2=Fraction(100, 1),
            carga_incendio_mj_m2=Fraction(200, 1),  # Risco Baixo (dist_max = 20m)
            maior_distancia_caminhamento_m=Fraction(45, 1),  # 45m exige 3 extintores
        )
        res = dimensionar_pavimento(pav, alertas)
        self.assertEqual(res.grau_risco, GrauRisco.BAIXO)
        self.assertEqual(res.unidades_por_area, 1)  # 100 / 250 = 1
        self.assertEqual(res.unidades_por_caminhamento, 3)  # ceil(45 / 20) = 3
        self.assertEqual(res.unidades_minimas_adotadas, 3)

    def test_galpao_industrial_grande_porte(self) -> None:
        """Galpão de 10.000 m² em risco alto com múltiplos riscos específicos."""
        risco_subestacao = RiscoEspecifico(
            identificador="Subestação 500 kVA",
            tipo=TipoRiscoEspecifico.CABINE_SUBESTACAO,
            distancia_ao_extintor_m=Fraction(4, 1),
            agente_sugerido=TipoAgenteExtintor.DIOXIDO_CARBONO,
        )
        risco_gerador = RiscoEspecifico(
            identificador="Gerador Diesel",
            tipo=TipoRiscoEspecifico.GERADOR_ENERGIA,
            distancia_ao_extintor_m=Fraction(3, 1),
            agente_sugerido=TipoAgenteExtintor.PO_ABC,
        )
        risco_glp = RiscoEspecifico(
            identificador="Abrigo GLP",
            tipo=TipoRiscoEspecifico.CENTRAL_GLP,
            distancia_ao_extintor_m=Fraction(4, 1),
            agente_sugerido=TipoAgenteExtintor.PO_BC,
        )

        pav = DadosPavimento(
            nome_pavimento="Pátio Industrial",
            area_m2=Fraction(10000, 1),
            carga_incendio_mj_m2=Fraction(1500, 1),  # Risco Alto (100 m²/unid)
            maior_distancia_caminhamento_m=Fraction(9, 1),
            riscos_especificos=(risco_subestacao, risco_gerador, risco_glp),
        )

        dados = DadosEdificacao(
            nome_edificacao="Complexo Logístico e Industrial",
            ocupacao="Indústria",
            pavimentos=(pav,),
        )
        res = dimensionar_extintores_edificacao(dados)

        # 10.000 / 100 = 100 unidades base + 3 riscos específicos = 103 extintores
        self.assertEqual(res.pavimentos[0].unidades_por_area, 100)
        self.assertEqual(res.pavimentos[0].unidades_minimas_adotadas, 100)
        self.assertEqual(res.pavimentos[0].extintores_especificos_adotados, 3)
        self.assertEqual(res.total_extintores_edificacao, 103)
        self.assertEqual(len(res.alertas), 0)  # Todos conformes

    def test_cozinha_profissional_classe_k(self) -> None:
        """Cozinha com fritadeiras a 7m (conforme, máx 9m) e a 12m (alerta)."""
        alertas: list[str] = []
        risco_conforme = RiscoEspecifico(
            identificador="Fritadeira 01",
            tipo=TipoRiscoEspecifico.COZINHA_PROFISSIONAL,
            distancia_ao_extintor_m=Fraction(7, 1),
            agente_sugerido=TipoAgenteExtintor.CLASSE_K_ACETATO,
        )
        pav_ok = DadosPavimento(
            nome_pavimento="Cozinha Conforme",
            area_m2=Fraction(120, 1),
            carga_incendio_mj_m2=Fraction(400, 1),
            maior_distancia_caminhamento_m=Fraction(10, 1),
            riscos_especificos=(risco_conforme,),
        )
        res_ok = dimensionar_pavimento(pav_ok, alertas)
        self.assertTrue(res_ok.riscos_especificos[0].conforme_distancia)
        self.assertEqual(len(alertas), 0)

        alertas_falha: list[str] = []
        risco_inconforme = RiscoEspecifico(
            identificador="Fritadeira Distante",
            tipo=TipoRiscoEspecifico.COZINHA_PROFISSIONAL,
            distancia_ao_extintor_m=Fraction(12, 1),  # Máx é 9m
            agente_sugerido=TipoAgenteExtintor.CLASSE_K_ACETATO,
        )
        pav_falha = DadosPavimento(
            nome_pavimento="Cozinha Falha",
            area_m2=Fraction(120, 1),
            carga_incendio_mj_m2=Fraction(400, 1),
            maior_distancia_caminhamento_m=Fraction(10, 1),
            riscos_especificos=(risco_inconforme,),
        )
        res_falha = dimensionar_pavimento(pav_falha, alertas_falha)
        self.assertFalse(res_falha.riscos_especificos[0].conforme_distancia)
        self.assertTrue(any("excede o limite máximo permitido de 9m" in a for a in alertas_falha))

    def test_edificacao_multipavimentos_totalizacao(self) -> None:
        """Edifício de 5 pavimentos iguais verifica a soma e área total."""
        pavs = []
        for i in range(1, 6):
            pavs.append(
                DadosPavimento(
                    nome_pavimento=f"Andar {i}",
                    area_m2=Fraction(300, 1),
                    carga_incendio_mj_m2=Fraction(300, 1),
                    maior_distancia_caminhamento_m=Fraction(12, 1),
                )
            )
        dados = DadosEdificacao(
            nome_edificacao="Edifício Torre 5 Andares",
            ocupacao="Escritórios",
            pavimentos=tuple(pavs),
        )
        res = dimensionar_extintores_edificacao(dados)
        self.assertEqual(res.area_total_m2, Fraction(1500, 1))
        # 300 / 250 = 2 extintores por pavimento * 5 = 10 extintores
        self.assertEqual(res.total_extintores_edificacao, 10)

    def test_area_media_por_extintor(self) -> None:
        """Verifica a fração exata de área média por extintor."""
        pav = DadosPavimento(
            nome_pavimento="Galpão Teste",
            area_m2=Fraction(900, 1),
            carga_incendio_mj_m2=Fraction(600, 1),
            maior_distancia_caminhamento_m=Fraction(15, 1),
        )
        alertas: list[str] = []
        res = dimensionar_pavimento(pav, alertas)
        # 900 / 150 = 6 extintores -> área média = 900 / 6 = 150 m²/unid
        self.assertEqual(res.area_media_por_extintor_m2, Fraction(150, 1))

    def test_risco_gas_glp_limites_distancia(self) -> None:
        """Testa abrigo de gás GLP a 4m (conforme) e 8m (alerta)."""
        alertas_ok: list[str] = []
        risco_ok = RiscoEspecifico(
            identificador="Abrigo P-45",
            tipo=TipoRiscoEspecifico.CENTRAL_GLP,
            distancia_ao_extintor_m=Fraction(4, 1),
            agente_sugerido=TipoAgenteExtintor.PO_BC,
        )
        pav_ok = DadosPavimento(
            nome_pavimento="Área Técnica GLP",
            area_m2=Fraction(80, 1),
            carga_incendio_mj_m2=Fraction(300, 1),
            maior_distancia_caminhamento_m=Fraction(8, 1),
            riscos_especificos=(risco_ok,),
        )
        res_ok = dimensionar_pavimento(pav_ok, alertas_ok)
        self.assertTrue(res_ok.riscos_especificos[0].conforme_distancia)
        self.assertEqual(len(alertas_ok), 0)

        alertas_bad: list[str] = []
        risco_bad = RiscoEspecifico(
            identificador="Abrigo P-45 Afastado",
            tipo=TipoRiscoEspecifico.CENTRAL_GLP,
            distancia_ao_extintor_m=Fraction(8, 1),
            agente_sugerido=TipoAgenteExtintor.PO_BC,
        )
        pav_bad = DadosPavimento(
            nome_pavimento="Área Técnica GLP",
            area_m2=Fraction(80, 1),
            carga_incendio_mj_m2=Fraction(300, 1),
            maior_distancia_caminhamento_m=Fraction(8, 1),
            riscos_especificos=(risco_bad,),
        )
        res_bad = dimensionar_pavimento(pav_bad, alertas_bad)
        self.assertFalse(res_bad.riscos_especificos[0].conforme_distancia)
        self.assertTrue(any("excede o limite máximo permitido de 5m" in a for a in alertas_bad))

    def test_risco_eletrico_transformador(self) -> None:
        """Testa cabine de transformadores com CO2."""
        alertas: list[str] = []
        risco_trafo = RiscoEspecifico(
            identificador="Transformador a Óleo 300 kVA",
            tipo=TipoRiscoEspecifico.CABINE_SUBESTACAO,
            distancia_ao_extintor_m=Fraction(3, 1),
            agente_sugerido=TipoAgenteExtintor.DIOXIDO_CARBONO,
        )
        pav = DadosPavimento(
            nome_pavimento="Subsolo Técnico",
            area_m2=Fraction(200, 1),
            carga_incendio_mj_m2=Fraction(400, 1),
            maior_distancia_caminhamento_m=Fraction(10, 1),
            riscos_especificos=(risco_trafo,),
        )
        res = dimensionar_pavimento(pav, alertas)
        self.assertTrue(res.riscos_especificos[0].conforme_distancia)
        self.assertEqual(res.riscos_especificos[0].distancia_maxima_permitida_m, Fraction(5, 1))

    def test_fracao_area_fracionaria_exata(self) -> None:
        """Testa cálculo rigoroso com área fracionária (ex: 225.5 m²)."""
        alertas: list[str] = []
        pav = DadosPavimento(
            nome_pavimento="Sala Comercial Fracionária",
            area_m2=Fraction(451, 2),  # 225.5 m²
            carga_incendio_mj_m2=Fraction(250, 1),  # Risco Baixo (250 m²/unid)
            maior_distancia_caminhamento_m=Fraction(12, 1),
        )
        res = dimensionar_pavimento(pav, alertas)
        # 225.5 <= 250 -> 1 unidade por área, mas mínimo por pavimento é 2
        self.assertEqual(res.unidades_por_area, 1)
        self.assertEqual(res.unidades_minimas_adotadas, 2)

    def test_sinalizacao_solo_geometria(self) -> None:
        """Verifica se a geometria da demarcação de piso atende a NBR 12693 e IT-CB."""
        from extintores_nbr12693.constants import (
            COMPRIMENTO_DEMARCACAO_PISO_M,
            LADO_QUADRADO_VERMELHO_M,
            LARGURA_DEMARCACAO_PISO_M,
            LARGURA_FAIXA_AMARELA_M,
        )
        self.assertEqual(LARGURA_DEMARCACAO_PISO_M, Fraction(1, 1))
        self.assertEqual(COMPRIMENTO_DEMARCACAO_PISO_M, Fraction(1, 1))
        # Largura total = miolo vermelho + 2 * faixa amarela = 0.70 + 2*0.15 = 1.00m
        self.assertEqual(LADO_QUADRADO_VERMELHO_M + (2 * LARGURA_FAIXA_AMARELA_M), Fraction(1, 1))

    def test_acumulacao_multiplos_alertas_edificacao(self) -> None:
        """Verifica a consolidação dos alertas em múltiplos pavimentos."""
        r1 = RiscoEspecifico("QGBT-Distante", TipoRiscoEspecifico.QUADRO_ELETRICO_GERAL, Fraction(7, 1), TipoAgenteExtintor.DIOXIDO_CARBONO)
        r2 = RiscoEspecifico("Fritadeira-Distante", TipoRiscoEspecifico.COZINHA_PROFISSIONAL, Fraction(15, 1), TipoAgenteExtintor.CLASSE_K_ACETATO)

        p1 = DadosPavimento("Andar 1", Fraction(200, 1), Fraction(300, 1), Fraction(10, 1), (r1,))
        p2 = DadosPavimento("Andar 2", Fraction(200, 1), Fraction(300, 1), Fraction(10, 1), (r2,))

        dados = DadosEdificacao("Prédio Alertas", "Comércio", (p1, p2))
        res = dimensionar_extintores_edificacao(dados)
        self.assertEqual(len(res.alertas), 2)


if __name__ == "__main__":
    unittest.main()
