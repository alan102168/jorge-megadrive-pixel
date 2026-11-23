# Jorge Truck Driver — Mega Drive Pixel Art

Versão nativa em C para **Sega Mega Drive**, com SGDK, gráficos originais em tiles de 8×8 pixels, caminhão, caixas e obstáculos.

## Arquivos

O GitHub Actions compila a ROM e publica em [Releases](../../releases):

- `Jorge_Truck_Driver.bin` — ROM de Mega Drive.
- `Jorge_Truck_Driver.png` — capa com o mesmo nome.
- `Jorge_Truck_Driver_M8_Lite.zip` — pacote com ROM e capa.

**Atenção:** a compatibilidade com o Game Stick M8 Lite depende do emulador e firmware do aparelho. Teste primeiro em emulador Mega Drive e faça backup do cartão microSD antes de copiar os arquivos. Não modifique BIOS nem arquivos do sistema.

Código: [src/main.c](src/main.c). Gerador de sprites: [tools/generate_art.py](tools/generate_art.py).

**Versões separadas:** [HTML Normal](https://github.com/alan102168/jogo-sest-senat-2d-caminhao) · [HTML Pixel](https://github.com/alan102168/jorge-html-pixel) · [Android Normal](https://github.com/alan102168/jorge-android-normal) · [Android Pixel](https://github.com/alan102168/jorge-truck-driver-android).
