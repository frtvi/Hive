import os
import hashlib
import tkinter as tk
from tkinter import filedialog
from art import text2art

def calcular_hash(arquivo):
    hasher = hashlib.sha256()
    with open(arquivo, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def carregar_hashes_maliciosos():
    try:
        with open('hashes_maliciosos.txt', 'r') as arquivo_hashes:
            hashes = arquivo_hashes.read().split(',')
            return [h.strip() for h in hashes if h.strip()]
    except FileNotFoundError:
        print("Arquivo 'hashes_maliciosos.txt' não encontrado.")
        return []

def verificar_arquivos(directory, hashes_maliciosos, extensoes_maliciosas):
    arquivos_suspeitos = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            caminho_arquivo = os.path.join(root, file)

            if file.lower().endswith(tuple(extensoes_maliciosas)):
                hash_arquivo = calcular_hash(caminho_arquivo)

                if hash_arquivo in hashes_maliciosos:
                    arquivos_suspeitos.append(caminho_arquivo)

    return arquivos_suspeitos

def selecionar_diretorio():
    diretorio_alvo = filedialog.askdirectory()
    if diretorio_alvo:
        verificar_diretorio(diretorio_alvo)

def verificar_diretorio(diretorio_alvo):
    hashes_maliciosos = carregar_hashes_maliciosos()

    if not hashes_maliciosos:
        return  # Se não foi possível carregar hashes, encerre o programa

    extensoes_maliciosas = ['.exe', '.dll', '.bat', '.vbs', '.js', '.ps1', '.scr', '.hta', '.jar', '.py', '.pyc', '.pyo']

    arquivos_suspeitos = verificar_arquivos(diretorio_alvo, hashes_maliciosos, extensoes_maliciosas)

    if arquivos_suspeitos:
        print("Arquivos suspeitos encontrados:")
        for arquivo in arquivos_suspeitos:
            print(arquivo)
    else:
        print("Nenhum arquivo suspeito encontrado.")

def exibir_tela_inicial():
    arte_ascii = text2art("Hive", "block")
    print(arte_ascii)
    print("Opções:")
    print("1. Selecionar Diretório")
    print("2. Sair")

def main():
    exibir_tela_inicial()

    opcao = input("Digite o número da opção desejada: ")

    if opcao == "1":
        root = tk.Tk()
        root.withdraw()  # Oculta a janela principal do Tkinter
        selecionar_diretorio()
    elif opcao == "2":
        print("Programa encerrado.")
    else:
        print("Opção inválida. Programa encerrado.")

if __name__ == "__main__":
    main()
