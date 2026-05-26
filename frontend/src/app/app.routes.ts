import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./components/dashboard/dashboard')
        .then(m => m.Dashboard)
  },
  {
    path: 'documents',
    loadComponent: () =>
      import('./components/document-list/document-list')
        .then(m => m.DocumentList)
  },
  {
    path: 'documents/new',
    loadComponent: () =>
      import('./components/document-form/document-form')
        .then(m => m.DocumentForm)
  },
  {
    path: 'documents/edit/:id',
    loadComponent: () =>
      import('./components/document-form/document-form')
        .then(m => m.DocumentForm)
  }
];
