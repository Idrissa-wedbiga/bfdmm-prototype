from collectors.github_client import GitHubClient
from metrics.dora_metrics import DoraMetrics
from exporters.pushgateway import push_dora_metrics


def main():
    github = GitHubClient()

    data = github.get_workflow_runs()

    workflows = data["workflow_runs"]
    print(f"Nombre récupéré : {len(workflows)}")

    for run in workflows:
        print(
            run["id"],
            run["name"],
            run["conclusion"],
            run["created_at"]
        )

    metrics = DoraMetrics(workflows)

    df = metrics.deployment_frequency(90)
    lt = metrics.lead_time_for_changes(90)
    cfr = metrics.change_failure_rate(90)
    mttr = metrics.mttr(90)

    print("=" * 60)
    print("MÉTRIQUES DORA")
    print("=" * 60)

    print("="*60)
    print("DEPLOYMENT FREQUENCY")
    print(df)

    print("="*60)
    print("LEAD TIME")
    print(lt)

    print("="*60)
    print("CHANGE FAILURE RATE")
    print(cfr)

    print("="*60)
    print("MTTR")
    print(mttr)
    success = push_dora_metrics(df, cfr, lt, mttr)

    if success:
        print("Métriques poussées vers Pushgateway avec succès.")
    else:
        print("Échec du push vers Pushgateway (voir logs).")

if __name__ == "__main__":
    main()