export interface ProgrammeRecu {
  code: string;
  lieu_mnemonique: string;
}

export interface ProgramResponse {
  status: "ok" | "warning";
  type?: "validation" | "not_found";
  message?: string;
  programmes_recus?: ProgrammeRecu[];
}
