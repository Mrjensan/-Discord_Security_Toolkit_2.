#!/usr/bin/env python3
"""
Discord Information Security Scanner v2.0
Desenvolvido por Jensan - https://github.com/
Ferramenta educacional para análise de segurança de informações Discord

AVISO: Use apenas para fins educacionais e análise ética!
Esta ferramenta analisa informações publicamente disponíveis para fins de segurança.
"""

import requests
import json
import re
import time
from datetime import datetime
from urllib.parse import urlparse

class DiscordInfoSecurityScanner:
    def __init__(self):
        self.base_url = "https://discord.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'Discord-Info-Security-Scanner/2.0 (by Jensan)'
        })
        self.version = "2.0"
        self.author = "Jensan"
        self.github = "https://github.com/"

    def display_banner(self):
        """Exibe banner da ferramenta"""
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║        Discord Information Security Scanner v{self.version}          ║
║                    Criado por {self.author}                          ║
║                 {self.github}                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔍 Scanner de Informações Públicas Discord                 ║
║  🛡️ Análise de Segurança e Privacidade                      ║
║  📊 Relatórios de Exposição de Dados                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def scan_invite_security(self, invite_code):
        """
        Escaneia informações de segurança em convites Discord
        """
        # Remove URL se fornecida completa
        if '/' in invite_code:
            invite_code = invite_code.split('/')[-1]

        url = f"{self.base_url}/api/v9/invites/{invite_code}"

        scan_report = {
            "scan_info": {
                "scanner": self.author,
                "version": self.version,
                "github": self.github,
                "scan_timestamp": datetime.now().isoformat(),
                "scan_type": "Public Invite Analysis"
            },
            "invite_code": invite_code,
            "security_analysis": {}
        }

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Extrai informações expostas
                guild_info = data.get("guild", {})
                channel_info = data.get("channel", {})
                inviter_info = data.get("inviter", {})

                exposed_data = {
                    "guild_information": {
                        "name": guild_info.get("name"),
                        "id": guild_info.get("id"),
                        "description": guild_info.get("description"),
                        "member_count": data.get("approximate_member_count"),
                        "online_count": data.get("approximate_presence_count"),
                        "verification_level": guild_info.get("verification_level"),
                        "has_vanity_url": bool(guild_info.get("vanity_url_code"))
                    },
                    "channel_information": {
                        "name": channel_info.get("name"),
                        "type": channel_info.get("type"),
                        "id": channel_info.get("id")
                    },
                    "inviter_information": {
                        "username": inviter_info.get("username"),
                        "discriminator": inviter_info.get("discriminator"),
                        "id": inviter_info.get("id"),
                        "has_avatar": bool(inviter_info.get("avatar"))
                    },
                    "invite_metadata": {
                        "expires_at": data.get("expires_at"),
                        "created_at": data.get("created_at"),
                        "uses": data.get("uses"),
                        "max_uses": data.get("max_uses")
                    }
                }

                # Análise de segurança
                security_assessment = self._assess_invite_security(exposed_data)

                scan_report.update({
                    "scan_status": "✅ Convite encontrado e analisado",
                    "exposed_data": exposed_data,
                    "security_analysis": security_assessment
                })

            elif response.status_code == 404:
                scan_report.update({
                    "scan_status": "❌ Convite não encontrado",
                    "message": "Convite pode ter expirado ou ser inválido",
                    "security_note": "Convites inexistentes são seguros por definição"
                })

            elif response.status_code == 429:
                scan_report.update({
                    "scan_status": "⏱️ Rate limit atingido", 
                    "message": "Aguarde antes de tentar novamente",
                    "recommendation": "Respeite os limites da API"
                })

            else:
                scan_report.update({
                    "scan_status": f"⚠️ Resposta inesperada: HTTP {response.status_code}",
                    "message": "Verificação manual necessária"
                })

        except Exception as e:
            scan_report.update({
                "scan_status": "❌ Erro no escaneamento",
                "error": str(e),
                "error_type": type(e).__name__
            })

        return scan_report

    def _assess_invite_security(self, exposed_data):
        """
        Avalia segurança das informações expostas
        """
        security_issues = []
        privacy_concerns = []
        recommendations = []

        guild_info = exposed_data.get("guild_information", {})
        inviter_info = exposed_data.get("inviter_information", {})

        # Analisa exposição do servidor
        if guild_info.get("description"):
            privacy_concerns.append("Descrição do servidor exposta publicamente")

        if guild_info.get("has_vanity_url"):
            privacy_concerns.append("URL personalizada exposta")

        member_count = guild_info.get("member_count", 0)
        if member_count and member_count > 10000:
            security_issues.append(f"Servidor grande ({member_count:,} membros) - alvo atrativo")
        elif member_count and member_count < 10:
            privacy_concerns.append("Servidor muito pequeno - pode ser privado")

        # Analisa exposição do criador do convite
        if inviter_info.get("username"):
            privacy_concerns.append("Informações do criador do convite expostas")
            recommendations.append("Considere criar convites anônimos quando possível")

        # Calcula score de privacidade (0-100)
        privacy_score = 100
        privacy_score -= len(security_issues) * 20
        privacy_score -= len(privacy_concerns) * 10
        privacy_score = max(privacy_score, 0)

        # Determina nível de risco
        if privacy_score >= 80:
            risk_level = "🟢 BAIXO"
        elif privacy_score >= 60:
            risk_level = "🟡 MÉDIO"
        elif privacy_score >= 40:
            risk_level = "🟠 ALTO"
        else:
            risk_level = "🔴 CRÍTICO"

        # Recomendações gerais
        base_recommendations = [
            "📝 Revise configurações de privacidade do servidor",
            "🔍 Monitore quem cria convites públicos",
            "⏰ Use convites temporários quando possível",
            "🛡️ Configure níveis de verificação adequados"
        ]

        recommendations.extend(base_recommendations)

        return {
            "privacy_score": privacy_score,
            "risk_level": risk_level,
            "security_issues": security_issues,
            "privacy_concerns": privacy_concerns,
            "recommendations": recommendations,
            "total_issues": len(security_issues) + len(privacy_concerns)
        }

    def scan_guild_widget_security(self, guild_id):
        """
        Escaneia segurança do widget público do servidor
        """
        url = f"{self.base_url}/api/guilds/{guild_id}/widget.json"

        scan_report = {
            "scan_info": {
                "scanner": self.author,
                "version": self.version,
                "github": self.github,
                "scan_timestamp": datetime.now().isoformat(),
                "scan_type": "Guild Widget Security Analysis"
            },
            "guild_id": guild_id
        }

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Analisa exposição de dados
                exposed_channels = data.get("channels", [])
                exposed_members = data.get("members", [])

                channel_exposure = []
                for channel in exposed_channels[:10]:  # Limita output
                    channel_exposure.append({
                        "name": channel.get("name"),
                        "id": channel.get("id"),
                        "position": channel.get("position")
                    })

                member_exposure = []
                for member in exposed_members[:10]:  # Limita output  
                    member_exposure.append({
                        "username": member.get("username"),
                        "id": member.get("id"),
                        "status": member.get("status"),
                        "discriminator": member.get("discriminator")
                    })

                # Análise de segurança
                security_assessment = self._assess_widget_security(
                    len(exposed_channels), len(exposed_members), data
                )

                scan_report.update({
                    "scan_status": "⚠️ Widget público habilitado",
                    "server_info": {
                        "name": data.get("name"),
                        "id": data.get("id")
                    },
                    "exposure_analysis": {
                        "channels_exposed": len(exposed_channels),
                        "members_exposed": len(exposed_members),
                        "sample_channels": channel_exposure,
                        "sample_members": member_exposure
                    },
                    "security_analysis": security_assessment
                })

            elif response.status_code == 403:
                scan_report.update({
                    "scan_status": "✅ Widget desabilitado",
                    "message": "Configuração segura - widget público desabilitado",
                    "security_note": "Esta é a configuração recomendada para privacidade"
                })

            else:
                scan_report.update({
                    "scan_status": f"⚠️ Resposta inesperada: HTTP {response.status_code}",
                    "message": "Widget pode estar desabilitado ou servidor inacessível"
                })

        except Exception as e:
            scan_report.update({
                "scan_status": "❌ Erro no escaneamento",
                "error": str(e)
            })

        return scan_report

    def _assess_widget_security(self, channel_count, member_count, widget_data):
        """
        Avalia segurança do widget público
        """
        security_issues = []
        recommendations = []

        # Avalia exposição de membros
        if member_count > 0:
            security_issues.append(f"Lista de {member_count} membros exposta publicamente")
            recommendations.append("🚨 CRÍTICO: Desabilite exposição de membros")

        # Avalia exposição de canais
        if channel_count > 5:
            security_issues.append(f"Estrutura de {channel_count} canais exposta")
            recommendations.append("🔍 Revise quais canais devem ser públicos")

        # Verifica se há convite instantâneo
        if widget_data.get("instant_invite"):
            security_issues.append("Convite instantâneo disponível no widget")
            recommendations.append("⚠️ Monitore uso do convite automático")

        # Calcula score de segurança
        security_score = 100
        security_score -= len(security_issues) * 25
        security_score = max(security_score, 0)

        # Determina nível de risco
        if security_score >= 80:
            risk_level = "🟢 BAIXO"
        elif security_score >= 60:
            risk_level = "🟡 MÉDIO"  
        else:
            risk_level = "🔴 ALTO"

        # Recomendações base
        base_recommendations = [
            "🛡️ Considere desabilitar widget público",
            "👥 Nunca exponha lista de membros",
            "📋 Limite canais visíveis no widget",
            "🔄 Revise configurações regularmente"
        ]

        recommendations.extend(base_recommendations)

        return {
            "security_score": security_score,
            "risk_level": risk_level,
            "security_issues": security_issues,
            "recommendations": recommendations,
            "widget_enabled": True,
            "members_exposed": member_count > 0,
            "channels_exposed": channel_count > 0
        }

    def comprehensive_security_scan(self, targets):
        """
        Realiza escaneamento abrangente de múltiplos alvos
        """
        comprehensive_report = {
            "scan_suite_info": {
                "scanner": self.author,
                "version": self.version,
                "github": self.github,
                "suite_timestamp": datetime.now().isoformat(),
                "total_targets": len(targets)
            },
            "individual_scans": [],
            "consolidated_analysis": {}
        }

        high_risk_count = 0
        total_issues = 0

        for target in targets:
            print(f"🔍 Escaneando: {target}")

            # Determina tipo de alvo e escaneia apropriadamente
            if target.startswith(('http', 'discord.gg', 'discord.com')):
                # É um convite
                invite_code = target.split('/')[-1]
                scan_result = self.scan_invite_security(invite_code)
                scan_result["target_type"] = "invite"

            elif len(target) > 15 and target.isdigit():
                # É um Guild ID
                scan_result = self.scan_guild_widget_security(target)
                scan_result["target_type"] = "guild_widget"

            else:
                # Tenta como código de convite
                scan_result = self.scan_invite_security(target)
                scan_result["target_type"] = "invite"

            comprehensive_report["individual_scans"].append(scan_result)

            # Contabiliza para análise consolidada
            if "security_analysis" in scan_result:
                risk_level = scan_result["security_analysis"].get("risk_level", "")
                if "ALTO" in risk_level or "CRÍTICO" in risk_level:
                    high_risk_count += 1
                total_issues += scan_result["security_analysis"].get("total_issues", 0)

            # Pausa respeitosa entre escaneamentos
            time.sleep(2)

        # Análise consolidada
        comprehensive_report["consolidated_analysis"] = {
            "high_risk_targets": high_risk_count,
            "total_security_issues": total_issues,
            "average_issues_per_target": total_issues / len(targets) if targets else 0,
            "overall_security_posture": self._assess_overall_security(high_risk_count, len(targets)),
            "top_recommendations": self._get_top_security_recommendations()
        }

        return comprehensive_report

    def _assess_overall_security(self, high_risk_count, total_targets):
        """Avalia postura geral de segurança"""
        if high_risk_count == 0:
            return "🟢 BOA - Nenhum risco alto detectado"
        elif high_risk_count <= total_targets * 0.3:
            return "🟡 MODERADA - Alguns riscos identificados"
        else:
            return "🔴 CRÍTICA - Múltiplos riscos altos detectados"

    def _get_top_security_recommendations(self):
        """Retorna recomendações principais de segurança"""
        return [
            "🔐 Desabilite widgets públicos desnecessários",
            "👥 Nunca exponha listas de membros publicamente", 
            "⏰ Use convites temporários sempre que possível",
            "🛡️ Configure níveis de verificação adequados",
            "🔄 Revise configurações de privacidade regularmente",
            "📊 Monitore exposição de informações sensíveis"
        ]

# Exemplo de uso educacional
if __name__ == "__main__":
    print("Discord Information Security Scanner - Ferramenta Educacional")
    print(f"Desenvolvido por Jensan - https://github.com/")
    print("AVISO: Para análise educacional de informações públicas apenas!")

    try:
        scanner = DiscordInfoSecurityScanner()
        scanner.display_banner()

        print("\n🔍 Opções de Escaneamento:")
        print("1. Escanear convite específico")
        print("2. Escanear widget de servidor")
        print("3. Escaneamento abrangente (múltiplos alvos)")

        choice = input("\nEscolha uma opção (1-3): ")

        if choice == "1":
            invite = input("Digite o código/URL do convite: ")
            print(f"\n🔍 Escaneando convite: {invite}")
            result = scanner.scan_invite_security(invite)

        elif choice == "2":
            guild_id = input("Digite o ID do servidor: ")
            print(f"\n🔍 Escaneando widget do servidor: {guild_id}")
            result = scanner.scan_guild_widget_security(guild_id)

        elif choice == "3":
            targets_input = input("Digite alvos separados por vírgula (convites/IDs): ")
            targets = [t.strip() for t in targets_input.split(",")]
            print(f"\n🔍 Escaneamento abrangente de {len(targets)} alvos...")
            result = scanner.comprehensive_security_scan(targets)

        else:
            print("Opção inválida!")
            exit()

        print("\n" + "="*70)
        print("📊 RELATÓRIO DE SEGURANÇA")
        print("="*70)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except KeyboardInterrupt:
        print("\n\n👋 Escaneamento interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")

    print(f"\n🛡️ Obrigado por usar a ferramenta de segurança do Jensan!")
    print("⭐ GitHub: https://github.com/")
