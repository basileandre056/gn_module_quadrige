import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


export interface QuadrigeConfig {
  locations: { code: string; label: string }[];
  extractable_fields: string[];
}

@Injectable({
  providedIn: 'root'
})
export class QuadrigeConfigService {

  public config: QuadrigeConfig = {
    locations: [],
    extractable_fields: []
  };

  private API = '/geonature/api/quadrige';
;

  constructor(private http: HttpClient) {}

  /**
   * Charge la configuration depuis le backend.
   * Appelé une fois au démarrage du module.
   */
  async loadConfig(): Promise<void> {
    const url = `${this.API}/config`;

    try {
      const res = await this.http.get<any>(url).toPromise();
      this.config = res.config ?? { locations: [], extractable_fields: [] };
      console.log('[CONFIG] Config chargée :', this.config);
    } catch (error) {
      console.error('[CONFIG] Erreur de chargement config :', error);
    }
  }
}
