"""Testes unitários dos codecs JSON da NBR 12693."""

import json
import unittest
from fractions import Fraction

from extintores_nbr12693.calculator import dimensionar_extintores_edificacao
from extintores_nbr12693.codecs import carregar_dados_extintores_json, exportar_resultado_json
from extintores_nbr12693.models import DadosEdificacao, DadosPavimento


class TestCodecs(unittest.TestCase):
    """Testa conformidade RFC 8259, rejeição de float, BOM e integridade de serialização."""

    def test_carregar_dados_valido(self) -> None:
        json_str = """{
            "nome_edificacao": "Edifício Alfa",
            "ocupacao": "Comercial",
            "pavimentos": [
                {
                    "nome_pavimento": "Térreo",
                    "area_m2": 300,
                    "carga_incendio_mj_m2": 250,
                    "maior_distancia_caminhamento_m": "15.0",
                    "riscos_especificos": []
                }
            ]
        }"""
        dados = carregar_dados_extintores_json(json_str)
        self.assertEqual(dados.nome_edificacao, "Edifício Alfa")
        self.assertEqual(len(dados.pavimentos), 1)
        self.assertEqual(dados.pavimentos[0].area_m2, Fraction(300, 1))

    def test_rejeitar_ponto_flutuante(self) -> None:
        json_float = """{
            "nome_edificacao": "Edifício Beta",
            "ocupacao": "Comercial",
            "pavimentos": [
                {
                    "nome_pavimento": "Térreo",
                    "area_m2": 350.5,
                    "carga_incendio_mj_m2": 250,
                    "maior_distancia_caminhamento_m": 15
                }
            ]
        }"""
        with self.assertRaises(ValueError) as ctx:
            carregar_dados_extintores_json(json_float)
        self.assertIn("Ponto flutuante", str(ctx.exception))

    def test_rejeitar_bom(self) -> None:
        json_bom = "\ufeff{\"nome_edificacao\": \"Teste\", \"ocupacao\": \"C\", \"pavimentos\": []}"
        with self.assertRaises(ValueError) as ctx:
            carregar_dados_extintores_json(json_bom)
        self.assertIn("Byte Order Mark", str(ctx.exception))

    def test_rejeitar_chaves_duplicadas(self) -> None:
        json_dup = """{
            "nome_edificacao": "Teste",
            "ocupacao": "Comercial",
            "ocupacao": "Serviços",
            "pavimentos": []
        }"""
        with self.assertRaises(ValueError) as ctx:
            carregar_dados_extintores_json(json_dup)
        self.assertIn("Chave duplicada", str(ctx.exception))

    def test_rejeitar_profundidade_excessiva(self) -> None:
        profundo = {"a": 1}
        for _ in range(35):
            profundo = {"sub": profundo}
        json_profundo = json.dumps(profundo)
        with self.assertRaises(ValueError) as ctx:
            carregar_dados_extintores_json(json_profundo)
        self.assertIn("Profundidade da estrutura JSON", str(ctx.exception))

    def test_rejeitar_raiz_lista(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            carregar_dados_extintores_json("[1, 2, 3]")
        self.assertIn("JSON raiz deve ser um objeto", str(ctx.exception))

    def test_exportar_json_resultado(self) -> None:
        pav = DadosPavimento(
            nome_pavimento="Térreo",
            area_m2=Fraction(300, 1),
            carga_incendio_mj_m2=Fraction(250, 1),
            maior_distancia_caminhamento_m=Fraction(15, 1),
        )
        dados = DadosEdificacao(
            nome_edificacao="Teste JSON",
            ocupacao="Comercial",
            pavimentos=(pav,),
        )
        res = dimensionar_extintores_edificacao(dados)
        json_out = exportar_resultado_json(res)
        self.assertIn("ABNT NBR 12693:2021", json_out)
        self.assertIn("Teste JSON", json_out)
        self.assertIn("Térreo", json_out)


if __name__ == "__main__":
    unittest.main()
