#!/usr/bin/env python3
"""
Discord API Security Tester v2.0
Desenvolvido por Jensan - https://github.com/
Ferramenta educacional para teste de segurança da API Discord

AVISO: Use apenas para fins educacionais e testes éticos!
Esta ferramenta testa a robustez da API Discord de forma responsável.
"""

import requests
import threading
import time
import json
from datetime import datetime
import statistics

class DiscordAPISecurityTester:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://discord.com/api/v9"
        self.headers = {
            "Authorization": f"Bot {token}" if token.startswith('M') else f"{token}",
            "Content-Type": "application/json",
            "User-Agent": f"Discord-API-Security-Tester/2.0 (by Jensan)"
        }
        self.results = []
        self.lock = threading.Lock()
        self.version = "2.0"
        self.author = "Jensan"
        self.github = "https://github.com/"

    def display_banner(self):
        """Exibe banner da ferramenta"""
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║           Discord API Security Tester v{self.version}               ║
║                    Criado por {self.author}                          ║
║                 {self.github}                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔬 Teste de Robustez da API Discord                        ║
║  ⚡ Análise de Performance e Consistência                    ║
║  📊 Relatórios Técnicos Detalhados                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def test_api_consistency(self, endpoint, method="GET", data=None, threads=2, delay=0.5):
        """
        Testa consistência da API com múltiplas requisições
        LIMITADO para ser educacional e responsável
        """
        # Limita threads para ser responsável
        threads = min(threads, 2)

        url = f"{self.base_url}{endpoint}" if not endpoint.startswith('http') else endpoint

        test_info = {
            "test_info": {
                "tester": self.author,
                "version": self.version,
                "github": self.github,
                "test_timestamp": datetime.now().isoformat()
            },
            "test_parameters": {
                "endpoint": endpoint,
                "method": method,
                "threads": threads,
                "delay": delay,
                "responsible_testing": True
            }
        }

        def make_request(thread_id):
            try:
                start_time = time.time()

                if method.upper() == "GET":
                    response = requests.get(url, headers=self.headers, timeout=10)
                elif method.upper() == "POST":
                    response = requests.post(url, headers=self.headers, json=data, timeout=10)
                elif method.upper() == "PATCH":
                    response = requests.patch(url, headers=self.headers, json=data, timeout=10)
                else:
                    raise ValueError(f"Método não suportado: {method}")

                end_time = time.time()

                with self.lock:
                    self.results.append({
                        "thread_id": thread_id,
                        "status_code": response.status_code,
                        "response_time": end_time - start_time,
                        "response_size": len(response.content),
                        "timestamp": start_time,
                        "rate_limit_info": {
                            "remaining": response.headers.get("X-RateLimit-Remaining"),
                            "reset": response.headers.get("X-RateLimit-Reset"),
                            "limit": response.headers.get("X-RateLimit-Limit")
                        },
                        "server_info": {
                            "server": response.headers.get("Server"),
                            "cf_ray": response.headers.get("CF-Ray"),
                            "content_type": response.headers.get("Content-Type")
                        }
                    })

            except Exception as e:
                with self.lock:
                    self.results.append({
                        "thread_id": thread_id,
                        "error": str(e),
                        "timestamp": time.time(),
                        "error_type": type(e).__name__
                    })

        # Limpa resultados anteriores
        self.results = []

        print(f"🧪 Testando consistência da API...")
        print(f"📡 Endpoint: {endpoint}")
        print(f"🔧 Método: {method}")
        print(f"🧵 Threads: {threads} (limitado para ser responsável)")
        print("⚠️ Testando de forma educacional e ética")

        # Cria e inicia threads
        thread_list = []
        start_time = time.time()

        for i in range(threads):
            t = threading.Thread(target=make_request, args=(i+1,))
            thread_list.append(t)
            t.start()
            time.sleep(delay)  # Delay responsável

        # Aguarda conclusão
        for t in thread_list:
            t.join()

        total_time = time.time() - start_time

        # Compila resultado do teste
        test_result = {
            **test_info,
            "test_results": {
                "total_execution_time": total_time,
                "individual_results": self.results,
                "analysis": self._analyze_api_consistency()
            }
        }

        return test_result

    def _analyze_api_consistency(self):
        """
        Analisa os resultados para avaliar consistência da API
        """
        if not self.results:
            return {"error": "Nenhum resultado para analisar"}

        # Separa resultados com sucesso e erros
        successful_results = [r for r in self.results if "status_code" in r]
        error_results = [r for r in self.results if "error" in r]

        if not successful_results:
            return {
                "analysis_status": "❌ Todos os testes falharam",
                "total_errors": len(error_results),
                "errors": error_results[:3],  # Limita output
                "recommendations": [
                    "Verificar conectividade de rede",
                    "Confirmar validade do token",
                    "Revisar endpoint testado"
                ]
            }

        # Métricas de performance
        response_times = [r["response_time"] for r in successful_results]
        status_codes = [r["status_code"] for r in successful_results]
        response_sizes = [r["response_size"] for r in successful_results]

        # Análise estatística
        analysis = {
            "performance_metrics": {
                "total_requests": len(self.results),
                "successful_requests": len(successful_results),
                "failed_requests": len(error_results),
                "success_rate": (len(successful_results) / len(self.results)) * 100
            },
            "response_time_analysis": {
                "min_ms": min(response_times) * 1000,
                "max_ms": max(response_times) * 1000,
                "average_ms": statistics.mean(response_times) * 1000,
                "median_ms": statistics.median(response_times) * 1000
            },
            "consistency_analysis": {
                "unique_status_codes": len(set(status_codes)),
                "status_code_distribution": {},
                "response_size_variance": len(set(response_sizes)) > 1
            },
            "api_health_indicators": [],
            "educational_insights": []
        }

        # Distribui códigos de status
        for code in status_codes:
            analysis["consistency_analysis"]["status_code_distribution"][code] =                 analysis["consistency_analysis"]["status_code_distribution"].get(code, 0) + 1

        # Rate limiting analysis
        rate_limit_data = [r.get("rate_limit_info", {}) for r in successful_results]
        remaining_calls = [int(data.get("remaining", 0)) for data in rate_limit_data if data.get("remaining")]

        if remaining_calls:
            analysis["rate_limiting"] = {
                "average_remaining": statistics.mean(remaining_calls),
                "min_remaining": min(remaining_calls),
                "rate_limited": any(x <= 5 for x in remaining_calls)
            }

        # Gera insights educacionais
        if len(set(status_codes)) == 1 and status_codes[0] == 200:
            analysis["educational_insights"].append("✅ API respondeu consistentemente")
            analysis["educational_insights"].append("📊 Comportamento estável detectado")

        if len(set(response_sizes)) > 1:
            analysis["educational_insights"].append("📏 Variação no tamanho das respostas")
            analysis["educational_insights"].append("🔍 Pode indicar dados dinâmicos")

        # Avalia saúde da API
        if analysis["performance_metrics"]["success_rate"] >= 95:
            analysis["api_health_indicators"].append("🟢 Alta disponibilidade")
        elif analysis["performance_metrics"]["success_rate"] >= 80:
            analysis["api_health_indicators"].append("🟡 Disponibilidade moderada")
        else:
            analysis["api_health_indicators"].append("🔴 Problemas de disponibilidade")

        avg_response_time = statistics.mean(response_times) * 1000
        if avg_response_time < 200:
            analysis["api_health_indicators"].append("⚡ Excelente tempo de resposta")
        elif avg_response_time < 500:
            analysis["api_health_indicators"].append("🟡 Tempo de resposta adequado")
        else:
            analysis["api_health_indicators"].append("🐌 Tempo de resposta lento")

        return analysis

    def test_common_endpoints(self):
        """
        Testa endpoints comuns do Discord para fins educacionais
        """
        common_endpoints = [
            {
                "name": "User Profile",
                "endpoint": "/users/@me",
                "method": "GET",
                "description": "Testa endpoint de perfil do usuário"
            },
            {
                "name": "Guild List",
                "endpoint": "/users/@me/guilds",
                "method": "GET", 
                "description": "Testa listagem de servidores"
            }
        ]

        test_suite_results = {
            "test_suite_info": {
                "tester": self.author,
                "version": self.version,
                "github": self.github,
                "suite_timestamp": datetime.now().isoformat(),
                "total_tests": len(common_endpoints)
            },
            "individual_tests": []
        }

        for endpoint_test in common_endpoints:
            print(f"\n🧪 Testando: {endpoint_test['name']}")
            print(f"📝 {endpoint_test['description']}")

            test_result = self.test_api_consistency(
                endpoint=endpoint_test["endpoint"],
                method=endpoint_test["method"],
                threads=2,
                delay=1.0  # Mais conservador
            )

            test_suite_results["individual_tests"].append({
                "test_name": endpoint_test["name"],
                "result": test_result
            })

            # Pausa entre testes para ser responsável
            time.sleep(2)

        # Análise consolidada
        successful_tests = sum(1 for test in test_suite_results["individual_tests"] 
                              if test["result"]["test_results"]["analysis"]["performance_metrics"]["success_rate"] >= 80)

        test_suite_results["suite_summary"] = {
            "successful_tests": successful_tests,
            "total_tests": len(common_endpoints),
            "overall_success_rate": (successful_tests / len(common_endpoints)) * 100,
            "suite_health": "🟢 SAUDÁVEL" if successful_tests == len(common_endpoints) else "🟡 PARCIAL"
        }

        return test_suite_results

    def generate_educational_report(self, test_results):
        """
        Gera relatório educacional dos testes
        """
        report = {
            "educational_report": {
                "author": self.author,
                "github": self.github,
                "version": self.version,
                "report_timestamp": datetime.now().isoformat()
            },
            "learning_objectives": [
                "🎯 Compreender consistência de APIs",
                "📊 Analisar métricas de performance",
                "🔍 Identificar padrões de comportamento",
                "🛡️ Avaliar robustez de sistemas"
            ],
            "test_summary": test_results,
            "educational_insights": [
                "💡 APIs consistentes são fundamentais para aplicações estáveis",
                "⚡ Tempo de resposta afeta experiência do usuário",
                "🔄 Rate limiting protege serviços contra sobrecarga",
                "📈 Monitoramento contínuo é essencial para qualidade"
            ],
            "next_steps": [
                "📚 Estudar documentação da API Discord",
                "🛠️ Implementar tratamento de erros adequado",
                "📊 Monitorar performance em produção",
                "🔄 Implementar retry logic inteligente"
            ]
        }

        return report

# Exemplo de uso educacional
if __name__ == "__main__":
    print("Discord API Security Tester - Ferramenta Educacional")
    print(f"Desenvolvido por Jensan - https://github.com/")
    print("AVISO: Para fins educacionais e testes éticos apenas!")

    try:
        token = input("\nDigite seu token Discord: ")
        if not token:
            print("Token não fornecido. Saindo...")
            exit()

        tester = DiscordAPISecurityTester(token)
        tester.display_banner()

        print("\n🔬 Opções de Teste Educacional:")
        print("1. Teste de endpoint específico")
        print("2. Suite de testes comuns")

        choice = input("\nEscolha uma opção (1-2): ")

        if choice == "1":
            endpoint = input("Digite o endpoint (ex: /users/@me): ")
            method = input("Método HTTP (GET/POST/PATCH): ").upper()

            print(f"\n🧪 Testando endpoint customizado...")
            result = tester.test_api_consistency(endpoint, method, None, 2)

            print("\n" + "="*70)
            print("📋 RELATÓRIO DE TESTE")
            print("="*70)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "2":
            print(f"\n🧪 Executando suite de testes educacionais...")
            results = tester.test_common_endpoints()

            # Gera relatório educacional
            educational_report = tester.generate_educational_report(results)

            print("\n" + "="*70)
            print("📚 RELATÓRIO EDUCACIONAL")
            print("="*70)
            print(json.dumps(educational_report, indent=2, ensure_ascii=False))

        else:
            print("Opção inválida!")

    except KeyboardInterrupt:
        print("\n\n👋 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")

    print(f"\n🎓 Obrigado por usar a ferramenta educacional do Jensan!")
    print("⭐ GitHub: https://github.com/")
