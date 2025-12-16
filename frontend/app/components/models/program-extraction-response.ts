import { ExtractedLink } from './extractedLinks';
import { Programme } from './programmes'; // ✅ pour typer la liste renvoyée

export interface ProgramExtractionResponse {
  status: string; // "ok" ou "warning"
  filtre_recu?: any; // parfois non renvoyé
  fichiers_csv: ExtractedLink[]; // liste des CSV disponibles
  programmes?: Programme[];      // ✅ nouveaux programmes filtrés renvoyés par le backend
  message?: string;              // message optionnel du backend
}
