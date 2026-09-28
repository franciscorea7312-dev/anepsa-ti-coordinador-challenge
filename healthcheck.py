import sys
import time
import signal
import json
import logging
import urllib.request
import urllib.error
import subprocess
from datetime import datetime

# Configuración por defecto (Parametrizable)
DEFAULT_URL = "http://localhost:8080/health"
DEFAULT_TIMEOUT = 2.0         # Respuesta en menos de 2 segundos
CHECK_INTERVAL = 30           # Verificar cada 30 segundos
MAX_FAILURES = 3              # Reintentos antes de reiniciar
RESTART_COMMAND = "echo 'Simulando reinicio del servicio...' && sleep 1"
LOG_FILE = "healthcheck.log"

# Configuración de Logging con Timestamp
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Manejo limpio de señales de interrupción (Ctrl+C)
def signal_handler(sig, frame):
    logging.info("Interrupción recibida (Ctrl+C). Cerrando monitoreo de forma limpia...")
    print("\n[INFO] Monitoreo detenido limpiamente.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def check_endpoint(url, timeout):
    """Verifica si el endpoint HTTP responde 200 en menos del timeout establecido."""
    start_time = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'HealthCheck-Agent/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            elapsed = time.time() - start_time
            if response.status == 200 and elapsed <= timeout:
                return True, response.status, elapsed
            return False, response.status, elapsed
    except Exception as e:
        elapsed = time.time() - start_time
        return False, None, elapsed

def trigger_notification(url, failures, status_msg):
    """Genera y emite payload JSON simulando envío a Slack/PagerDuty."""
    payload = {
        "event": "CRITICAL_ALERT",
        "service_url": url,
        "consecutive_failures": failures,
        "status": status_msg,
        "timestamp": datetime.now().isoformat(),
        "action_required": "Intervención manual requerida: El servicio sigue sin responder tras el intento de reinicio."
    }
    json_output = json.dumps(payload, indent=2)
    logging.error(f"Notificación de alerta enviada: {json_output}")
    print("\n--- [NOTIFICACIÓN ALERTA JSON] ---")
    print(json_output)
    print("----------------------------------\n")

def run_healthcheck(url=DEFAULT_URL, timeout=DEFAULT_TIMEOUT, interval=CHECK_INTERVAL, max_failures=MAX_FAILURES):
    """Bucle principal de monitoreo y lógica de auto-recuperación."""
    consecutive_failures = 0
    logging.info(f"Iniciando servicio de monitoreo para {url} (Intervalo: {interval}s, Timeout: {timeout}s)")
    
    while True:
        is_healthy, status_code, elapsed = check_endpoint(url, timeout)
        
        if is_healthy:
            logging.info(f"HEALTHY - Endpoint: {url} | HTTP {status_code} | Tiempo: {elapsed:.2f}s")
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            logging.warning(f"UNHEALTHY ({consecutive_failures}/{max_failures}) - Endpoint: {url} | HTTP: {status_code} | Tiempo: {elapsed:.2f}s")
            
            if consecutive_failures == max_failures:
                logging.error(f"Alcanzado el límite de {max_failures} fallos consecutivos. Ejecutando intento de reinicio...")
                
                # Intento de reinicio del servicio
                try:
                    subprocess.run(RESTART_COMMAND, shell=True, check=True)
                    logging.info("Comando de reinicio ejecutado con éxito.")
                except subprocess.CalledProcessError as e:
                    logging.error(f"Fallo al ejecutar el comando de reinicio: {e}")
                
                # Verificación post-reinicio
                time.sleep(2)
                post_healthy, post_code, post_elapsed = check_endpoint(url, timeout)
                if not post_healthy:
                    trigger_notification(url, consecutive_failures, "FAILED_AFTER_RESTART")
                else:
                    logging.info("El servicio se recuperó exitosamente tras el reinicio.")
                    consecutive_failures = 0
                    
        time.sleep(interval)

# BLOQUE DE PRUEBA Y SIMULACIÓN DE ESCENARIOS
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("=== MODO DE PRUEBA Y SIMULACIÓN ===")
        # Escenario 1: Servicio Sano (Simulado)
        print("[Escenario 1] Evaluando respuesta de servicio sano...")
        sano, code, t = check_endpoint("https://httpbin.org/status/200", 2.0)
        print(f"Resultado Escenario 1 -> Estado Sano: {sano} (HTTP {code}, {t:.2f}s)")
        
        # Escenario 2: Servicio Caído (Simulado)
        print("\n[Escenario 2] Evaluando servicio caído (Simulación de 3 fallos y notificación)...")
        trigger_notification("http://localhost:9999/down", 3, "FAILED_AFTER_RESTART")
        print("=== FIN DE PRUEBAS ===")
        sys.exit(0)
        
    run_healthcheck()
EOF