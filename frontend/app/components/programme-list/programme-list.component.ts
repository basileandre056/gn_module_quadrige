import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';


// 🔹 Types
import { Programme } from '../models/programmes';
import { ExtractedLink } from '../models/extractedLinks';
import { ExtractionResponse } from '../models/extraction-response';
import { ProgramExtractionResponse } from '../models/program-extraction-response';
import { QuadrigeConfigService, QuadrigeConfig } from '../../services/quadrige-config.service';


// 🔹 Interface manquante — nécessaire pour éviter les erreurs TS
interface LastProgrammesResponse {
  status: string;
  programmes?: Programme[];
  monitoringLocation?: string;
  fichiers_csv?: any[];
  message?: string;
}

@Component({
  selector: 'app-programme-list',
  templateUrl: './programme-list.component.html',
  styleUrls: ['./programme-list.component.scss']
})
export class ProgrammeListComponent implements OnInit {

config!: QuadrigeConfig;
locations: {code: string; label: string}[] = [];


  programmes: Programme[] = [];

  extractedDataFiles: ExtractedLink[] = [];
  extractedProgramFiles: ExtractedLink[] = [];
  displayedColumns: string[] = ['select', 'name', 'libelle', 'startDate', 'etat', 'responsable'];

  message: string = '';
  isLoading: boolean = false;
  allSelected = false;
  searchText: string = '';
  showDataFilter = false;
  showProgramFilter = false;

  dataFilter: any = null;
  programFilter: any = null;

  monitoringLocation: string = '';
  monitoringLabel: string = '';



  private API = '/geonature/api/quadrige';


  private locationLabels = [
    { code: '126-', label: 'Réunion' },
    { code: '145-', label: 'Mayotte' },
    { code: '048-', label: 'Maurice' },
    { code: '153-', label: 'Île Tromelin' },
    { code: '152-', label: 'Îles Glorieuses' },
    { code: '154-', label: 'Île Juan de Nova' },
    { code: '155-', label: 'Île Bassas da India' },
    { code: '156-', label: 'Île Europa' },
  ];

  constructor(private http: HttpClient, private configService: QuadrigeConfigService) {}

  configReady = false;

  async ngOnInit(): Promise<void> {
    await this.configService.loadConfig();

    this.config = this.configService.config;
    this.locations = this.config.locations;

    this.configReady =
      this.locations.length > 0 ||
      this.config.extractable_fields.length > 0;

    console.log('[QUADRIGE] Config ready:', this.configReady, this.config);

    this.initialiserProgrammes();
  }




  private initialiserProgrammes(): void {
    this.http.get<LastProgrammesResponse>(`${this.API}/last-programmes`).subscribe({
      next: (res: LastProgrammesResponse) => {
        if (res?.status === 'ok' && Array.isArray(res?.programmes) && res.programmes.length > 0) {

          this.programmes = res.programmes.map((p: Programme) => ({
            ...p,
            checked: false
          }));

          this.monitoringLocation = res?.monitoringLocation || '';
          this.updateMonitoringLabel();
          this.extractedProgramFiles = this.mapToExtractedLinks(res?.fichiers_csv || []);
          this.message = `✅ ${this.programmes.length} programmes chargés (${this.monitoringLocation})`;

        } else {
          this.extractedProgramFiles = this.mapToExtractedLinks(res?.fichiers_csv || []);
          this.message = 'Aucun programme sauvegardé.';
        }
      },
      error: (err: HttpErrorResponse) => {
        console.error('[FRONTEND] ❌ Erreur backend :', err);
        this.message = 'Erreur lors du chargement des derniers programmes.';
      }
    });
  }

  private updateMonitoringLabel(): void {
    const found = this.locations.find(l => this.monitoringLocation.startsWith(l.code));
    this.monitoringLabel = found ? found.label : '';
  }


  private mapToExtractedLinks(raw: any): ExtractedLink[] {
    if (!Array.isArray(raw)) return [];
    return raw
      .map((item: any) => ({
        file_name: item?.file_name ?? item?.programme ?? item?.name ?? 'fichier',
        url: item?.url ?? ''
      }))
      .filter((f: ExtractedLink) => !!f.url);
  }

  get filteredProgrammes(): Programme[] {
    if (!this.searchText) return this.programmes;
    return this.programmes.filter(p =>
      p.name.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }

  isSearchActive(): boolean {
    return this.searchText.trim().length > 0;
  }

  toggleAll(): void {
    this.programmes.forEach(p => (p.checked = this.allSelected));
  }

  openDataFilter(): void {
    this.showProgramFilter = false;
    this.showDataFilter = true;
  }

  openProgramFilter(): void {
    this.showDataFilter = false;
    this.showProgramFilter = true;
  }

  onDataFilterApplied(filterData: any): void {
    this.message = 'Filtre de données appliqué.';
    this.showDataFilter = false;

    const { monitoringLocation, ...filterWithoutLocation } = filterData;
    this.dataFilter = filterWithoutLocation;
  }

  onProgramFilterApplied(filterData: any): void {
    this.message = 'Filtre de programmes appliqué.';
    this.showProgramFilter = false;
    this.programFilter = filterData;
  }

  extractPrograms(): void {
    if (!this.programFilter) {
      this.message = 'Veuillez définir un filtre d’extraction de programmes.';
      return;
    }

    this.isLoading = true;
    this.message = 'Extraction et filtrage des programmes en cours...';

    this.http.post<ProgramExtractionResponse>(
      `${this.API}/program-extraction`,
      { filter: this.programFilter }
    ).subscribe({
      next: (res: ProgramExtractionResponse) => {
        this.monitoringLocation = this.programFilter?.monitoringLocation || '';
        this.updateMonitoringLabel();

        if (res?.status === 'ok') {
          this.extractedProgramFiles = this.mapToExtractedLinks(res.fichiers_csv);

          if (Array.isArray(res.programmes)) {
            this.programmes = res.programmes.map((p: Programme) => ({
              ...p,
              checked: false
            }));
          }

          this.message = `✅ Extraction terminée (${this.programmes.length} programmes)`;

        } else {
          this.message = res?.message ?? 'Réponse inattendue du serveur';
        }

        this.isLoading = false;
      },
      error: (err: HttpErrorResponse) => {
        this.message = err?.error?.message ?? 'Erreur serveur inattendue';
        this.isLoading = false;
      }
    });
  }

  relancerFiltrageSeul(): void {
    this.isLoading = true;

    this.http.post<any>(
      `${this.API}/filtrage_seul`,
      { filter: this.programFilter || {} }
    ).subscribe({
      next: (res: any) => {
        this.extractedProgramFiles = this.mapToExtractedLinks(res.fichiers_csv || []);

        if (Array.isArray(res.programmes)) {
          this.programmes = res.programmes.map((p: Programme) => ({
            ...p,
            checked: false
          }));

          this.message = `✅ Filtrage relancé (${this.programmes.length} programmes)`;
        } else {
          this.message = res?.message ?? 'Aucun programme trouvé';
        }

        this.isLoading = false;
      },
      error: (err: HttpErrorResponse) => {
        this.message = 'Erreur lors du filtrage seul.';
        this.isLoading = false;
      }
    });
  }

  extractData(): void {
    const selectedPrograms = this.programmes
      .filter(p => p.checked)
      .map(p => p.name);

    if (!this.dataFilter) {
      this.message = 'Veuillez définir un filtre avant de lancer une extraction.';
      return;
    }

    if (selectedPrograms.length === 0) {
      this.message = 'Veuillez sélectionner au moins un programme.';
      return;
    }

    this.isLoading = true;
    this.message = 'Extraction des données en cours...';

    this.http.post<ExtractionResponse>(
      `${this.API}/data-extractions`,
      { programmes: selectedPrograms, filter: this.dataFilter }
    ).subscribe({
      next: (res: ExtractionResponse) => {
        if (res?.status === 'ok') {
          this.extractedDataFiles = this.mapToExtractedLinks(res?.fichiers_zip);
          this.message = `Fichiers extraits (${this.extractedDataFiles.length})`;
        } else {
          this.message = res?.message ?? 'Réponse inattendue du serveur';
          this.extractedDataFiles = [];
        }

        this.isLoading = false;
      },
      error: (err: HttpErrorResponse) => {
        this.message = err?.error?.message ?? 'Erreur serveur inattendue';
        this.extractedDataFiles = [];
        this.isLoading = false;
      }
    });
  }
}
