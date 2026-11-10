"""Testes unitários dos modelos e dataclasses da NBR 12693."""

import unittest
from fractions import Fraction

from extintores_nbr12693.models import (
    ClasseFogo,
    DadosEdificacao,
    DadosPavimento,
    GrauRisco,
    RiscoEspecifico,
    TipoAgenteExtintor,
    TipoRiscoEspecifico,
)


class TestModels(unittest.TestCase):
    """Verifica instanciação, imutabilidade e validações dos modelos."""

    def test_enums(self) -> None:
        self.assertEqual(ClasseFogo.CLASSE_A.value, "A")
        self.assertEqual(ClasseFogo.CLASSE_K.value, "K")
        self.assertEqual(GrauRisco.BAIXO.value, "baixo")
        self.assertEqual(GrauRisco.ALTO.value, "alto")
        self.assertEqual(TipoAgenteExtintor.PO_ABC.value, "po_quimico_abc")
        self.assertEqual(TipoRiscoEspecifico.COZINHA_PROFISSIONAL.value, "cozinha_profissional")

    def test_risco_especifico_valido(self) -> None:
        r = RiscoEspecifico(
            identificador="QGBT-01",
            tipo=TipoRiscoEspecifico.QUADRO_ELETRICO_GERAL,
            distancia_ao_extintor_m=Fraction(3, 1),
            agente_sugerido=TipoAgenteExtintor.DIOXIDO_CARBONO,
        )
        self.assertEqual(r.identificador, "QGBT-01")
        self.assertEqual(r.distancia_ao_extintor_m, Fraction(3, 1))

    def test_risco_especifico_invalido(self) -> None:
        with self.assertRaises(ValueError):
            RiscoEspecifico(
                identificador="",
                tipo=TipoRiscoEspecifico.QUADRO_ELETRICO_GERAL,
                distancia_ao_extintor_m=Fraction(3, 1),
                agente_sugerido=TipoAgenteExtintor.DIOXIDO_CARBONO,
            )
        with self.assertRaises(ValueError):
            RiscoEspecifico(
                identificador="QGBT",
                tipo=TipoRiscoEspecifico.QUADRO_ELETRICO_GERAL,
                distancia_ao_extintor_m=Fraction(-1, 1),
                agente_sugerido=TipoAgenteExtintor.DIOXIDO_CARBONO,
            )

    def test_dados_pavimento_valido(self) -> None:
        p = DadosPavimento(
            nome_pavimento="Térreo",
            area_m2=Fraction(400, 1),
            carga_incendio_mj_m2=Fraction(250, 1),
            maior_distancia_caminhamento_m=Fraction(15, 1),
        )
        self.assertEqual(p.nome_pavimento, "Térreo")
        self.assertEqual(p.area_m2, Fraction(400, 1))

    def test_dados_pavimento_invalido(self) -> None:
        with self.assertRaises(ValueError):
            DadosPavimento(
                nome_pavimento="",
                area_m2=Fraction(400, 1),
                carga_incendio_mj_m2=Fraction(250, 1),
                maior_distancia_caminhamento_m=Fraction(15, 1),
            )
        with self.assertRaises(ValueError):
            DadosPavimento(
                nome_pavimento="Térreo",
                area_m2=Fraction(0, 1),
                carga_incendio_mj_m2=Fraction(250, 1),
                maior_distancia_caminhamento_m=Fraction(15, 1),
            )
        with self.assertRaises(ValueError):
            DadosPavimento(
                nome_pavimento="Térreo",
                area_m2=Fraction(400, 1),
                carga_incendio_mj_m2=Fraction(-10, 1),
                maior_distancia_caminhamento_m=Fraction(15, 1),
            )

    def test_dados_edificacao_valido(self) -> None:
        p = DadosPavimento(
            nome_pavimento="Pavimento 1",
            area_m2=Fraction(300, 1),
            carga_incendio_mj_m2=Fraction(200, 1),
            maior_distancia_caminhamento_m=Fraction(12, 1),
        )
        ed = DadosEdificacao(
            nome_edificacao="Prédio Central",
            ocupacao="Comercial",
            pavimentos=(p,),
        )
        self.assertEqual(ed.nome_edificacao, "Prédio Central")
        self.assertEqual(len(ed.pavimentos), 1)

    def test_dados_edificacao_invalido(self) -> None:
        with self.assertRaises(ValueError):
            DadosEdificacao(
                nome_edificacao="",
                ocupacao="Comercial",
                pavimentos=(),
            )
        with self.assertRaises(ValueError):
            DadosEdificacao(
                nome_edificacao="Prédio",
                ocupacao="",
                pavimentos=(),
            )


if __name__ == "__main__":
    unittest.main()
