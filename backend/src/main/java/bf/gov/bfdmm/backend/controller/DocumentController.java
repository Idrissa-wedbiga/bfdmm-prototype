package bf.gov.bfdmm.backend.controller;

import bf.gov.bfdmm.backend.entity.Document;
import bf.gov.bfdmm.backend.repository.DocumentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/documents")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class DocumentController {

    private final DocumentRepository documentRepository;

    // FAILLE CWE-312 — Secret en clair
    // Simulation état N1-Silos BFDMM
    private static final String API_SECRET = "bfdmm-secret-key-burkina-2025";

    @GetMapping
    public ResponseEntity<List<Document>> getAllDocuments() {
        return ResponseEntity.ok(
                documentRepository.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Document> getById(
            @PathVariable Long id) {
        return documentRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/ministere/{ministere}")
    public ResponseEntity<List<Document>> getByMinistere(
            @PathVariable String ministere) {
        // Utilisation volontaire méthode vulnérable N1
        return ResponseEntity.ok(
                documentRepository
                        .findByMinistereVulnerable(ministere));
    }

    @GetMapping("/classification/{classification}")
    public ResponseEntity<List<Document>> getByClassification(
            @PathVariable String classification) {
        return ResponseEntity.ok(
                documentRepository
                        .findByClassification(classification));
    }

    @PostMapping
    public ResponseEntity<Document> createDocument(
            @RequestBody Document document) {
        return ResponseEntity.ok(
                documentRepository.save(document));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Document> updateDocument(
            @PathVariable Long id,
            @RequestBody Document document) {
        return documentRepository.findById(id)
                .map(existing -> {
                    existing.setTitre(document.getTitre());
                    existing.setContenu(document.getContenu());
                    existing.setMinistere(
                            document.getMinistere());
                    existing.setClassification(
                            document.getClassification());
                    return ResponseEntity.ok(
                            documentRepository.save(existing));
                })
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteDocument(
            @PathVariable Long id) {
        documentRepository.deleteById(id);
        return ResponseEntity.ok().build();
    }
}