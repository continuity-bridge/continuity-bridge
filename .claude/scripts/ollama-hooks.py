#!/usr/bin/env python3
"""
Continuity Bridge - Ollama/Local LLM Integration Hooks
Detects and offers integration with local LLM instances

Version: 0.2.0
Date: 2026-03-01
"""

import os
import sys
import json
import socket
import subprocess
from typing import Dict, Optional, List


class OllamaHooks:
    """Integration hooks for Ollama/Local LLM."""
    
    def __init__(self, endpoint: str = "http://localhost:11434"):
        self.endpoint = endpoint
        self.host = "localhost"
        self.port = 11434
        
    def is_running(self) -> bool:
        """Check if Ollama service is running."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((self.host, self.port))
            return True
        except:
            return False
        finally:
            s.close()
    
    def get_models(self) -> List[str]:
        """
        Get list of available models.
        
        Requires ollama CLI to be installed.
        """
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return []
            
            # Parse output
            models = []
            lines = result.stdout.strip().split('\n')
            
            # Skip header line
            for line in lines[1:]:
                if line.strip():
                    # Extract model name (first column)
                    model_name = line.split()[0]
                    models.append(model_name)
            
            return models
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def suggest_usage(self, context: Dict) -> Dict:
        """
        Generate usage suggestions based on current context.
        
        Returns dict with:
        - available: bool
        - models: list of str
        - suggestions: list of str (use cases)
        - commands: dict of example commands
        """
        result = {
            "available": self.is_running(),
            "endpoint": self.endpoint,
            "models": [],
            "suggestions": [],
            "commands": {}
        }
        
        if not result["available"]:
            result["note"] = "Ollama not running. Start with: ollama serve"
            return result
        
        # Get available models
        result["models"] = self.get_models()
        
        if not result["models"]:
            result["note"] = "No models installed. Install with: ollama pull <model>"
            result["suggestions"] = [
                "ollama pull llama2",
                "ollama pull codellama",
                "ollama pull mistral"
            ]
            return result
        
        # Generate usage suggestions
        result["suggestions"] = [
            "Code review and suggestions",
            "Alternative perspectives on architecture decisions",
            "Documentation generation",
            "Test case generation",
            "Refactoring suggestions",
            "Quick prototyping and brainstorming"
        ]
        
        # Example commands
        result["commands"] = {
            "interactive": f"ollama run {result['models'][0]}",
            "single_query": f"ollama run {result['models'][0]} 'Your question here'",
            "api_call": f"curl {self.endpoint}/api/generate -d '{{\"model\": \"{result['models'][0]}\", \"prompt\": \"Your prompt\"}}'",
            "python_api": "See ollama Python library: pip install ollama"
        }
        
        return result
    
    def offer_integration(self, workflow: str) -> str:
        """
        Generate friendly offer message for integration.
        
        Based on detected workflow, suggest how local LLM could help.
        """
        info = self.suggest_usage({})
        
        if not info["available"]:
            return None
        
        message = [
            "╔════════════════════════════════════════════════════════╗",
            "║  Local LLM Detected (Ollama)                          ║",
            "╚════════════════════════════════════════════════════════╝",
            "",
            f"Endpoint: {info['endpoint']}",
            f"Models available: {', '.join(info['models']) if info['models'] else 'None'}",
            ""
        ]
        
        if info['models']:
            message.extend([
                "Potential uses:",
                ""
            ])
            for suggestion in info['suggestions']:
                message.append(f"  • {suggestion}")
            
            message.extend([
                "",
                "Quick start:",
                f"  {info['commands']['interactive']}",
                ""
            ])
        else:
            message.extend([
                "No models installed yet. Suggestions:",
                ""
            ])
            for cmd in info['suggestions']:
                message.append(f"  {cmd}")
            message.append("")
        
        return "\n".join(message)


def main():
    """Run Ollama hooks and display info."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ollama/Local LLM integration hooks"
    )
    parser.add_argument('--check', action='store_true',
                       help='Check if Ollama is running')
    parser.add_argument('--models', action='store_true',
                       help='List available models')
    parser.add_argument('--suggest', action='store_true',
                       help='Show usage suggestions')
    parser.add_argument('--json', action='store_true',
                       help='Output JSON format')
    
    args = parser.parse_args()
    
    hooks = OllamaHooks()
    
    if args.check:
        running = hooks.is_running()
        if args.json:
            print(json.dumps({"running": running}))
        else:
            status = "✓ Running" if running else "✗ Not running"
            print(f"Ollama: {status}")
        sys.exit(0 if running else 1)
    
    elif args.models:
        models = hooks.get_models()
        if args.json:
            print(json.dumps({"models": models}))
        else:
            if models:
                print("Available models:")
                for model in models:
                    print(f"  • {model}")
            else:
                print("No models available")
        sys.exit(0)
    
    elif args.suggest:
        info = hooks.suggest_usage({})
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            message = hooks.offer_integration("unknown")
            if message:
                print(message)
            else:
                print("Ollama not running")
        sys.exit(0)
    
    else:
        # Default: Show integration offer if available
        message = hooks.offer_integration("unknown")
        if message:
            print(message)
        else:
            print("Ollama not detected or not running")
            print("Start with: ollama serve")


if __name__ == '__main__':
    main()
