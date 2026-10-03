def converter_bases(df):
    print("\n===== DISPOSITIVOS, BASES NUMÉRICAS E ELETRICIDADE =====")
    print("Entrada: sensores de latência, tensão e corrente em cada módulo (simulados pelo CSV).")
    print("Saída: terminal, relatório e gráficos gerados pelo sistema.")
    print("Interface: rede/Wi-Fi da colônia enviando as leituras para a central (conceitual).")
    codigo = input("\nDigite um código de sensor em hexadecimal (Enter para 0x1A01): ").strip() or "0x1A01"
    try:
        decimal = int(codigo, 16)
    except ValueError:
        print("Código inválido.")
        return
    print(f"Hexadecimal: {hex(decimal)}")
    print(f"Decimal    : {decimal}")
    print(f"Binário    : {bin(decimal)}")
    print(f"Octal      : {oct(decimal)}")
    linha = df[df["codigo_sensor"].str.lower() == hex(decimal)]
    if not linha.empty:
        l = linha.iloc[0]
        print(f"\nSensor pertence ao módulo {l['modulo']} (ciclo {l['ciclo']})")
        print(f"Tensão V = {l['tensao_v']} V | Corrente I = {l['corrente_a']} A")
        print(f"Potência P = V x I = {l['potencia_w']} W")
        print(f"Resistência pela Lei de Ohm R = V / I = {l['resistencia_ohm']} Ω")
        # Energia em kWh = potência (W) x horas / 1000
        energia = l["potencia_w"] * 24 / 1000
        print(f"Energia gasta pelo transmissor em 24h: {energia:.3f} kWh")
    print("\nPotência média por tipo de módulo:")
    print(df.groupby("tipo")["potencia_w"].mean().round(2).to_string())
