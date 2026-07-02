// src/environments/environment.ts
// En développement local (ng serve), Angular appelle directement le backend.
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api',   // direct vers Spring Boot
};
