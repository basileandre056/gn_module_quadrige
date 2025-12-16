export interface ExtractionResponse {
  status: "ok" | "warning";
  type?: "validation" | "not_found";  // ✅ pour différencier les cas
  message?: string;
  programmes_recus?: string[];
  fichiers_zip?: { programme: string; url: string }[];
}
