FROM eclipse-temurin:21-jre-alpine AS runtime

WORKDIR /app

# Utilisateur non-root — Principe moindre privilège
RUN addgroup -S bfdmm && adduser -S bfdmm -G bfdmm

# Copier le JAR
COPY target/*.jar app.jar

# Permissions
RUN chown bfdmm:bfdmm app.jar

USER bfdmm

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget -qO- http://localhost:8080/actuator/health \
  || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
