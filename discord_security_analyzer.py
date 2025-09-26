#!/usr/bin/env python3
"""
Discord Token Security Analyzer v2.0
Desenvolvido por Jensan - https://github.com/
Ferramenta educacional para análise de segurança de tokens Discord

AVISO: Use apenas com seus próprios tokens!
Esta ferramenta foi criada para fins educacionais e auditoria de segurança pessoal.
"""

import base64
import json
import re
from datetime import datetime
import hashlib

class DiscordTokenSecurityAnalyzer:
    def __init__(self):
        self.token_pattern = r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}'
        self.version = "2.0"
        self.author = "Jensan"
        self.github = "https://github.com/"

    def display_banner(self):
        """Exibe banner da ferramenta"""
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║           Discord Token Security Analyzer v{self.version}              ║
║                    Criado por {self.author}                          ║
║                 {self.github}                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔐 Ferramenta de Análise de Segurança                      ║
║  📊 Análise estrutural de tokens Discord                    ║
║  🛡️ Auditoria de segurança pessoal                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def analyze_token_structure(self, token):
        """
        Analisa a estrutura de um token Discord para fins educacionais
        """
        if not self.is_valid_token_format(token):
            return {"error": "Formato de token inválido"}

        parts = token.split('.')
        if len(parts) != 3:
            return {"error": "Token deve ter 3 partes separadas por ponto"}

        try:
            # Decodifica a primeira parte (user ID)
            user_id_encoded = parts[0]
            user_id = base64.b64decode(user_id_encoded + '==').decode('utf-8')

            # Analisa timestamp da segunda parte
            timestamp_encoded = parts[1]

            # Hash do token para identificação segura (sem revelar)
            token_hash = hashlib.sha256(token.encode()).hexdigest()[:16]

            return {
                "analysis_info": {
                    "analyzer_version": self.version,
                    "created_by": self.author,
                    "github": self.github
                },
                "token_info": {
                    "user_id": user_id,
                    "timestamp_part": timestamp_encoded,
                    "hmac_part": parts[2][:10] + "..." if len(parts[2]) > 10 else parts[2],
                    "token_hash": token_hash,
                    "is_bot": user_id_encoded.startswith('M'),
                    "token_type": "Bot Token" if user_id_encoded.startswith('M') else "User Token",
                },
                "security_analysis": {
                    "format_valid": True,
                    "structure_intact": True,
                    "token_age": self._estimate_token_age(timestamp_encoded),
                    "security_recommendations": self._get_security_recommendations(user_id_encoded.startswith('M'))
                },
                "analysis_timestamp": datetime.now().isoformat(),
                "disclaimer": "NUNCA compartilhe este token com ninguém!"
            }

        except Exception as e:
            return {"error": f"Erro na análise: {str(e)}"}

    def _estimate_token_age(self, timestamp_encoded):
        """Estima idade do token baseado no timestamp"""
        try:
            # Discord epoch (2015-01-01)
            discord_epoch = 1420070400000
            timestamp_bytes = base64.b64decode(timestamp_encoded + '==')

            if len(timestamp_bytes) >= 4:
                # Aproximação baseada nos primeiros bytes
                return "Token parece ser recente (análise aproximada)"
            else:
                return "Não foi possível determinar idade"
        except:
            return "Análise de idade não disponível"

    def _get_security_recommendations(self, is_bot):
        """Gera recomendações de segurança"""
        base_recommendations = [
            "🔐 Nunca compartilhe seu token publicamente",
            "🔄 Regenere o token se suspeitar de vazamento", 
            "📝 Monitore uso não autorizado da conta",
            "🛡️ Use autenticação de dois fatores (2FA)"
        ]

        if is_bot:
            base_recommendations.extend([
                "🤖 Mantenha permissões de bot no mínimo necessário",
                "📊 Monitore logs de atividade do bot",
                "🏠 Hospede bots em ambiente seguro"
            ])
        else:
            base_recommendations.extend([
                "👤 Evite fazer login em sites não oficiais",
                "🚫 Não execute scripts desconhecidos no console",
                "📱 Use o aplicativo oficial quando possível"
            ])

        return base_recommendations

    def is_valid_token_format(self, token):
        """Verifica se o token tem formato válido"""
        return bool(re.match(self.token_pattern, token))

    def security_audit_token(self, token):
        """
        Realiza auditoria de segurança do token
        """
        import requests

        headers = {
            "Authorization": f"Bot {token}" if token.startswith('M') else f"{token}",
            "Content-Type": "application/json",
            "User-Agent": f"Discord-Token-Analyzer/{self.version} (by {self.author})"
        }

        try:
            # Testa endpoint básico
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)

            audit_result = {
                "audit_info": {
                    "auditor": self.author,
                    "version": self.version,
                    "github": self.github
                },
                "token_validity": {},
                "security_assessment": {},
                "recommendations": []
            }

            if response.status_code == 200:
                user_data = response.json()

                audit_result["token_validity"] = {
                    "status": "✅ Token válido e ativo",
                    "account_info": {
                        "username": user_data.get("username", "N/A"),
                        "id": user_data.get("id", "N/A"),
                        "verified": user_data.get("verified", False),
                        "mfa_enabled": user_data.get("mfa_enabled", False),
                        "avatar": "Presente" if user_data.get("avatar") else "Ausente"
                    }
                }

                # Análise de segurança
                mfa_enabled = user_data.get("mfa_enabled", False)
                verified = user_data.get("verified", False)

                audit_result["security_assessment"] = {
                    "mfa_status": "✅ Habilitado" if mfa_enabled else "⚠️ Desabilitado",
                    "account_verified": "✅ Verificada" if verified else "❌ Não verificada",
                    "security_score": self._calculate_security_score(mfa_enabled, verified),
                    "risk_level": self._assess_risk_level(mfa_enabled, verified)
                }

                # Recomendações personalizadas
                if not mfa_enabled:
                    audit_result["recommendations"].append("🚨 CRÍTICO: Habilite 2FA imediatamente")

                if not verified:
                    audit_result["recommendations"].append("📧 Verifique sua conta via email")

                audit_result["recommendations"].extend([
                    "🔍 Monitore atividade suspeita na conta",
                    "🔄 Considere regenerar token periodicamente",
                    "📱 Use Discord oficial sempre que possível"
                ])

            elif response.status_code == 401:
                audit_result["token_validity"] = {
                    "status": "❌ Token inválido ou expirado",
                    "action_required": "Gerar novo token"
                }

            elif response.status_code == 429:
                audit_result["token_validity"] = {
                    "status": "⏱️ Rate limit atingido",
                    "action_required": "Aguardar antes de nova verificação"
                }

            else:
                audit_result["token_validity"] = {
                    "status": f"⚠️ Resposta inesperada: HTTP {response.status_code}",
                    "action_required": "Verificar manualmente"
                }

            audit_result["audit_timestamp"] = datetime.now().isoformat()
            return audit_result

        except requests.RequestException as e:
            return {
                "audit_info": {
                    "auditor": self.author,
                    "version": self.version
                },
                "error": f"Erro na verificação: {str(e)}",
                "audit_timestamp": datetime.now().isoformat()
            }

    def _calculate_security_score(self, mfa_enabled, verified):
        """Calcula score de segurança (0-100)"""
        score = 50  # Base

        if mfa_enabled:
            score += 30
        if verified:
            score += 20

        return min(score, 100)

    def _assess_risk_level(self, mfa_enabled, verified):
        """Avalia nível de risco"""
        if mfa_enabled and verified:
            return "🟢 BAIXO"
        elif mfa_enabled or verified:
            return "🟡 MÉDIO"  
        else:
            return "🔴 ALTO"

# Exemplo de uso APENAS para seus próprios tokens
if __name__ == "__main__":
    analyzer = DiscordTokenSecurityAnalyzer()
    analyzer.display_banner()

    print("AVISO: Esta ferramenta é para auditoria de segurança pessoal apenas!")
    print(f"Desenvolvida por {analyzer.author} - {analyzer.github}")
    print("Use apenas com seus próprios tokens Discord!")
    print("Pressione Ctrl+C para sair\n")

    try:
        token = input("Digite seu token Discord (apenas para análise de segurança): ")

        if not token:
            print("Token não fornecido. Saindo...")
            exit()

        print("\n" + "="*60)
        print("📊 ANÁLISE ESTRUTURAL")
        print("="*60)
        result = analyzer.analyze_token_structure(token)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # Auditoria de segurança (opcional)
        audit_choice = input("\nRealizar auditoria de segurança do token? (s/n): ").lower()
        if audit_choice == 's':
            print("\n" + "="*60)
            print("🛡️ AUDITORIA DE SEGURANÇA")
            print("="*60)
            audit_result = analyzer.security_audit_token(token)
            print(json.dumps(audit_result, indent=2, ensure_ascii=False))

    except KeyboardInterrupt:
        print("\n\n👋 Encerrando análise...")
    except Exception as e:
        print(f"❌ Erro: {e}")

    print(f"\n🙏 Obrigado por usar a ferramenta do {analyzer.author}!")
    print(f"⭐ Visite: {analyzer.github}")
