export interface Document {
  id?: number;
  titre: string;
  contenu: string;
  ministere: string;
  classification: string;
  dateCreation?: string;
  dateModification?: string;
}

export const MINISTERES = [
  'Ministère de l\'Économie',
  'Ministère de la Santé',
  'Ministère de l\'Éducation',
  'Ministère de la Défense',
  'Ministère de la Justice'
];

export const CLASSIFICATIONS = ['PUBLIC', 'INTERNE', 'CONFIDENTIEL', 'SECRET'];
