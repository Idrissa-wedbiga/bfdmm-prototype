// src/environments/environment.prod.ts
// En production (Docker), Nginx proxifie /api/* vers le backend.
// Angular appelle donc /api/* sans préciser l'hôte.
export const environment = {
  production: true,
  apiUrl: '/api',         // relatif : passe par le proxy Nginx
};
