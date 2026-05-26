import { Component, inject, signal, OnInit } from '@angular/core';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { DocumentService } from '../../services/document.service';
import { Document, MINISTERES, CLASSIFICATIONS } from '../../models/document.model';

@Component({
  selector: 'app-document-form',
  standalone: true,
  imports: [FormsModule, RouterLink, MatFormFieldModule, MatInputModule,
    MatSelectModule, MatButtonModule, MatIconModule, MatSnackBarModule],
  templateUrl: './document-form.html',
  styleUrl: './document-form.scss'
})
export class DocumentForm implements OnInit {
  private documentService = inject(DocumentService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private snackBar = inject(MatSnackBar);

  ministeres = MINISTERES;
  classifications = CLASSIFICATIONS;
  isEdit = signal(false);
  editId = signal<number | null>(null);

  document: Document = {
    titre: '', contenu: '', ministere: '', classification: ''
  };

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit.set(true);
      this.editId.set(+id);
      this.documentService.getById(+id).subscribe(doc => {
        this.document = doc;
      });
    }
  }

  save() {
    if (this.isEdit()) {
      this.documentService.update(this.editId()!, this.document).subscribe(() => {
        this.snackBar.open('Document modifié', 'OK', { duration: 3000 });
        this.router.navigate(['/documents']);
      });
    } else {
      this.documentService.create(this.document).subscribe(() => {
        this.snackBar.open('Document créé', 'OK', { duration: 3000 });
        this.router.navigate(['/documents']);
      });
    }
  }
}
