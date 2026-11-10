# Dimensionamento de Sistemas de Proteção por Extintores de Incêndio (ABNT NBR 12693:2021)

[![CI](https://github.com/martinlofranodeoliveira/dimensionamento-extintores-incendio-nbr12693/actions/workflows/ci.yml/badge.svg)](https://github.com/martinlofranodeoliveira/dimensionamento-extintores-incendio-nbr12693/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Norma](https://img.shields.io/badge/norma-ABNT%20NBR%2012693%3A2021-orange.svg)](https://www.abnt.org.br/)
[![Aritmética](https://img.shields.io/badge/aritmética-racional%20exata%20(Zero%20Float)-success.svg)]()
[![Dependências](https://img.shields.io/badge/dependências-zero%20externas%20(stdlib)-brightgreen.svg)]()
[![Licença](https://img.shields.io/badge/licença-MIT-green.svg)](LICENSE)

Sistema computacional de alta precisão para projeto, cálculo e dimensionamento da proteção por extintores portáteis e sobre rodas em edificações residenciais, comerciais, industriais e de serviços, em estrita conformidade com os requisitos e critérios técnicos da norma brasileira **ABNT NBR 12693:2021** (*Sistemas de proteção por extintores de incêndio*) e Instruções Técnicas dos Corpos de Bombeiros Militares.

Desenvolvido segundo as diretrizes de engenharia de software da **LOFRANO TECNOLOGIA**: 100% em português brasileiro, dependência zero de pacotes externos (utilizando exclusivamente a biblioteca padrão do Python), aritmética racional exata via `fractions.Fraction` (proibição total de ponto flutuante IEEE-754 em cálculos de capacidade extintora, áreas de cobertura e distâncias de caminhamento) e empacotamento determinístico.

---

## Painel Esquemático de Engenharia

O módulo inclui gerador vetorial SVG integrado e renderização gráfica em alta resolução (1440x900) contendo o corte esquemático da edificação, distribuição dos extintores nos pavimentos, cotas ergonômicas de instalação e detalhe executivo da demarcação de piso regulamentar:

![Painel Esquemático de Proteção por Extintores NBR 12693](docs/exemplo.png)

---

## Fundamentação Normativa e Física (ABNT NBR 12693:2021)

### 1. Classes de Fogo Regulamentares
- **Classe A**: Combustíveis sólidos que deixam resíduos e brasas (madeira, papel, tecidos, borracha, plásticos). Agentes: Água Pressurizada (AP 10L, 2-A), Pó Químico Polivalente ABC, Espuma Mecânica (EM 10L, 2-A:10-B).
- **Classe B**: Líquidos e gases inflamáveis, óleos e graxas. Agentes: Pó Químico BC, Pó ABC, Dióxido de Carbono ($CO_2$), Espuma Mecânica.
- **Classe C**: Equipamentos e circuitos elétricos energizados (transformadores, QGBT, servidores). Agentes não condutores: $CO_2$ (5-B:C) e Pó ABC.
- **Classe D**: Metais pirofóricos e combustíveis (magnésio, titânio, zircônio, sódio, lítio). Agentes: Pós químicos especiais Classe D.
- **Classe K**: Meios de cocção comercial (óleos vegetais e gorduras animais em altas temperaturas em cozinhas profissionais). Agente: Solução aquosa de Acetato de Potássio (6L, 1-A:K).

### 2. Classificação do Grau de Risco e Parâmetros de Distribuição
A classificação da edificação ou compartimento fundamenta-se na carga de incêndio específica $q$ (MJ/m²):

| Grau de Risco | Carga de Incêndio ($q$) | Distância Máx. a Caminhar | Área Máx. Protegida / Unid. | Capacidade Mínima Requerida |
| :--- | :---: | :---: | :---: | :---: |
| **Risco Baixo** | $q \le 300\text{ MJ/m}^2$ | $20{,}0\text{ m}$ | $250\text{ m}^2$ | $2\text{-A} : 20\text{-B:C}$ |
| **Risco Médio** | $300 < q \le 1200\text{ MJ/m}^2$ | $15{,}0\text{ m}$ | $150\text{ m}^2$ | $2\text{-A} : 40\text{-B:C}$ |
| **Risco Alto** | $q > 1200\text{ MJ/m}^2$ | $10{,}0\text{ m}$ | $100\text{ m}^2$ | $4\text{-A} : 80\text{-B:C}$ |

### 3. Quantidade Mínima de Unidades Extintoras
Cada pavimento ou compartimentação autônoma deve possuir no mínimo **2 unidades extintoras** (sendo uma para Classe A e outra para Classe B/C, ou duas unidades de Pó ABC polivalente).

> **Exceção Normativa**: Para pavimentos ou mezaninos técnicos com área de até $50{,}0\text{ m}^2$, admite-se a instalação de apenas **1 unidade extintora** polivalente ABC.

A quantidade de unidades extintoras $N$ por pavimento é obtida por:

$$N = \max\left(N_{\text{mínimo}}, \left\lceil \frac{A_{\text{pavimento}}}{A_{\text{máx,unidade}}} \right\rceil, \left\lceil \frac{d_{\text{caminhamento}}}{d_{\text{máx,caminhar}}} \right\rceil \right)$$

### 4. Proteção de Riscos Especiais Localizados
Áreas com equipamentos críticos e riscos concentrados exigem proteção dedicada com extintor posicionado próximo ao equipamento:

- **Riscos Elétricos** (QGBT, subestações, transformadores, grupos moto-geradores, casa de bombas): Extintor de $CO_2$ ($4\text{ kg}$ ou $6\text{ kg}$) ou Pó ABC instalado a **no máximo $5{,}0\text{ m}$** do risco.
- **Líquidos e Gases Inflamáveis** (central de cilindros GLP, depósitos de solventes): Extintor de Pó BC ou ABC instalado a **no máximo $5{,}0\text{ m}$** do risco.
- **Cozinhas Comerciais / Industriais** (fritadeiras e chapas): Extintor Classe K (base acetato de potássio) instalado a **no máximo $9{,}0\text{ m}$** do foco de cocção.

### 5. Requisitos de Instalação e Ergonomia (Item 5.4 da NBR 12693)
- **Suporte de Parede**: a alça de empunhadura do extintor deve estar posicionada a no máximo $1{,}60\text{ m}$ do piso acabado.
- **Suporte de Piso**: a base do cilindro deve estar a uma altura entre $0{,}10\text{ m}$ e $0{,}20\text{ m}$ do piso.
- **Demarcação de Solo**: pintura regulamentar no piso com dimensões de $1{,}00\text{ m} \times 1{,}00\text{ m}$, composta por borda amarela de $0{,}15\text{ m}$ e campo central vermelho de $0{,}70\text{ m} \times 0{,}70\text{ m}$, proibindo qualquer tipo de obstrução.
- **Sinalização de Parede**: placa fotoluminescente (ABNT NBR 16820) fixada a $1{,}80\text{ m}$ de altura sobreposta ao equipamento.

---

## Fluxo Lógico e Arquitetura do Sistema

```mermaid
flowchart TD
    A[Arquivo de Entrada JSON Canônico] --> B[Decodificador Estrito RFC 8259]
    B --> C{Enquadramento por Carga q}
    C -->|q <= 300 MJ/m²| D1[Risco Baixo: 20m / 250m² / 2-A:20-B]
    C -->|300 < q <= 1200 MJ/m²| D2[Risco Médio: 15m / 150m² / 2-A:40-B]
    C -->|q > 1200 MJ/m²| D3[Risco Alto: 10m / 100m² / 4-A:80-B]
    D1 --> E[Cálculo de Unidades por Área e Caminhamento]
    D2 --> E
    D3 --> E
    E --> F[Aplicação do Mínimo Regulamentar]
    B --> G[Avaliação de Riscos Especiais]
    G --> H{Verificação de Distâncias Máximas}
    H -->|d <= 5m / 9m| I[Risco Conforme]
    H -->|d > 5m / 9m| J[Emissão de Alerta Normativo]
    F --> K[Consolidação Técnica dos Resultados]
    I --> K
    J --> K
    K --> L[Relatório Técnico Formatado]
    K --> M[Planilha CSV Sanitizada]
    K --> N[JSON Estruturado sem Float]
    K --> O[Painel Vetorial SVG 1440x900]
    K --> P[Pacote ZIP Determinístico O_EXCL]
```

---

## Estrutura do Repositório

```
dimensionamento-extintores-incendio-nbr12693/
├── .github/
│   └── workflows/
│       └── ci.yml                     # Pipeline CI multiplataforma (Linux 3.11-3.14, Windows 3.14)
├── docs/
│   ├── exemplo.png                    # Renderização gráfica do painel (1440x900)
│   └── painel_exemplo.svg             # Esquema vetorial da instalação
├── examples/
│   ├── edificio_comercial_escritorios.json # 4 pavimentos, escritórios e mezanino
│   ├── galpao_logistico_alta_carga.json    # Galpão industrial 2400m², risco alto
│   └── restaurante_cozinha_industrial.json # Restaurante com cozinha profissional Classe K
├── scripts/
│   ├── check_distribution.py         # Validador estrito de artefatos sdist e wheel
│   └── generate_assets.py            # Script headless de geração de imagens
├── src/
│   └── extintores_nbr12693/
│       ├── __init__.py                # Exportações principais do módulo
│       ├── calculator.py              # Motor de cálculo em frações exatas
│       ├── cli.py                     # Interface de linha de comando pt-BR
│       ├── codecs.py                  # Parser e serializador JSON RFC 8259
│       ├── constants.py               # Constantes e coeficientes da NBR 12693
│       ├── exporters.py               # Exportadores TXT, CSV sanitizado e ZIP determinístico
│       ├── models.py                  # Modelos imutáveis com validações prévias
│       ├── py.typed                   # Marcação de conformidade PEP 561
│       └── svg_generator.py           # Gerador procedural de esquemas vetoriais
├── tests/
│   ├── test_calculator.py             # Testes de distribuição, área e caminhamento
│   ├── test_casos_avancados.py        # Casos de borda, mezaninos, riscos elétricos/K
│   ├── test_cli.py                    # Testes de subcomandos e parâmetros da CLI
│   ├── test_codecs.py                 # Testes de rejeição de float, BOM e chaves duplicadas
│   ├── test_constants.py              # Testes das constantes físicas da NBR 12693
│   ├── test_exporters.py              # Testes de formatação, sanitização e integridade
│   ├── test_models.py                 # Testes de dataclasses e tipos enumerados
│   └── test_svg.py                    # Testes de integridade da saída gráfica SVG
├── tools/
│   └── verify_independent.py          # Auditor independente em SQLite em memória
├── LICENSE                            # Licença de Código Aberto MIT
├── pyproject.toml                     # Metadados de empacotamento PEP 517/621
└── README.md                          # Manual de engenharia e referência técnica
```

---

## Instalação e Execução

### Requisitos
- Python 3.11 ou superior (testado até Python 3.14).
- Nenhuma dependência externa necessária para execução de cálculos ou geração de relatórios.

### Instalação em Modo Editável
```bash
git clone https://github.com/martinlofranodeoliveira/dimensionamento-extintores-incendio-nbr12693.git
cd dimensionamento-extintores-incendio-nbr12693
pip install -e .
```

### Linha de Comando (CLI)

O pacote disponibiliza o ponto de entrada `extintores-nbr12693`:

```bash
# Exibir ajuda detalhada
extintores-nbr12693 --ajuda

# Executar cálculo exibindo memorial técnico descritivo
extintores-nbr12693 calcular examples/edificio_comercial_escritorios.json

# Exportar resultado em formato JSON canônico estruturado
extintores-nbr12693 calcular examples/edificio_comercial_escritorios.json --formato json

# Exportar planilha CSV sanitizada
extintores-nbr12693 calcular examples/edificio_comercial_escritorios.json --formato csv

# Gerar pacote completo determinístico ZIP contendo memorial, CSV, JSON e painel SVG
extintores-nbr12693 calcular examples/edificio_comercial_escritorios.json --pacote-zip dist/pacote_extintores.zip

# Gerar arquivo de modelo JSON para preenchimento
extintores-nbr12693 gerar-exemplo --saida novo_projeto.json

# Listar catálogo normativo de referências da NBR 12693
extintores-nbr12693 catalogo
```

---

## Formato do Arquivo de Entrada (JSON)

Exemplo de entrada para edifício comercial com riscos especiais (`examples/edificio_comercial_escritorios.json`):

```json
{
  "nome_edificacao": "Edifício Comercial Rocha Corporate",
  "ocupacao": "Comercial e Serviços",
  "pavimentos": [
    {
      "nome_pavimento": "Térreo - Hall e Acesso",
      "area_m2": 450,
      "carga_incendio_mj_m2": 250,
      "maior_distancia_caminhamento_m": "18.0",
      "riscos_especificos": [
        {
          "identificador": "QGBT - Entrada Geral de Energia",
          "tipo": "quadro_eletrico_geral",
          "distancia_ao_extintor_m": "3.5",
          "agente_sugerido": "dioxido_carbono_co2"
        }
      ]
    }
  ]
}
```

> **Atenção**: Números não-inteiros devem ser expressos entre aspas como strings decimais exatas (ex: `"18.0"`, `"3.5"`) para evitar contaminação por imprecisão binária de ponto flutuante IEEE-754.

---

## Verificação e Auditoria Independente

O projeto conta com uma ferramenta de auditoria independente (`tools/verify_independent.py`) que utiliza um banco de dados relacional `sqlite3` puramente em memória para reexecutar e auditar os cálculos sem importar os módulos de produção da biblioteca, garantindo blindagem contra vícios de implementação.

Para executar os testes e o auditor independente:

```bash
# Executar a suíte de 52 testes unitários nativos
PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v

# Executar o auditor independente em SQLite
python3 tools/verify_independent.py
```

---

## Licença

Distribuído sob a licença de código aberto MIT. Consulte o arquivo [LICENSE](LICENSE) para obter todos os termos e condições.

**Lofrano Tecnologia** — Engenharia de Software e Segurança Contra Incêndio de Alta Precisão (2026).
