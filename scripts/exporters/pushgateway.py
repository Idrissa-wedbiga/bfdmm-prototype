"""
pushgateway.py

Responsabilité unique : pousser les métriques DORA (déjà calculées)
vers Prometheus Pushgateway. Ce module ne calcule rien lui-même —
il reçoit des dictionnaires déjà produits par DoraMetrics et les
convertit en Gauges Prometheus.
"""

import time
import logging

from config import PUSHGATEWAY
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

log = logging.getLogger("pushgateway")

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

JOB_NAME = "bfdmm_dora_metrics"

# Label fixe : garantit que chaque push REMPLACE le précédent dans
# Pushgateway au lieu de créer une nouvelle série à côté.
GROUPING_KEY = {"project": "bfdmm", "instance": "prototype"}


def push_dora_metrics(df: dict, cfr: dict, lt: dict, mttr: dict) -> bool:
    """
    Pousse les 4 métriques DORA vers Pushgateway.

    Args:
        df:   résultat de DoraMetrics.deployment_frequency()
        cfr:  résultat de DoraMetrics.change_failure_rate()
        lt:   résultat de DoraMetrics.lead_time_for_changes()
        mttr: résultat de DoraMetrics.mttr()

    Returns:
        True si le push a réussi, False sinon.
    """
    registry = CollectorRegistry()

    Gauge(
        "bfdmm_deployments_per_day",
        "Nombre moyen de déploiements réussis par jour",
        registry=registry,
    ).set(df["deployments_per_day"])

    Gauge(
        "bfdmm_successful_deployments_total",
        "Déploiements réussis sur la période",
        registry=registry,
    ).set(df["successful_deployments"])

    Gauge(
        "bfdmm_failed_deployments_total",
        "Déploiements échoués sur la période",
        registry=registry,
    ).set(df["failed_deployments"])

    Gauge(
        "bfdmm_change_failure_rate_percent",
        "Change Failure Rate (%)",
        registry=registry,
    ).set(cfr["change_failure_rate_percent"])

    Gauge(
        "bfdmm_lead_time_minutes",
        "Lead Time for Changes (minutes)",
        registry=registry,
    ).set(lt["average_lead_time_minutes"])

    Gauge(
        "bfdmm_mttr_minutes",
        "MTTR (minutes)",
        registry=registry,
    ).set(mttr["mttr_minutes"])

    Gauge(
        "bfdmm_mttr_recoveries_total",
        "Nombre de récupérations observées",
        registry=registry,
    ).set(mttr["recoveries"])

    Gauge(
        "bfdmm_exporter_last_push_timestamp_seconds",
        "Timestamp Unix du dernier push réussi",
        registry=registry,
    ).set(time.time())

    Gauge(
        "bfdmm_dora_analysis_period_days",
        "Fenêtre temporelle utilisée pour le calcul DORA",
        registry=registry,
    ).set(df["period_days"])

    Gauge(
        "bfdmm_exporter_last_scrape_success",
        "1 si le dernier calcul + push des métriques a réussi, 0 sinon",
        registry=registry,
    ).set(1)

    try:
        push_to_gateway(
            PUSHGATEWAY,
            job=JOB_NAME,
            registry=registry,
            grouping_key=GROUPING_KEY,
        )
        log.info("Push réussi vers Pushgateway (%s)", PUSHGATEWAY)
        return True

    except Exception:
        log.exception("Échec du push vers Pushgateway")

        # Tentative de signaler l'échec à Grafana via une gauge dédiée,
        # poussée seule (registry séparé) pour ne pas dépendre du push
        # principal qui vient d'échouer.
        try:
            failure_registry = CollectorRegistry()
            Gauge(
                "bfdmm_exporter_last_scrape_success",
                "1 si le dernier calcul + push des métriques a réussi, 0 sinon",
                registry=failure_registry,
            ).set(0)
            push_to_gateway(
                PUSHGATEWAY,
                job=JOB_NAME,
                registry=failure_registry,
                grouping_key=GROUPING_KEY,
            )
        except Exception:
            log.exception("Impossible de signaler l'échec à Pushgateway")

        return False