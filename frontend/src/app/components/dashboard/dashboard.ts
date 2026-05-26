import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { DocumentService } from '../../services/document.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [RouterLink, MatCardModule, MatButtonModule, MatIconModule, MatChipsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit {
  private documentService = inject(DocumentService);

  totalDocuments = signal(0);
  documentsPublics = signal(0);
  documentsConfidentiels = signal(0);

  ngOnInit() {
    this.documentService.getAll().subscribe(docs => {
      this.totalDocuments.set(docs.length);
      this.documentsPublics.set(
        docs.filter(d => d.classification === 'PUBLIC').length);
      this.documentsConfidentiels.set(
        docs.filter(d => d.classification === 'CONFIDENTIEL').length);
    });
  }
}
