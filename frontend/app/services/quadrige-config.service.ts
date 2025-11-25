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

  private API = '/api/quadrige';

  constructor(private http: HttpClient) {}

  /**
   * Charge la configuration depuis le backend.
   * Appelé une fois au démarrage du module.
   */
  async loadConfig(): Promise<void> {
    const url = `${this.API}/config`;

    try {
      const data = await this.http.get<QuadrigeConfig>(url).toPromise();

      this.config = data;
      console.log('[CONFIG] Config chargée :', this.config);
    } catch (error) {
      console.error('[CONFIG] Erreur de chargement config :', error);
    }
  }
}
