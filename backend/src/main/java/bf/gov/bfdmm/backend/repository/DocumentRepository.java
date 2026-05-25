package bf.gov.bfdmm.backend.repository;

import bf.gov.bfdmm.backend.entity.Document;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface DocumentRepository
        extends JpaRepository<Document, Long> {

    // FAILLE CWE-89 — Injection SQL intentionnelle
    // Simulation état N1-Silos BFDMM
    @Query(value = "SELECT * FROM documents " +
            "WHERE ministere = :ministere",
            nativeQuery = true)
    List<Document> findByMinistereVulnerable(
            String ministere);

    // Version sécurisée N3-Defined
    List<Document> findByMinistere(String ministere);

    List<Document> findByClassification(
            String classification);
}