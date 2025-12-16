export interface Programme {
  name: string;
  checked: boolean;
  libelle?: string;  // au lieu de Programme_Libellé
  etat?: string;
  startDate?: string;
  responsable?: string;
}
