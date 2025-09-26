#!/usr/bin/env python3
"""
Discord Security Toolkit v2.0 - Suite Completa
Desenvolvido por Jensan - https://github.com/
Ferramenta educacional completa para análise de segurança Discord

AVISO: Use apenas para fins educacionais e análise de segurança pessoal!
"""

import os
import sys
import json
import importlib.util
from datetime import datetime

class DiscordSecurityToolkit:
    def __init__(self):
        self.version = "2.0"
        self.author = "Jensan"
        self.github = "https://github.com/"

        self.tools = {
            "1": {
                "name": "Security Token Analyzer",
                "description": "Análise avançada de tokens Discord para auditoria de segurança",
                "module": "discord_security_analyzer",
                "class": "DiscordTokenSecurityAnalyzer",
                "icon": "🔐"
            },
            "2": {
                "name": "Permission Security Auditor", 
                "description": "Auditoria completa de permissões em servidores Discord",
                "module": "discord_permission_auditor",
                "class": "DiscordPermissionSecurityAuditor",
                "icon": "🛡️"
            },
            "3": {
                "name": "API Security Tester",
                "description": "Testes de robustez e consistência da API Discord",
                "module": "discord_api_security_tester", 
                "class": "DiscordAPISecurityTester",
                "icon": "⚡"
            },
            "4": {
                "name": "Information Security Scanner",
                "description": "Scanner de informações públicas e análise de privacidade",
                "module": "discord_info_security_scanner",
                "class": "DiscordInfoSecurityScanner",
                "icon": "🔍"
            }
        }

        self.session_data = {
            "session_start": datetime.now().isoformat(),
            "tools_used": [],
            "security_findings": [],
            "recommendations": []
        }

    def display_main_banner(self):
        """
        Exibe o banner principal da suite
        """
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║              Discord Security Toolkit v{self.version}                ║
║                   Criado por {self.author}                           ║
║                  {self.github}                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔐 Suite Completa de Segurança para Discord                ║
║  🛡️ Ferramentas Educacionais e Profissionais                ║
║  📊 Análise Avançada e Relatórios Detalhados                ║
║                                                              ║
║  ⚠️  IMPORTANTE:                                             ║
║  • Use apenas para fins educacionais                       ║
║  • Teste apenas seus próprios recursos                     ║
║  • Siga práticas de segurança responsável                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def display_tools_menu(self):
        """
        Exibe menu de ferramentas disponíveis
        """
        print("\n" + "="*70)
        print("                    FERRAMENTAS DE SEGURANÇA")
        print("="*70)

        for key, tool in self.tools.items():
            print(f"{tool['icon']} {key}. {tool['name']}")
            print(f"     {tool['description']}")
            print()

        print("📊 r. Gerar relatório de segurança da sessão")
        print("📚 h. Exibir guia de segurança Discord")
        print("🌐 l. Alterar idioma / Change Language")
        print("❌ q. Sair / Exit")
        print("="*70)

    def display_security_guide(self):
        """
        Exibe guia abrangente de segurança Discord
        """
        guide = f"""
╔══════════════════════════════════════════════════════════════╗
║                   GUIA DE SEGURANÇA DISCORD                  ║
║                    por {self.author} - {self.github}                    ║
╚══════════════════════════════════════════════════════════════╝

🎯 FUNDAMENTOS DE SEGURANÇA DISCORD:

🔐 SEGURANÇA DE TOKENS:
   • Nunca compartilhe seus tokens publicamente
   • Use autenticação de dois fatores (2FA) sempre
   • Regenere tokens se suspeitar de compromisso
   • Monitore atividade suspeita em sua conta
   • Evite fazer login em sites não oficiais

🛡️ SEGURANÇA DE SERVIDORES:
   • Aplique o princípio do menor privilégio
   • Revise permissões regularmente
   • Use verificação por telefone em servidores grandes
   • Configure AutoMod para proteção automática
   • Mantenha logs de auditoria habilitados

🔍 PRIVACIDADE DE INFORMAÇÕES:
   • Desabilite widgets públicos desnecessários
   • Use convites temporários quando possível
   • Configure níveis de verificação adequados
   • Monitore informações expostas publicamente
   • Revise configurações de privacidade regularmente

⚡ SEGURANÇA DA API:
   • Implemente rate limiting em aplicações
   • Use HTTPS sempre para comunicação
   • Valide todas as entradas de usuário
   • Implemente retry logic inteligente
   • Monitore performance e disponibilidade

🚨 RESPOSTA A INCIDENTES:
   • Documente todos os incidentes de segurança
   • Notifique usuários afetados rapidamente
   • Implemente correções permanentes
   • Revise políticas após incidentes
   • Treine equipe em práticas de segurança

📚 RECURSOS ADICIONAIS:
   • Discord Safety Center: https://discord.com/safety
   • Discord Developer Docs: https://discord.com/developers/docs
   • OWASP Security Guidelines: https://owasp.org

🏆 MELHORES PRÁTICAS:
   • Mantenha software sempre atualizado
   • Use senhas fortes e únicas
   • Eduque usuários sobre segurança
   • Implemente monitoramento contínuo
   • Pratique response plan regularmente

⚖️ CONSIDERAÇÕES ÉTICAS:
   • Sempre obtenha permissão antes de testar
   • Respeite privacidade de outros usuários
   • Reporte vulnerabilidades responsavelmente
   • Siga termos de serviço da plataforma
   • Contribua para um Discord mais seguro

📧 RECURSOS DE SUPORTE:
   • Discord Support: https://support.discord.com
   • Security Contact: Para questões críticas de segurança
   • Community Guidelines: https://discord.com/guidelines

        """
        print(guide)

    def load_security_module(self, module_name):
        """
        Carrega um módulo de segurança dinamicamente
        """
        try:
            if not os.path.exists(f"{module_name}.py"):
                print(f"❌ Módulo {module_name}.py não encontrado!")
                print(f"Certifique-se de que todos os arquivos estão no mesmo diretório.")
                return None

            spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            return module

        except Exception as e:
            print(f"❌ Erro ao carregar módulo {module_name}: {e}")
            return None

    def run_security_token_analyzer(self):
        """
        Executa o analisador de tokens de segurança
        """
        print("\n" + "="*60)
        print("🔐           SECURITY TOKEN ANALYZER")
        print("="*60)

        module = self.load_security_module("discord_security_analyzer")
        if not module:
            return

        try:
            analyzer = module.DiscordTokenSecurityAnalyzer()
            analyzer.display_banner()

            token = input("Digite seu token Discord para análise de segurança: ")
            if not token:
                print("Token não fornecido.")
                return

            print("\n🔍 Realizando análise estrutural...")
            structural_result = analyzer.analyze_token_structure(token)

            print("\n🛡️ Realizando auditoria de segurança...")
            security_result = analyzer.security_audit_token(token)

            # Combina resultados
            combined_result = {
                "structural_analysis": structural_result,
                "security_audit": security_result
            }

            print("\n📊 RELATÓRIO COMPLETO:")
            print(json.dumps(combined_result, indent=2, ensure_ascii=False))

            # Registra na sessão
            self.session_data["tools_used"].append({
                "tool": "Security Token Analyzer",
                "timestamp": datetime.now().isoformat(),
                "findings": "Análise de token realizada"
            })

        except Exception as e:
            print(f"❌ Erro: {e}")

    def run_permission_auditor(self):
        """
        Executa o auditor de permissões
        """
        print("\n" + "="*60)
        print("🛡️        PERMISSION SECURITY AUDITOR")
        print("="*60)

        module = self.load_security_module("discord_permission_auditor")
        if not module:
            return

        try:
            token = input("Digite seu token Discord: ")
            if not token:
                print("Token não fornecido.")
                return

            auditor = module.DiscordPermissionSecurityAuditor(token)
            auditor.display_banner()

            print("\n📋 Opções de Auditoria:")
            print("1. Auditoria completa de todos os servidores")
            print("2. Auditoria detalhada de servidor específico")

            choice = input("Escolha (1-2): ")

            if choice == "1":
                print("\n🔍 Auditoria completa em progresso...")
                result = auditor.list_accessible_guilds_with_audit()

            elif choice == "2":
                guild_id = input("ID do servidor: ")
                print(f"\n🛡️ Auditoria detalhada - Servidor {guild_id}...")
                result = auditor.audit_guild_permissions(guild_id)

            else:
                print("Opção inválida.")
                return

            print("\n📊 RELATÓRIO DE AUDITORIA:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Registra na sessão
            self.session_data["tools_used"].append({
                "tool": "Permission Security Auditor",
                "timestamp": datetime.now().isoformat(),
                "findings": f"Auditoria de permissões - Opção {choice}"
            })

        except Exception as e:
            print(f"❌ Erro: {e}")

    def run_api_tester(self):
        """
        Executa o testador de segurança da API
        """
        print("\n" + "="*60)
        print("⚡           API SECURITY TESTER")
        print("="*60)

        module = self.load_security_module("discord_api_security_tester")
        if not module:
            return

        try:
            token = input("Digite seu token Discord: ")
            if not token:
                print("Token não fornecido.")
                return

            tester = module.DiscordAPISecurityTester(token)
            tester.display_banner()

            print("\n🔬 Opções de Teste:")
            print("1. Teste de endpoint específico")
            print("2. Suite completa de testes de segurança")

            choice = input("Escolha (1-2): ")

            if choice == "1":
                endpoint = input("Digite o endpoint (ex: /users/@me): ")
                method = input("Método HTTP (GET/POST/PATCH): ").upper()

                print(f"\n🧪 Testando endpoint: {endpoint}")
                result = tester.test_api_consistency(endpoint, method, None, 2)

            elif choice == "2":
                print("\n🧪 Executando suite completa de testes...")
                result = tester.test_common_endpoints()

                # Gera relatório educacional
                educational_result = tester.generate_educational_report(result)
                result = {"test_results": result, "educational_report": educational_result}

            else:
                print("Opção inválida.")
                return

            print("\n📊 RELATÓRIO DE TESTES:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Registra na sessão
            self.session_data["tools_used"].append({
                "tool": "API Security Tester",
                "timestamp": datetime.now().isoformat(),
                "findings": f"Testes de API - Opção {choice}"
            })

        except Exception as e:
            print(f"❌ Erro: {e}")

    def run_info_scanner(self):
        """
        Executa o scanner de segurança de informações
        """
        print("\n" + "="*60)
        print("🔍      INFORMATION SECURITY SCANNER")
        print("="*60)

        module = self.load_security_module("discord_info_security_scanner")
        if not module:
            return

        try:
            scanner = module.DiscordInfoSecurityScanner()
            scanner.display_banner()

            print("\n🔍 Opções de Escaneamento:")
            print("1. Escanear segurança de convite")
            print("2. Escanear widget de servidor")
            print("3. Escaneamento abrangente (múltiplos alvos)")

            choice = input("Escolha (1-3): ")

            if choice == "1":
                invite = input("Digite o código/URL do convite: ")
                print(f"\n🔍 Escaneamento de segurança: {invite}")
                result = scanner.scan_invite_security(invite)

            elif choice == "2":
                guild_id = input("Digite o ID do servidor: ")
                print(f"\n🔍 Escaneamento de widget: {guild_id}")
                result = scanner.scan_guild_widget_security(guild_id)

            elif choice == "3":
                targets_input = input("Digite alvos separados por vírgula: ")
                targets = [t.strip() for t in targets_input.split(",")]
                print(f"\n🔍 Escaneamento abrangente de {len(targets)} alvos...")
                result = scanner.comprehensive_security_scan(targets)

            else:
                print("Opção inválida.")
                return

            print("\n📊 RELATÓRIO DE ESCANEAMENTO:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Registra na sessão
            self.session_data["tools_used"].append({
                "tool": "Information Security Scanner",
                "timestamp": datetime.now().isoformat(),
                "findings": f"Escaneamento - Opção {choice}"
            })

        except Exception as e:
            print(f"❌ Erro: {e}")

    def generate_session_report(self):
        """
        Gera relatório completo da sessão de segurança
        """
        print("\n" + "="*60)
        print("📊           RELATÓRIO DE SEGURANÇA")
        print("="*60)

        session_report = {
            "session_info": {
                "toolkit_version": self.version,
                "created_by": self.author,
                "github": self.github,
                "session_start": self.session_data["session_start"],
                "session_end": datetime.now().isoformat(),
                "duration": self._calculate_session_duration()
            },
            "usage_summary": {
                "tools_used_count": len(self.session_data["tools_used"]),
                "tools_used": self.session_data["tools_used"]
            },
            "security_recommendations": self._generate_session_recommendations(),
            "next_steps": [
                "📚 Revise todas as descobertas de segurança",
                "🔧 Implemente correções necessárias",
                "📊 Monitore mudanças nos perfis de risco",
                "🔄 Execute auditorias regulares",
                "📖 Continue estudando práticas de segurança"
            ]
        }

        print(json.dumps(session_report, indent=2, ensure_ascii=False))

        # Salva relatório
        filename = f"discord_security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_report, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Relatório salvo em: {filename}")
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")

    def _calculate_session_duration(self):
        """Calcula duração da sessão"""
        try:
            start = datetime.fromisoformat(self.session_data["session_start"])
            end = datetime.now()
            duration = end - start
            return str(duration).split('.')[0]  # Remove microsegundos
        except:
            return "Não calculado"

    def _generate_session_recommendations(self):
        """Gera recomendações baseadas no uso da sessão"""
        recommendations = [
            f"🔐 Continue usando as ferramentas do {self.author} regularmente",
            "📊 Documente todas as descobertas de segurança",
            "🛡️ Implemente práticas de segurança proativa",
            "📚 Mantenha-se atualizado sobre novas ameaças",
            f"⭐ Visite {self.github} para atualizações"
        ]

        if len(self.session_data["tools_used"]) >= 3:
            recommendations.append("🏆 Excelente uso da suite - você está no caminho certo!")

        return recommendations

    def change_language(self):
        """
        Opção para alterar idioma (placeholder para futuras versões)
        """
        print("\n🌐 SELEÇÃO DE IDIOMA / LANGUAGE SELECTION")
        print("="*50)
        print("🇧🇷 1. Português (Brasil) - ATUAL")
        print("🇺🇸 2. English (US) - Em desenvolvimento")
        print("🇪🇸 3. Español - Em desenvolvimento") 
        print("🇫🇷 4. Français - Em desenvolvimento")

        choice = input("\nEscolha um idioma / Choose language: ")

        if choice == "1":
            print("✅ Idioma já está em Português!")
        else:
            print("🚧 Outros idiomas estarão disponíveis em versões futuras!")
            print(f"📧 Contribua com traduções em: {self.github}")

    def run_toolkit(self):
        """
        Executa o loop principal da toolkit
        """
        self.display_main_banner()

        print(f"\n👋 Bem-vindo ao Discord Security Toolkit do {self.author}!")
        print(f"🔗 GitHub: {self.github}")
        print("\n⚠️ Lembrete: Use apenas para fins educacionais e recursos próprios!")

        while True:
            try:
                self.display_tools_menu()
                choice = input("\nEscolha uma opção: ").lower().strip()

                if choice == "q":
                    print("\n👋 Encerrando Discord Security Toolkit...")
                    print(f"🙏 Obrigado por usar as ferramentas do {self.author}!")
                    print(f"⭐ Não esqueça de visitar: {self.github}")
                    break

                elif choice == "r":
                    self.generate_session_report()

                elif choice == "h":
                    self.display_security_guide()

                elif choice == "l":
                    self.change_language()

                elif choice in self.tools:
                    tool = self.tools[choice]
                    print(f"\n🚀 Executando {tool['name']}...")

                    if choice == "1":
                        self.run_security_token_analyzer()
                    elif choice == "2":
                        self.run_permission_auditor()
                    elif choice == "3":
                        self.run_api_tester()
                    elif choice == "4":
                        self.run_info_scanner()

                else:
                    print("❌ Opção inválida. Tente novamente.")

                input("\n⏸️  Pressione Enter para continuar...")

            except KeyboardInterrupt:
                print("\n\n👋 Encerrando Discord Security Toolkit...")
                print(f"🙏 Obrigado por usar as ferramentas do {self.author}!")
                break
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    print("Iniciando Discord Security Toolkit...")
    toolkit = DiscordSecurityToolkit()
    toolkit.run_toolkit()
