import { Component } from '@angular/core';

@Component({
  selector: 'gn-quadrige-extraction',
  template: `
    <h2>QUADRIGE – Extraction</h2>
    <p>Démo d'intégration du MapList et d'un petit formulaire générique.</p>

    <!-- Exemple d'assets du module -->
    <img src="assets/gn_module_quadrige_extraction/logo.png" alt="logo" width="120" />

    <!-- Exemple d'utilisation MapList (liste externe non montrée ici) -->
    <pnx-map-list idName="id_releve" height="60vh"></pnx-map-list>
  `
})
export class QuadrigeExtractionComponent {}