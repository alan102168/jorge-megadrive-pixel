#!/usr/bin/env python3
"""Confere se o arquivo e uma ROM Mega Drive, nao um HTML renomeado."""
from pathlib import Path
import sys

rom = Path(sys.argv[1])
content = rom.read_bytes()
if len(content) < 32768 or len(content) % 512:
    raise SystemExit(f"ROM invalida: tamanho inesperado ({len(content)} bytes)")
if content[0x100:0x104] != b"SEGA":
    raise SystemExit("ROM invalida: nao possui a assinatura SEGA no cabecalho")
if content.startswith(b"<!DOCTYPE") or b"<html" in content[:1024].lower():
    raise SystemExit("Erro: arquivo HTML renomeado em vez de uma ROM")
print(f"ROM Sega Mega Drive verificada: {rom}, {len(content)} bytes")
