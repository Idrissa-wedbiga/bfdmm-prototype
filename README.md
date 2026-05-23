# BFDMM Prototype — Burkina Faso DevSecOps Maturity Model

## Description
Prototype de validation du modèle BFDMM démontrant la transition
du niveau N1-Silos vers N3-Defined via un pipeline CI/CD sécurisé.

## Stack technique
- **Frontend** : Angular 17
- **Backend** : Spring Boot 3.2 + Java 21
- **Base de données** : PostgreSQL 16
- **Pipeline** : GitHub Actions
- **Infrastructure** : K3s (Kubernetes léger)
- **Sécurité** : SonarQube · Trivy · OWASP ZAP · Vault · Falco

## Pipeline de sécurité (7 stages)
| Stage | Outil | Rôle |
|-------|-------|------|
| S0 | Threat Dragon CLI | Threat Modeling STRIDE |
| S1 | SonarQube | SAST + Quality Gate |
| S2 | OWASP Dep-Check + Trivy | SCA |
| S3 | Trivy | Scan image Docker |
| S4 | Helm + Vault | Déploiement K3s |
| S5 | OWASP ZAP | DAST |
| S6 | Falco | Surveillance runtime |

## Lancer le projet
```bash
docker compose up -d
cd backend && mvn spring-boot:run
cd frontend && ng serve
```

## Score BFDMM
- **Avant** : 16,38% (N1-Silos)
- **Après** : 84,12% (N3-Defined)
