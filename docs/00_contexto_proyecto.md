---
title: "00 – Contexto del Proyecto"
document_type: "contexto"
repo: "etlproject_birds"
created: "2025-11-22"
last_updated: "2025-11-22"
status: "estable"
role: "base-de-conocimiento"
confidence: "WHITE"
notes: "Documento estable. Se actualiza solo cuando cambie la naturaleza del proyecto."
---

# 00 – Contexto del Proyecto

## Propósito
Este documento define el contexto base del proyecto y actúa como referencia estable para cualquier IA o colaborador humano que se una al flujo de trabajo. No describe detalles técnicos cambiantes, sino el marco constante del proyecto.

## Qué es este proyecto
Repositorio para procesamiento de datos y proyección productiva en aves. Su objetivo es transformar, consolidar y preparar datos y cálculos relacionados a predicciones y análisis productivos. Futuras etapas incluirán modularización, refactors, integración a pipelines productivos y agentes IA.

Este documento no describe la implementación vigente; solo establece el marco.

## Enfoque de trabajo
El proyecto se desarrolla de forma iterativa, con soporte de IA, manteniendo claridad entre:

- **Línea de código:** ramas, cambios, PRs.
- **Línea de conocimiento:** documentación en docs/, decisiones, arquitectura y devlogs.

Los cambios significativos siempre pasan por PRs pequeños y semánticos.

## Convenciones de ramas
- `main` → estado estable del proyecto.
- `feature/*` → cambios funcionales en código.
- `docs/*` → cambios documentales.
- `research/*` → exploración o experimentación, puede ser descartable.
- `codex/*` → ramas generadas por IAs para trabajo técnico, solo mergean si aportan.

## Documentos principales en docs/
- `01_estado_actual.md` → cómo está hoy el sistema (radiografía).
- `02_plan_arquitectura.md` → arquitectura objetivo (v1 aún no creada).
- `03_prs_planificados.md` → roadmap de cambios.
- `journal/` → registro diario de decisiones y acciones.
- `adr/` → decisiones arquitectónicas formales.

Este documento es el punto de partida conceptual; los demás evolucionan.

## Rol de la IA (Resumen)
La IA participa como apoyo modular por roles:
- Orquestador: coordina pasos, PRs, prompts a otros agentes.
- Ejecutor: propone cambios de código.
- Documentador: sintetiza cambios en docs.
- Analizador: inspecciona el estado del código.

Este archivo se entregará al Orquestador en cada nueva sesión para cargar contexto.

## Qué no contiene
- Detalles de implementación.
- Arquitectura actual o futura.
- Plan de PRs.

Toda esa información vive en documentos correspondientes versionados por PR.
