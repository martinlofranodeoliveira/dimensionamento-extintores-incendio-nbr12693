"""Testes unitários da interface CLI da NBR 12693."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from extintores_nbr12693.cli import main


class TestCLI(unittest.TestCase):
    """Testa subcomandos, parâmetros e opções da CLI."""

    def test_cli_sem_argumentos(self) -> None:
        stdout_buf = io.StringIO()
        with redirect_stdout(stdout_buf):
            ret = main([])
        self.assertEqual(ret, 0)
        self.assertIn("extintores-nbr12693", stdout_buf.getvalue())

    def test_cli_catalogo(self) -> None:
        stdout_buf = io.StringIO()
        with redirect_stdout(stdout_buf):
            ret = main(["catalogo"])
        self.assertEqual(ret, 0)
        self.assertIn("ABNT NBR 12693:2021", stdout_buf.getvalue())
        self.assertIn("Risco Baixo", stdout_buf.getvalue())

    def test_cli_gerar_exemplo_stdout(self) -> None:
        stdout_buf = io.StringIO()
        with redirect_stdout(stdout_buf):
            ret = main(["gerar-exemplo"])
        self.assertEqual(ret, 0)
        self.assertIn("nome_edificacao", stdout_buf.getvalue())

    def test_cli_gerar_exemplo_arquivo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "exemplo.json")
            stdout_buf = io.StringIO()
            with redirect_stdout(stdout_buf):
                ret = main(["gerar-exemplo", "--saida", out_file])
            self.assertEqual(ret, 0)
            self.assertTrue(os.path.exists(out_file))

    def test_cli_calcular_arquivo_inexistente(self) -> None:
        stderr_buf = io.StringIO()
        with redirect_stderr(stderr_buf):
            ret = main(["calcular", "arquivo_que_nao_existe.json"])
        self.assertEqual(ret, 1)
        self.assertIn("Erro ao ler arquivo", stderr_buf.getvalue())

    def test_cli_calcular_formatos(self) -> None:
        raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        exemplo = os.path.join(raiz, "examples", "edificio_comercial_escritorios.json")

        for fmt in ["texto", "json", "csv", "svg"]:
            stdout_buf = io.StringIO()
            with redirect_stdout(stdout_buf):
                ret = main(["calcular", exemplo, "--formato", fmt])
            self.assertEqual(ret, 0, f"Falha no formato {fmt}")
            self.assertTrue(len(stdout_buf.getvalue()) > 0)

    def test_cli_calcular_pacote_zip(self) -> None:
        raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        exemplo = os.path.join(raiz, "examples", "edificio_comercial_escritorios.json")

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_dest = os.path.join(tmpdir, "pacote.zip")
            stdout_buf = io.StringIO()
            with redirect_stdout(stdout_buf):
                ret = main(["calcular", exemplo, "--pacote-zip", zip_dest])
            self.assertEqual(ret, 0)
            self.assertTrue(os.path.exists(zip_dest))


if __name__ == "__main__":
    unittest.main()
