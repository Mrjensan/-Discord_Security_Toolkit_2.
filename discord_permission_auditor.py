#!/usr/bin/env python3
"""
Discord Permission Security Auditor v2.0
Desenvolvido por Jensan - https://github.com/
Ferramenta para auditoria de segurança de permissões em servidores Discord

AVISO: Use apenas em seus próprios servidores!
Esta ferramenta foi criada para auditoria de segurança pessoal e educacional.
"""

import requests
import json
import time
from datetime import datetime

class DiscordPermissionSecurityAuditor:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://discord.com/api/v9"
        self.headers = {
            "Authorization": f"Bot {token}" if token.startswith('M') else f"{token}",
            "Content-Type": "application/json",
            "User-Agent": f"Discord-Permission-Auditor/2.0 (by Jensan)"
        }
        self.rate_limit_delay = 1
        self.version = "2.0"
        self.author = "Jensan"
        self.github = "https://github.com/"

    def display_banner(self):
        """Exibe banner da ferramenta"""
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║        Discord Permission Security Auditor v{self.version}             ║
║                    Criado por {self.author}                          ║
║                 {self.github}                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔍 Auditoria de Permissões Discord                         ║
║  🛡️ Análise de Segurança de Servidores                      ║
║  📊 Relatórios Detalhados de Permissões                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def audit_guild_permissions(self, guild_id):
        """
        Realiza auditoria completa de permissões em um servidor
        """
        try:
            time.sleep(self.rate_limit_delay)

            url = f"{self.base_url}/guilds/{guild_id}/members/@me"
            response = requests.get(url, headers=self.headers)

            audit_report = {
                "audit_info": {
                    "auditor": self.author,
                    "version": self.version,
                    "github": self.github,
                    "audit_timestamp": datetime.now().isoformat()
                },
                "guild_id": guild_id,
                "permission_analysis": {},
                "security_assessment": {},
                "recommendations": []
            }

            if response.status_code == 200:
                member_data = response.json()

                # Decodifica permissões
                permissions_int = int(member_data.get("permissions", "0"))
                permissions_list = self._decode_permissions(permissions_int)

                audit_report["permission_analysis"] = {
                    "raw_permissions": member_data.get("permissions", "0"),
                    "decoded_permissions": permissions_list,
                    "total_permissions": len(permissions_list),
                    "roles": member_data.get("roles", []),
                    "joined_at": member_data.get("joined_at")
                }

                # Análise de segurança
                security_analysis = self._analyze_permission_security(permissions_list)
                audit_report["security_assessment"] = security_analysis

                # Gera recomendações
                audit_report["recommendations"] = self._generate_security_recommendations(security_analysis)

                audit_report["status"] = "✅ Auditoria concluída com sucesso"

            elif response.status_code == 403:
                audit_report.update({
                    "status": "❌ Acesso negado",
                    "error": "Sem permissão para acessar este servidor",
                    "recommendation": "Verifique se você é membro do servidor"
                })
            elif response.status_code == 404:
                audit_report.update({
                    "status": "❌ Servidor não encontrado",
                    "error": "Servidor não existe ou você não é membro",
                    "recommendation": "Verifique o ID do servidor"
                })
            else:
                audit_report.update({
                    "status": f"⚠️ Erro HTTP {response.status_code}",
                    "error": "Resposta inesperada da API"
                })

            return audit_report

        except Exception as e:
            return {
                "audit_info": {
                    "auditor": self.author,
                    "version": self.version
                },
                "guild_id": guild_id,
                "status": "❌ Erro na auditoria",
                "error": str(e),
                "audit_timestamp": datetime.now().isoformat()
            }

    def _decode_permissions(self, permissions_int):
        """
        Decodifica as permissões numéricas do Discord
        """
        permission_flags = {
            1 << 0: "CREATE_INSTANT_INVITE",
            1 << 1: "KICK_MEMBERS", 
            1 << 2: "BAN_MEMBERS",
            1 << 3: "ADMINISTRATOR",
            1 << 4: "MANAGE_CHANNELS",
            1 << 5: "MANAGE_GUILD",
            1 << 6: "ADD_REACTIONS",
            1 << 7: "VIEW_AUDIT_LOG",
            1 << 8: "PRIORITY_SPEAKER",
            1 << 9: "STREAM",
            1 << 10: "VIEW_CHANNEL",
            1 << 11: "SEND_MESSAGES",
            1 << 12: "SEND_TTS_MESSAGES",
            1 << 13: "MANAGE_MESSAGES",
            1 << 14: "EMBED_LINKS",
            1 << 15: "ATTACH_FILES",
            1 << 16: "READ_MESSAGE_HISTORY",
            1 << 17: "MENTION_EVERYONE",
            1 << 18: "USE_EXTERNAL_EMOJIS",
            1 << 19: "VIEW_GUILD_INSIGHTS",
            1 << 20: "CONNECT",
            1 << 21: "SPEAK",
            1 << 22: "MUTE_MEMBERS",
            1 << 23: "DEAFEN_MEMBERS",
            1 << 24: "MOVE_MEMBERS",
            1 << 25: "USE_VAD",
            1 << 26: "CHANGE_NICKNAME",
            1 << 27: "MANAGE_NICKNAMES",
            1 << 28: "MANAGE_ROLES",
            1 << 29: "MANAGE_WEBHOOKS",
            1 << 30: "MANAGE_EMOJIS_AND_STICKERS"
        }

        active_permissions = []
        for flag, name in permission_flags.items():
            if permissions_int & flag:
                active_permissions.append(name)

        return active_permissions

    def _analyze_permission_security(self, permissions_list):
        """
        Analisa a segurança das permissões atribuídas
        """
        # Classifica permissões por nível de risco
        critical_permissions = [
            "ADMINISTRATOR", "MANAGE_GUILD", "BAN_MEMBERS", 
            "KICK_MEMBERS", "MANAGE_ROLES", "MANAGE_WEBHOOKS"
        ]

        high_risk_permissions = [
            "MANAGE_CHANNELS", "MANAGE_MESSAGES", "MENTION_EVERYONE",
            "VIEW_AUDIT_LOG", "MANAGE_NICKNAMES", "MUTE_MEMBERS", "DEAFEN_MEMBERS"
        ]

        user_critical = [p for p in permissions_list if p in critical_permissions]
        user_high_risk = [p for p in permissions_list if p in high_risk_permissions]

        # Calcula score de risco
        risk_score = len(user_critical) * 20 + len(user_high_risk) * 10
        risk_score = min(risk_score, 100)

        # Determina nível de risco
        if risk_score >= 60:
            risk_level = "🔴 CRÍTICO"
        elif risk_score >= 30:
            risk_level = "🟡 ALTO"
        elif risk_score >= 10:
            risk_level = "🟠 MÉDIO"
        else:
            risk_level = "🟢 BAIXO"

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "critical_permissions": user_critical,
            "high_risk_permissions": user_high_risk,
            "total_permissions": len(permissions_list),
            "security_analysis": {
                "has_admin": "ADMINISTRATOR" in permissions_list,
                "can_manage_server": "MANAGE_GUILD" in permissions_list,
                "can_moderate": any(p in permissions_list for p in ["BAN_MEMBERS", "KICK_MEMBERS"]),
                "can_manage_channels": "MANAGE_CHANNELS" in permissions_list
            }
        }

    def _generate_security_recommendations(self, security_analysis):
        """
        Gera recomendações de segurança baseadas na análise
        """
        recommendations = []

        if security_analysis["security_analysis"]["has_admin"]:
            recommendations.extend([
                "🚨 CRÍTICO: Permissão ADMINISTRATOR detectada",
                "⚠️ Esta permissão concede acesso total ao servidor",
                "🔧 Considere remover e atribuir permissões específicas",
                "📋 Revise regularmente quem possui esta permissão"
            ])

        if security_analysis["security_analysis"]["can_manage_server"]:
            recommendations.extend([
                "⚠️ IMPORTANTE: Permissão MANAGE_GUILD detectada",
                "🔍 Esta permissão permite alterações críticas no servidor",
                "👥 Certifique-se de que apenas administradores confiáveis a possuam"
            ])

        if security_analysis["security_analysis"]["can_moderate"]:
            recommendations.extend([
                "👮 Permissões de moderação detectadas",
                "📝 Estabeleça diretrizes claras para uso",
                "🔄 Monitore ações de moderação nos logs de auditoria"
            ])

        # Recomendações gerais baseadas no nível de risco
        risk_level = security_analysis["risk_level"]

        if "CRÍTICO" in risk_level:
            recommendations.extend([
                "🚨 URGENTE: Nível de risco crítico detectado",
                "🔒 Implemente autenticação de dois fatores (2FA)",
                "📊 Monitore atividade da conta constantemente",
                "👥 Revise todas as permissões imediatamente"
            ])
        elif "ALTO" in risk_level:
            recommendations.extend([
                "⚠️ Nível de risco alto - atenção necessária",
                "🔍 Revise permissões desnecessárias",
                "📝 Documente justificativa para cada permissão"
            ])
        else:
            recommendations.append("✅ Configuração de permissões aparenta estar segura")

        # Sempre incluir recomendações gerais
        recommendations.extend([
            "📚 Eduque-se sobre princípio do menor privilégio",
            "🔄 Revise permissões periodicamente",
            "📊 Use logs de auditoria para monitorar atividade"
        ])

        return recommendations

    def list_accessible_guilds_with_audit(self):
        """
        Lista servidores acessíveis com análise de segurança
        """
        try:
            time.sleep(self.rate_limit_delay)

            url = f"{self.base_url}/users/@me/guilds"
            response = requests.get(url, headers=self.headers)

            audit_report = {
                "audit_info": {
                    "auditor": self.author,
                    "version": self.version,
                    "github": self.github,
                    "audit_timestamp": datetime.now().isoformat()
                },
                "guild_summary": {},
                "detailed_analysis": []
            }

            if response.status_code == 200:
                guilds = response.json()

                total_guilds = len(guilds)
                total_owned = sum(1 for g in guilds if g.get("owner", False))
                high_risk_guilds = 0

                for guild in guilds:
                    permissions = self._decode_permissions(int(guild.get("permissions", "0")))
                    security_analysis = self._analyze_permission_security(permissions)

                    if "CRÍTICO" in security_analysis["risk_level"] or "ALTO" in security_analysis["risk_level"]:
                        high_risk_guilds += 1

                    guild_analysis = {
                        "id": guild["id"],
                        "name": guild["name"],
                        "owner": guild.get("owner", False),
                        "permissions_count": len(permissions),
                        "risk_level": security_analysis["risk_level"],
                        "risk_score": security_analysis["risk_score"],
                        "critical_permissions": security_analysis["critical_permissions"]
                    }

                    audit_report["detailed_analysis"].append(guild_analysis)

                audit_report["guild_summary"] = {
                    "total_guilds": total_guilds,
                    "owned_guilds": total_owned,
                    "high_risk_guilds": high_risk_guilds,
                    "overall_risk": "🔴 ALTO" if high_risk_guilds > total_guilds * 0.3 else "🟢 BAIXO"
                }

                audit_report["status"] = "✅ Auditoria de servidores concluída"

            else:
                audit_report.update({
                    "status": f"❌ Erro HTTP {response.status_code}",
                    "error": "Não foi possível listar servidores"
                })

            return audit_report

        except Exception as e:
            return {
                "audit_info": {
                    "auditor": self.author,
                    "version": self.version
                },
                "status": "❌ Erro na auditoria",
                "error": str(e),
                "audit_timestamp": datetime.now().isoformat()
            }

# Exemplo de uso
if __name__ == "__main__":
    print("Discord Permission Security Auditor")
    print(f"Desenvolvido por Jensan - https://github.com/")
    print("AVISO: Use apenas em seus próprios servidores!")
    print("Esta ferramenta é para auditoria de segurança pessoal!")

    try:
        token = input("\nDigite seu token Discord: ")
        if not token:
            print("Token não fornecido. Saindo...")
            exit()

        auditor = DiscordPermissionSecurityAuditor(token)
        auditor.display_banner()

        print("\n🔍 Opções de Auditoria:")
        print("1. Listar todos os servidores com análise de risco")
        print("2. Auditoria detalhada de servidor específico")

        choice = input("\nEscolha uma opção (1-2): ")

        if choice == "1":
            print("\n📊 Realizando auditoria de todos os servidores...")
            result = auditor.list_accessible_guilds_with_audit()

        elif choice == "2":
            guild_id = input("Digite o ID do servidor: ")
            print(f"\n🛡️ Auditoria de segurança - Servidor {guild_id}...")
            result = auditor.audit_guild_permissions(guild_id)

        else:
            print("Opção inválida!")
            exit()

        print("\n" + "="*70)
        print("📋 RELATÓRIO DE AUDITORIA DE SEGURANÇA")
        print("="*70)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except KeyboardInterrupt:
        print("\n\n👋 Auditoria interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")

    print(f"\n🙏 Obrigado por usar a ferramenta do Jensan!")
    print("⭐ GitHub: https://github.com/")
