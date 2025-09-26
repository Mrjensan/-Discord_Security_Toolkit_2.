#!/usr/bin/env python3
"""
Discord Security Toolkit v2.0 - Setup Script
Desenvolvido por Jensan - https://github.com/
Script de configuração e instalação automática
"""

import os
import sys
import subprocess
import platform

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║           Discord Security Toolkit v2.0 Setup              ║
║                   Criado por Jensan                         ║
║                https://github.com/                          ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ é necessário!")
        print(f"Versão atual: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} detectado")
    return True

def install_requirements():
    """Instala dependências necessárias"""
    print("\n📦 Instalando dependências...")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_advanced.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")

    directories = ["reports", "logs", "temp", "exports"]

    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Diretório criado: {directory}")
        except Exception as e:
            print(f"❌ Erro ao criar {directory}: {e}")

def setup_permissions():
    """Configura permissões necessárias (Linux/Mac)"""
    if platform.system() != "Windows":
        print("\n🔐 Configurando permissões...")
        try:
            os.chmod("discord_security_toolkit.py", 0o755)
            os.chmod("advanced_discord_reverser.py", 0o755)
            print("✅ Permissões configuradas")
        except Exception as e:
            print(f"⚠️ Aviso: {e}")

def verify_installation():
    """Verifica se a instalação foi bem-sucedida"""
    print("\n🔍 Verificando instalação...")

    required_files = [
        "discord_security_toolkit.py",
        "discord_security_analyzer.py", 
        "discord_permission_auditor.py",
        "discord_api_security_tester.py",
        "discord_info_security_scanner.py",
        "advanced_discord_reverser.py",
        "config.ini"
    ]

    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - AUSENTE")
            missing_files.append(file)

    if missing_files:
        print(f"\n⚠️ Arquivos ausentes: {', '.join(missing_files)}")
        return False

    print("\n🎉 Instalação verificada com sucesso!")
    return True

def main():
    print_banner()
    print("🚀 Iniciando configuração do Discord Security Toolkit...")
    print("⚠️ Para fins educacionais e pesquisa de segurança apenas!")

    # Verificações
    if not check_python_version():
        sys.exit(1)

    # Instalação
    create_directories()

    if input("\n📦 Instalar dependências? (s/n): ").lower() == 's':
        if not install_requirements():
            print("❌ Falha na instalação de dependências")
            sys.exit(1)

    setup_permissions()

    if not verify_installation():
        print("❌ Falha na verificação da instalação")
        sys.exit(1)

    print("\n" + "="*60)
    print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print("\n🚀 Para começar, execute:")
    print("   python discord_security_toolkit.py")
    print("\n📚 Leia o README_v2.md para documentação completa")
    print("\n⚖️ LEMBRE-SE:")
    print("   • Use apenas para fins educacionais")
    print("   • Teste apenas seus próprios recursos")
    print("   • Siga práticas de divulgação responsável")
    print("\n💝 Criado com ❤️ por Jensan")
    print("⭐ GitHub: https://github.com/")

if __name__ == "__main__":
    main()
