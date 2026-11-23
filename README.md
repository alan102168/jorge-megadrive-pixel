# 🎮 Jorge the Truck Driver — Mega Drive Pixel Art

> **Somente a ROM nativa de Mega Drive.** Não coloque HTML ou APK neste repositório.

### ⬇️ Baixar para emulador / M8 Lite

**[Releases — ROM, capa e ZIP](https://github.com/alan102168/jorge-megadrive-pixel/releases)**

Arquivos gerados automaticamente:
- `Jorge_Truck_Driver.bin` — ROM verdadeira de Sega Mega Drive.
- `Jorge_Truck_Driver.png` — capa original com o mesmo nome.
- `Jorge_Truck_Driver_M8_Lite.zip` — pacote com os dois arquivos.

### 🕹 Jogabilidade 16 bits

Jorge dirige por três faixas, pega caixas (+1 ponto), evita rochas/cones (-1 vida) e perde 3 pontos ao deixar uma caixa passar. Controle Mega Drive: cima/baixo, A/C para acelerar, B para frear, Start para iniciar/pausar.

É uma adaptação original **mais simples que o HTML**, com artes próprias feitas em pixels/tiles 8×8, compilada em C com [SGDK](https://github.com/Stephane-D/SGDK).

### 📁 Estrutura

- `src/main.c` — jogo nativo em C.
- `tools/generate_art.py` — gera tiles e sprites 16 bits.
- `tools/create_cover.py` — gera a capa PNG.
- `tools/verify_rom.py` — valida cabeçalho da ROM.
- `.github/workflows/megadrive-rom.yml` — compila, confere e publica no GitHub.

Os arquivos compilados em `dist/`, `out/` e `src/graphics.h` são **gerados automaticamente**, não devem ser editados manualmente.

### ⚠️ Antes de colocar no Game Stick

1. Primeiro, teste a ROM num emulador Mega Drive no PC.
2. Faça backup do microSD do M8 Lite.
3. Confira a pasta e o formato que o firmware reconhece.
4. Copie `.bin` e `.png` juntos, com o mesmo nome, sem apagar BIOS ou arquivos do sistema.

A compilação SGDK já foi confirmada, **mas o funcionamento em cada revisão do Game Stick M8 Lite ainda depende de teste real**.

### 📚 Outras versões

| Edição | Repositório |
|---|---|
| 🌐 HTML Normal | [Abrir](https://github.com/alan102168/jogo-sest-senat-2d-caminhao) |
| 🎨 HTML Pixel Art | [Abrir](https://github.com/alan102168/jorge-html-pixel) |
| 📱 Android Normal | [Abrir](https://github.com/alan102168/jorge-android-normal) |
| 📱 Android Pixel Art | [Abrir](https://github.com/alan102168/jorge-truck-driver-android) |
| 🎮 ROM Mega Drive Pixel Art | [Abrir](https://github.com/alan102168/jorge-megadrive-pixel) |
