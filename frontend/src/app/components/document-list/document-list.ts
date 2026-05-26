import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { DocumentService } from '../../services/document.service';
import { Document } from '../../models/document.model';

@Component({
  selector: 'app-document-list',
  standalone: true,
  imports: [RouterLink, MatTableModule, MatButtonModule,
    MatIconModule, MatChipsModule, MatSnackBarModule],
  templateUrl: './document-list.html',
  styleUrl: './document-list.scss'
})
export class DocumentList implements OnInit {
  private documentService = inject(DocumentService);
  private snackBar = inject(MatSnackBar);

  documents = signal<Document[]>([]);
  displayedColumns = ['id', 'titre', 'ministere', 'classification', 'actions'];

  ngOnInit() {
    this.loadDocuments();
  }

  loadDocuments() {
    this.documentService.getAll().subscribe(docs => {
      this.documents.set(docs);
    });
  }

  delete(id: number) {
    if (confirm('Supprimer ce document ?')) {
      this.documentService.delete(id).subscribe(() => {
        this.snackBar.open('Document supprimé', 'OK', { duration: 3000 });
        this.loadDocuments();
      });
    }
  }
}
