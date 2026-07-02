from datetime import datetime, timedelta, timezone


class DoraMetrics:
    """
    Calcul des quatre métriques DORA à partir des workflow runs GitHub Actions :
      - Deployment Frequency
      - Lead Time for Changes
      - Change Failure Rate
      - Mean Time To Recovery (MTTR)
    """

    def __init__(self, workflow_runs):
        self.workflow_runs = workflow_runs

    # ------------------------------------------------------------------
    # Utilitaires
    # ------------------------------------------------------------------

    @staticmethod
    def _parse(date_str):
        """Parse une date ISO GitHub (suffixe Z) en datetime aware UTC."""
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    def filter_last_days(self, days):
        """Retourne les workflows exécutés durant les 'days' derniers jours."""
        limit = datetime.now(timezone.utc) - timedelta(days=days)
        return [
            run for run in self.workflow_runs
            if self._parse(run["created_at"]) >= limit
        ]

    # ------------------------------------------------------------------
    # 1. Deployment Frequency
    # ------------------------------------------------------------------

    def deployment_frequency(self, days):
        """Nombre de déploiements réussis sur une période, et fréquence par jour."""
        runs = self.filter_last_days(days)

        successful = [
            r for r in runs
            if r["status"] == "completed" and r["conclusion"] == "success"
        ]
        failed = [
            r for r in runs
            if r["status"] == "completed" and r["conclusion"] == "failure"
        ]

        freq_per_day = round(len(successful) / days, 3) if days > 0 else 0

        return {
            "period_days": days,
            "total_runs": len(runs),
            "successful_deployments": len(successful),
            "failed_deployments": len(failed),
            "deployments_per_day": freq_per_day,
        }

    # ------------------------------------------------------------------
    # 2. Change Failure Rate
    # ------------------------------------------------------------------

    def change_failure_rate(self, days):
        """Pourcentage de déploiements terminés qui ont échoué."""
        runs = self.filter_last_days(days)

        total = [r for r in runs if r["status"] == "completed"]
        failed = [r for r in total if r["conclusion"] == "failure"]

        rate = round((len(failed) / len(total)) * 100, 2) if total else 0

        return {
            "period_days": days,
            "total_deployments": len(total),
            "failed_deployments": len(failed),
            "change_failure_rate_percent": rate,
        }

    # ------------------------------------------------------------------
    # 3. Lead Time for Changes
    # ------------------------------------------------------------------

    def lead_time_for_changes(self, days):
        """Durée moyenne (minutes) entre création et fin d'un run terminé."""
        runs = self.filter_last_days(days)

        durations = []
        for run in runs:
            if run["status"] != "completed":
                continue
            start = self._parse(run["created_at"])
            end = self._parse(run["updated_at"])
            durations.append((end - start).total_seconds() / 60)

        average = round(sum(durations) / len(durations), 2) if durations else 0

        return {
            "period_days": days,
            "runs": len(durations),
            "average_lead_time_minutes": average,
        }

    # ------------------------------------------------------------------
    # 4. MTTR — Mean Time To Recovery
    # ------------------------------------------------------------------

    def mttr(self, days):
        """
        Pour chaque run en échec, cherche le PROCHAIN run réussi
        (pas seulement le suivant immédiat) et mesure le temps de récupération.
        Un même run de succès ne "répare" qu'un seul échec (le plus récent
        en attente) afin d'éviter de compter plusieurs fois la même reprise.
        """
        runs = sorted(self.filter_last_days(days), key=lambda r: r["created_at"])
        completed = [r for r in runs if r["status"] == "completed"]

        recoveries = []
        pending_failure_time = None

        for run in completed:
            if run["conclusion"] == "failure":
                if pending_failure_time is None:
                    pending_failure_time = self._parse(run["updated_at"])
                # si un échec était déjà en attente, on garde le premier
                # (la panne n'est résolue qu'au prochain succès)

            elif run["conclusion"] == "success" and pending_failure_time is not None:
                t_success = self._parse(run["updated_at"])
                recoveries.append((t_success - pending_failure_time).total_seconds() / 60)
                pending_failure_time = None  # panne résolue, on repart à zéro

        average = round(sum(recoveries) / len(recoveries), 2) if recoveries else 0

        return {
            "period_days": days,
            "recoveries": len(recoveries),
            "mttr_minutes": average,
        }