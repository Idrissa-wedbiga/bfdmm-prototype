import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Document } from '../models/document.model';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {

  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8080/api/v1/documents';

  getAll(): Observable<Document[]> {
    return this.http.get<Document[]>(this.apiUrl);
  }

  getById(id: number): Observable<Document> {
    return this.http.get<Document>(`${this.apiUrl}/${id}`);
  }

  getByMinistere(ministere: string): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.apiUrl}/ministere/${ministere}`);
  }

  create(document: Document): Observable<Document> {
    return this.http.post<Document>(this.apiUrl, document);
  }

  update(id: number, document: Document): Observable<Document> {
    return this.http.put<Document>(`${this.apiUrl}/${id}`, document);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
