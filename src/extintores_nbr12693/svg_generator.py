"""Gerador de painel técnico vetorial SVG para proteção por extintores NBR 12693:2021."""

from extintores_nbr12693.exporters import _fmt
from extintores_nbr12693.models import ResultadoDimensionamento


def gerar_painel_svg(res: ResultadoDimensionamento) -> str:
    """Gera painel vetorial SVG em alta resolução (1440x900) com esquema dos extintores."""
    largura = 1440
    altura = 900

    linhas: list[str] = []
    linhas.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} {altura}" width="{largura}" height="{altura}">')
    linhas.append('  <defs>')
    linhas.append('    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">')
    linhas.append('      <stop offset="0%" stop-color="#0f172a" />')
    linhas.append('      <stop offset="100%" stop-color="#1e293b" />')
    linhas.append('    </linearGradient>')
    linhas.append('    <linearGradient id="extintorGrad" x1="0" y1="0" x2="1" y2="0">')
    linhas.append('      <stop offset="0%" stop-color="#ef4444" />')
    linhas.append('      <stop offset="50%" stop-color="#b91c1c" />')
    linhas.append('      <stop offset="100%" stop-color="#7f1d1d" />')
    linhas.append('    </linearGradient>')
    linhas.append('    <linearGradient id="co2Grad" x1="0" y1="0" x2="1" y2="0">')
    linhas.append('      <stop offset="0%" stop-color="#64748b" />')
    linhas.append('      <stop offset="50%" stop-color="#334155" />')
    linhas.append('      <stop offset="100%" stop-color="#0f172a" />')
    linhas.append('    </linearGradient>')
    linhas.append('    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">')
    linhas.append('      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.4" />')
    linhas.append('    </filter>')
    linhas.append('  </defs>')

    # Fundo
    linhas.append(f'  <rect width="{largura}" height="{altura}" fill="url(#bgGrad)" />')

    # Cabeçalho
    linhas.append('  <rect x="30" y="25" width="1380" height="75" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5" />')
    linhas.append('  <text x="60" y="58" fill="#f8fafc" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="bold">LOFRANO TECNOLOGIA — ENGENHARIA DE SEGURANÇA CONTRA INCÊNDIO</text>')
    linhas.append('  <text x="60" y="82" fill="#38bdf8" font-family="system-ui, -apple-system, sans-serif" font-size="14">SISTEMAS DE PROTEÇÃO POR EXTINTORES DE INCÊNDIO — ABNT NBR 12693:2021</text>')
    linhas.append(f'  <text x="1380" y="70" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="13">Edificação: {res.nome_edificacao} | {res.ocupacao}</text>')

    # Painel Esquerdo: Indicadores Consolidados
    linhas.append('  <g transform="translate(30, 120)">')
    linhas.append('    <rect width="360" height="745" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1" />')
    linhas.append('    <text x="20" y="35" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="16" font-weight="bold">DADOS GERAIS DO SISTEMA</text>')
    linhas.append('    <line x1="20" y1="48" x2="340" y2="48" stroke="#334155" stroke-width="1" />')

    dados_painel_esq = [
        ("Área Total Protegida", f"{_fmt(res.area_total_m2, 2)} m²"),
        ("Quantidade de Pavimentos", f"{len(res.pavimentos)} pavimento(s)"),
        ("Total de Extintores", f"{res.total_extintores_edificacao} unidade(s)"),
        ("Norma Técnica", "ABNT NBR 12693:2021"),
        ("Sinalização de Emergência", "ABNT NBR 16820"),
        ("Precisão de Cálculo", "Racional Exata (Zero Float)"),
    ]

    y_pos = 80
    for rotulo, val in dados_painel_esq:
        linhas.append(f'    <text x="20" y="{y_pos}" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12">{rotulo}</text>')
        linhas.append(f'    <text x="20" y="{y_pos + 20}" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="15" font-weight="bold">{val}</text>')
        y_pos += 50

    # Bloco de Detalhe da Demarcação de Solo
    linhas.append('    <rect x="20" y="400" width="320" height="325" rx="6" fill="#0f172a" stroke="#475569" stroke-width="1" />')
    linhas.append('    <text x="35" y="425" fill="#facc15" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">SINALIZAÇÃO DE PISO REGULAMENTAR</text>')

    # Desenho da pintura de piso (amarelo e vermelho)
    linhas.append('    <g transform="translate(100, 450)">')
    linhas.append('      <rect width="160" height="160" fill="#facc15" stroke="#ca8a04" stroke-width="2" />')
    linhas.append('      <rect x="25" y="25" width="110" height="110" fill="#dc2626" stroke="#991b1b" stroke-width="1.5" />')
    linhas.append('      <text x="80" y="85" text-anchor="middle" fill="#ffffff" font-family="system-ui, sans-serif" font-size="11" font-weight="bold">ÁREA LIVRE</text>')
    linhas.append('    </g>')
    linhas.append('    <text x="35" y="640" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">• Dimensão Total: 1,00 m x 1,00 m</text>')
    linhas.append('    <text x="35" y="660" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">• Borda Amarela: 0,15 m perimetral</text>')
    linhas.append('    <text x="35" y="680" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">• Campo Vermelho Central: 0,70 m x 0,70 m</text>')
    linhas.append('    <text x="35" y="705" fill="#ef4444" font-family="system-ui, sans-serif" font-size="11" font-weight="bold">PROIBIDO QUALQUER OBSTÁCULO</text>')
    linhas.append('  </g>')

    # Painel Central: Corte Arquitetônico Esquemático dos Pavimentos e Extintores
    linhas.append('  <g transform="translate(410, 120)">')
    linhas.append('    <rect width="600" height="745" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1" />')
    linhas.append('    <text x="20" y="35" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="16" font-weight="bold">CORTE ESQUEMÁTICO — DISTRIBUIÇÃO E COTAS REGULAMENTARES</text>')
    linhas.append('    <line x1="20" y1="48" x2="580" y2="48" stroke="#334155" stroke-width="1" />')

    # Desenho dos pavimentos (até 4 pavimentos representados no corte)
    num_exib = min(4, len(res.pavimentos))
    h_pav = 140
    y_base_corte = 70

    for i in range(num_exib):
        p_obj = res.pavimentos[i]
        yp = y_base_corte + i * h_pav

        # Piso e laje
        linhas.append(f'    <rect x="40" y="{yp}" width="520" height="{h_pav - 15}" fill="#0f172a" stroke="#334155" stroke-width="1" />')
        linhas.append(f'    <rect x="40" y="{yp + h_pav - 20}" width="520" height="6" fill="#475569" />')  # piso

        # Rótulo do pavimento
        linhas.append(f'    <text x="55" y="{yp + 25}" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">{p_obj.nome_pavimento}</text>')
        linhas.append(f'    <text x="55" y="{yp + 42}" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">Risco {p_obj.grau_risco.value.upper()} | Área: {_fmt(p_obj.area_m2, 0)}m² | Dist. Máx: {_fmt(p_obj.distancia_maxima_caminhar_m, 0)}m</text>')

        # Representação de extintores no pavimento
        # Extintor 1 (Pó ABC)
        x_ext1 = 200
        y_ext_base = yp + h_pav - 20
        # Cilindro extintor
        linhas.append(f'    <rect x="{x_ext1 - 10}" y="{y_ext_base - 50}" width="20" height="42" rx="4" fill="url(#extintorGrad)" />')
        # Bico e alça
        linhas.append(f'    <rect x="{x_ext1 - 4}" y="{y_ext_base - 58}" width="8" height="8" fill="#e2e8f0" />')
        # Sinalização na parede (NBR 16820)
        linhas.append(f'    <rect x="{x_ext1 - 12}" y="{y_ext_base - 85}" width="24" height="18" fill="#ef4444" stroke="#ffffff" stroke-width="1" />')
        linhas.append(f'    <text x="{x_ext1}" y="{y_ext_base - 72}" text-anchor="middle" fill="#ffffff" font-family="system-ui, sans-serif" font-size="8" font-weight="bold">ABC</text>')

        # Extintor 2 (ou específico se houver)
        x_ext2 = 360
        linhas.append(f'    <rect x="{x_ext2 - 10}" y="{y_ext_base - 50}" width="20" height="42" rx="4" fill="url(#extintorGrad)" />')
        linhas.append(f'    <rect x="{x_ext2 - 4}" y="{y_ext_base - 58}" width="8" height="8" fill="#e2e8f0" />')
        linhas.append(f'    <rect x="{x_ext2 - 12}" y="{y_ext_base - 85}" width="24" height="18" fill="#ef4444" stroke="#ffffff" stroke-width="1" />')
        linhas.append(f'    <text x="{x_ext2}" y="{y_ext_base - 72}" text-anchor="middle" fill="#ffffff" font-family="system-ui, sans-serif" font-size="8" font-weight="bold">ABC</text>')

        # Extintor específico (se presente)
        if p_obj.riscos_especificos:
            x_ext3 = 480
            linhas.append(f'    <rect x="{x_ext3 - 8}" y="{y_ext_base - 55}" width="16" height="47" rx="3" fill="url(#co2Grad)" />')
            linhas.append(f'    <rect x="{x_ext3 - 4}" y="{y_ext_base - 62}" width="8" height="7" fill="#cbd5e1" />')
            linhas.append(f'    <rect x="{x_ext3 - 12}" y="{y_ext_base - 85}" width="24" height="18" fill="#0f172a" stroke="#ffffff" stroke-width="1" />')
            linhas.append(f'    <text x="{x_ext3}" y="{y_ext_base - 72}" text-anchor="middle" fill="#ffffff" font-family="system-ui, sans-serif" font-size="8" font-weight="bold">CO2</text>')

    # Linha e cota de altura regulamentar (1,60m e 1,80m)
    y_cota = y_base_corte + h_pav - 20
    linhas.append('    <g transform="translate(60, 0)">')
    linhas.append(f'      <line x1="70" y1="{y_cota}" x2="70" y2="{y_cota - 50}" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3" />')
    linhas.append(f'      <text x="65" y="{y_cota - 25}" text-anchor="end" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">h ≤ 1,60 m</text>')
    linhas.append(f'      <line x1="100" y1="{y_cota}" x2="100" y2="{y_cota - 80}" stroke="#4ade80" stroke-width="1.5" stroke-dasharray="3,3" />')
    linhas.append(f'      <text x="95" y="{y_cota - 60}" text-anchor="end" fill="#4ade80" font-family="system-ui, sans-serif" font-size="10" font-weight="bold">h = 1,80 m</text>')
    linhas.append('    </g>')

    # Legenda descritiva inferior
    linhas.append('    <rect x="40" y="650" width="520" height="75" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1" />')
    linhas.append('    <text x="55" y="675" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">DIRETRIZES DE INSTALAÇÃO (ITEM 5.4)</text>')
    linhas.append('    <text x="55" y="695" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">• Alça de empunhadura do suporte de parede fixada a no máximo 1,60 m do piso.</text>')
    linhas.append('    <text x="55" y="712" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">• Placa fotoluminescente (NBR 16820) sobreposta verticalmente a 1,80 m do piso.</text>')
    linhas.append('  </g>')

    # Painel Direito: Resumo por Pavimento e Conformidades
    linhas.append('  <g transform="translate(1030, 120)">')
    linhas.append('    <rect width="380" height="745" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1" />')
    linhas.append('    <text x="20" y="35" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="16" font-weight="bold">TABELA DE DISTRIBUIÇÃO</text>')
    linhas.append('    <line x1="20" y1="48" x2="360" y2="48" stroke="#334155" stroke-width="1" />')

    y_tab = 75
    for p in res.pavimentos:
        linhas.append(f'    <rect x="20" y="{y_tab}" width="340" height="95" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1" />')
        linhas.append(f'    <text x="35" y="{y_tab + 22}" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">{p.nome_pavimento}</text>')
        linhas.append(f'    <text x="35" y="{y_tab + 40}" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">Grau: {p.grau_risco.value.upper()} ({_fmt(p.carga_incendio_mj_m2, 0)} MJ/m²)</text>')
        linhas.append(f'    <text x="35" y="{y_tab + 58}" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">Capacidade: {p.capacidade_minima_a}-A : {p.capacidade_minima_b}-B:C</text>')
        linhas.append(f'    <text x="35" y="{y_tab + 78}" fill="#4ade80" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Total: {p.total_extintores_pavimento} extintor(es) ({_fmt(p.area_media_por_extintor_m2, 1)} m²/unid.)</text>')
        y_tab += 105

    # Rodapé do painel direito
    linhas.append('    <rect x="20" y="650" width="340" height="75" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1" />')
    linhas.append('    <text x="35" y="675" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">STATUS DE CONFORMIDADE</text>')
    status_cor = "#4ade80" if not res.alertas else "#facc15"
    status_msg = "SISTEMA CONFORME ABNT NBR 12693" if not res.alertas else f"{len(res.alertas)} ALERTA(S) REGISTRADO(S)"
    linhas.append(f'    <text x="35" y="698" fill="{status_cor}" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">{status_msg}</text>')
    linhas.append('    <text x="35" y="715" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Verificado via Lofrano Tecnologia</text>')
    linhas.append('  </g>')

    linhas.append('</svg>')
    return "\n".join(linhas)
