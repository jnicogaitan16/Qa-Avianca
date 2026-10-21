#!/usr/bin/env python3
"""
extract_and_score.py — Puntuación de confiabilidad de fuentes

Recibe una lista de URLs/fuentes citadas y devuelve un score de confianza
según los criterios de references/criterios-fuentes-confiables.md.

Uso:
    python extract_and_score.py --sources '["https://learn.microsoft.com/...", "https://stackoverflow.com/..."]'
    python extract_and_score.py --file fuentes.json

Salida: JSON con cada fuente y su score.
"""

import argparse
import json
import re
import sys
from urllib.parse import urlparse


# Dominios oficiales de proveedores (score 5)
OFFICIAL_DOMAINS = {
    "learn.microsoft.com",
    "docs.microsoft.com",
    "selenium.dev",
    "nightwatchjs.org",
    "learning.postman.com",
    "docs.python.org",
    "developer.mozilla.org",
    "nodejs.org",
    "docs.npmjs.com",
    "devdocs.io",
    "cucumber.io",
    "docs.github.com",
    "cloud.google.com",
    "docs.aws.amazon.com",
    "reactjs.org",
    "vuejs.org",
    "angular.io",
    "typescriptlang.org",
    "go.dev",
    "rust-lang.org",
    "kubernetes.io",
    "docker.com",
}

# Dominios de estándares (score 4)
STANDARDS_DOMAINS = {
    "istqb.org",
    "astqb.org",
    "ietf.org",
    "w3.org",
    "ieee.org",
    "owasp.org",
    "iso.org",
    "ecma-international.org",
}

# Dominios de terceros reconocidos (score 3)
RECOGNIZED_THIRD_PARTY = {
    "martinfowler.com",
    "digitalocean.com",
    "thoughtworks.com",
    "baeldung.com",
    "realpython.com",
    "css-tricks.com",
    "smashingmagazine.com",
    "web.dev",
    "freecodecamp.org",
    "tutorialspoint.com",
}

# Dominios de comunidad curada (score 2)
CURATED_COMMUNITY = {
    "stackoverflow.com",
    "stackexchange.com",
    "github.com",
    "dev.to",
    "reddit.com",
    "hashnode.dev",
    "discourse.org",
}

# Dominios de contenido sin curación (score 1)
UNCURATED = {
    "medium.com",
    "blogger.com",
    "wordpress.com",
    "blogspot.com",
    "youtube.com",
    "quora.com",
}


def extract_domain(url: str) -> str:
    """Extrae el dominio base de una URL."""
    try:
        parsed = urlparse(url if "://" in url else f"https://{url}")
        domain = parsed.netloc.lower()
        # Quitar www.
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return ""


def match_domain(domain: str, domain_set: set) -> bool:
    """Verifica si el dominio coincide con alguno del set (incluyendo subdominios)."""
    for known in domain_set:
        if domain == known or domain.endswith(f".{known}"):
            return True
    return False


def score_source(source: str) -> dict:
    """Asigna un score de confiabilidad a una fuente."""
    # Si no es URL, score 0
    if not re.match(r"https?://|www\.", source, re.IGNORECASE):
        return {
            "source": source,
            "domain": None,
            "score": 0,
            "level": "sin_fuente",
            "reason": "No es una URL verificable",
        }

    domain = extract_domain(source)

    if not domain:
        return {
            "source": source,
            "domain": None,
            "score": 0,
            "level": "sin_fuente",
            "reason": "No se pudo extraer el dominio",
        }

    if match_domain(domain, OFFICIAL_DOMAINS):
        return {
            "source": source,
            "domain": domain,
            "score": 5,
            "level": "oficial",
            "reason": "Documentación oficial del proveedor",
        }

    if match_domain(domain, STANDARDS_DOMAINS):
        return {
            "source": source,
            "domain": domain,
            "score": 4,
            "level": "estandar",
            "reason": "Estándar reconocido de la industria",
        }

    if match_domain(domain, RECOGNIZED_THIRD_PARTY):
        return {
            "source": source,
            "domain": domain,
            "score": 3,
            "level": "tercero_reconocido",
            "reason": "Documentación de tercero reconocido",
        }

    if match_domain(domain, CURATED_COMMUNITY):
        return {
            "source": source,
            "domain": domain,
            "score": 2,
            "level": "comunidad_curada",
            "reason": "Comunidad con mecanismos de curación",
        }

    if match_domain(domain, UNCURATED):
        return {
            "source": source,
            "domain": domain,
            "score": 1,
            "level": "sin_curacion",
            "reason": "Contenido sin curación/revisión de pares",
        }

    # Dominio desconocido — score 1 por defecto
    return {
        "source": source,
        "domain": domain,
        "score": 1,
        "level": "desconocido",
        "reason": f"Dominio '{domain}' no está en ninguna lista conocida",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Puntúa la confiabilidad de fuentes citadas"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--sources",
        type=str,
        help='Lista JSON de URLs/fuentes (ej: \'["https://...", "https://..."]\')',
    )
    group.add_argument(
        "--file",
        type=str,
        help="Archivo JSON con lista de fuentes",
    )

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            sources = json.load(f)
    else:
        sources = json.loads(args.sources)

    if not isinstance(sources, list):
        print("Error: la entrada debe ser una lista JSON de strings", file=sys.stderr)
        sys.exit(1)

    results = [score_source(s) for s in sources]

    # Resumen
    min_score = min(r["score"] for r in results) if results else 0
    avg_score = sum(r["score"] for r in results) / len(results) if results else 0
    below_threshold = [r for r in results if r["score"] < 3]

    output = {
        "fuentes_evaluadas": len(results),
        "score_minimo": min_score,
        "score_promedio": round(avg_score, 2),
        "fuentes_bajo_umbral": len(below_threshold),
        "umbral_minimo_aceptable": 3,
        "detalle": results,
    }

    if below_threshold:
        output["advertencia"] = (
            f"{len(below_threshold)} fuente(s) con score < 3. "
            "Estas afirmaciones deben marcarse con advertencia en la respuesta final."
        )

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
