
import os
import sys
import json
from datetime import datetime, timedelta

JSON_FILE = "sprint_data.json"

def generate_default_data():
    """Genera 15 tareas simuladas si el archivo JSON no existe."""
    today = datetime.now()
    tasks = [
        {"id": "TASK-101", "titulo": "Configurar Nginx Hardening", "responsable": "Carlos Perez", "estado": "Hecho", "story_points": 5, "fecha_limite": (today - timedelta(days=2)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 0},
        {"id": "TASK-102", "titulo": "Migración de Base de Datos", "responsable": "Maria Lopez", "estado": "En progreso", "story_points": 8, "fecha_limite": (today - timedelta(days=1)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 4},
        {"id": "TASK-103", "titulo": "Crear Pipeline CI/CD GitHub Actions", "responsable": "Carlos Perez", "estado": "Hecho", "story_points": 5, "fecha_limite": (today + timedelta(days=3)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 1},
        {"id": "TASK-104", "titulo": "Implementar Healthcheck script", "responsable": "Juan Gomez", "estado": "Hecho", "story_points": 3, "fecha_limite": (today + timedelta(days=1)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 0},
        {"id": "TASK-105", "titulo": "Limpieza de historial Git (.env)", "responsable": "Carlos Perez", "estado": "Por hacer", "story_points": 5, "fecha_limite": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 0},
        {"id": "TASK-106", "titulo": "Pruebas QA de Autenticación", "responsable": "Ana Martinez", "estado": "En progreso", "story_points": 3, "fecha_limite": (today - timedelta(days=3)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 5},
        {"id": "TASK-107", "titulo": "Optimizacion de consultas SQL", "responsable": "Maria Lopez", "estado": "En progreso", "story_points": 13, "fecha_limite": (today + timedelta(days=5)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 1},
        {"id": "TASK-108", "titulo": "Documentación de APIs N8N", "responsable": "Juan Gomez", "estado": "Por hacer", "story_points": 2, "fecha_limite": (today + timedelta(days=4)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 0},
        {"id": "TASK-109", "titulo": "Monitoreo de logs en producción", "responsable": "Ana Martinez", "estado": "Hecho", "story_points": 2, "fecha_limite": (today - timedelta(days=4)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 0},
        {"id": "TASK-110", "titulo": "Refactorización de Modulo de Pagos", "responsable": "Maria Lopez", "estado": "Bloqueado", "story_points": 8, "fecha_limite": (today - timedelta(days=2)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 6},
        {"id": "TASK-111", "titulo": "Soporte a usuarios finales", "responsable": "Juan Gomez", "estado": "Hecho", "story_points": 1, "fecha_limite": (today - timedelta(days=1)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 0},
        {"id": "TASK-112", "titulo": "Implementación de Webhooks", "responsable": "Carlos Perez", "estado": "En progreso", "story_points": 5, "fecha_limite": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 2},
        {"id": "TASK-113", "titulo": "Auditoría de Roles RBAC", "responsable": "Ana Martinez", "estado": "Por hacer", "story_points": 3, "fecha_limite": (today + timedelta(days=6)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 0},
        {"id": "TASK-114", "titulo": "Diseño de Dashboard en Jira", "responsable": "Juan Gomez", "estado": "Hecho", "story_points": 3, "fecha_limite": (today - timedelta(days=2)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 0},
        {"id": "TASK-115", "titulo": "Configuración de Alertamiento Slack", "responsable": "Carlos Perez", "estado": "Hecho", "story_points": 2, "fecha_limite": (today - timedelta(days=1)).strftime("%Y-%m-%d"), "dias_sin_movimiento": 0}
    ]
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)
    print(f"[INFO] Archivo '{JSON_FILE}' no existía. Se han generado 15 tareas por defecto.")

def load_data():
    """Carga y valida la estructura del archivo JSON."""
    if not os.path.exists(JSON_FILE):
        generate_default_data()
        
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            raise ValueError("El JSON debe contener una lista de tareas.")
            
        required_fields = {"id", "titulo", "responsable", "estado", "story_points", "fecha_limite"}
        for idx, task in enumerate(data):
            missing = required_fields - set(task.keys())
            if missing:
                raise KeyError(f"La tarea en el índice {idx} ({task.get('id', 'SIN_ID')}) no tiene los campos obligatorios: {missing}")
        return data
        
    except json.JSONDecodeError as e:
        print(f"[ERROR CRÍTICO] El archivo '{JSON_FILE}' tiene un formato JSON inválido: {e}")
        sys.exit(1)
    except (ValueError, KeyError) as e:
        print(f"[ERROR CRÍTICO] Estructura de datos incorrecta: {e}")
        sys.exit(1)

def generate_report(tasks):
    """Calcula métricas de Velocity, Tareas en Riesgo y Carga de Trabajo."""
    today = datetime.now()
    
    total_sp_comprometidos = sum(t["story_points"] for t in tasks)
    sp_completados = sum(t["story_points"] for t in tasks if t["estado"] == "Hecho")
    velocity_percentage = (sp_completados / total_sp_comprometidos * 100) if total_sp_comprometidos > 0 else 0
    
    # Detección de tareas en riesgo
    at_risk_tasks = []
    for t in tasks:
        due_date = datetime.strptime(t["fecha_limite"], "%Y-%m-%d")
        is_overdue = due_date < today and t["estado"] != "Hecho"
        is_stale = t.get("dias_sin_movimiento", 0) > 3 and t["estado"] != "Hecho"
        
        if is_overdue or is_stale:
            reason = []
            if is_overdue:
                reason.append(f"Vencida desde {t['fecha_limite']}")
            if is_stale:
                reason.append(f"Inactiva por {t.get('dias_sin_movimiento')} días")
            at_risk_tasks.append((t, ", ".join(reason)))

    # Carga por responsable
    workload = {}
    for t in tasks:
        resp = t["responsable"]
        if resp not in workload:
            workload[resp] = {"assigned_sp": 0, "completed_sp": 0, "tasks_count": 0}
        workload[resp]["assigned_sp"] += t["story_points"]
        workload[resp]["tasks_count"] += 1
        if t["estado"] == "Hecho":
            workload[resp]["completed_sp"] += t["story_points"]

    # Generación de reporte plano ejecutivo
    report = []
    report.append("==========================================================")
    report.append("        📊 REPORTE EJECUTIVO DE ESTADO DE SPRINT")
    report.append(f"        Fecha de emisión: {today.strftime('%Y-%m-%d %H:%M')}")
    report.append("==========================================================\n")
    
    report.append("1. METRICAS DE VELOCITY")
    report.append(f"   • SP Comprometidos Total: {total_sp_comprometidos} pts")
    report.append(f"   • SP Completados:         {sp_completados} pts")
    report.append(f"   • Cumplimiento de Velocity: {velocity_percentage:.1f}%\n")
    
    report.append("2. TAREAS EN RIESGO / BLOQUEADAS")
    if at_risk_tasks:
        for t, reason in at_risk_tasks:
            report.append(f"   🔴 [{t['id']}] {t['titulo']}")
            report.append(f"      Responsable: {t['responsable']} | Estado: {t['estado']} | SP: {t['story_points']}")
            report.append(f"      Motivo de riesgo: {reason}\n")
    else:
        report.append("   ✅ No se detectaron tareas en riesgo crítico.\n")
        
    report.append("3. CARGA DE TRABAJO Y ESTADO POR RESPONSABLE")
    for resp, stats in workload.items():
        assigned = stats["assigned_sp"]
        completed = stats["completed_sp"]
        
        # Lógica de Diagnóstico
        if assigned >= 20:
            status = "⚠️ SOBRECARGADO(A)"
        elif assigned <= 5:
            status = "🟢 SUBUTILIZADO(A)"
        else:
            status = "✅ CARGA OPTIMA"
            
        report.append(f"   • {resp}: {assigned} SP Asignados | {completed} SP Completados | {stats['tasks_count']} Tareas -> {status}")

    report.append("\n==========================================================")
    report.append("  Reporte listo para envío a Dirección / Comunicación Interna")
    report.append("==========================================================")
    
    return "\n".join(report)

if __name__ == "__main__":
    tasks_data = load_data()
    print(generate_report(tasks_data))