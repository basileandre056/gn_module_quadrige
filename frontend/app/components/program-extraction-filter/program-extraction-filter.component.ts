import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { QuadrigeConfigService } from '../../services/quadrige-config.service';

@Component({
  selector: 'app-program-extraction-filter',
  templateUrl: './program-extraction-filter.component.html',
  styleUrls: ['./program-extraction-filter.component.scss'],
})
export class ProgramExtractionFilterComponent implements OnInit {
  @Output() apply = new EventEmitter<any>();
  @Output() close = new EventEmitter<void>();

  filterForm!: FormGroup;

  // Liste fournie au composant GN
  locations: { code: string; label: string }[] = [];

  constructor(
    private fb: FormBuilder,
    private configService: QuadrigeConfigService
  ) {}

  ngOnInit(): void {
    // Chargement des lieux depuis la config GN
    this.locations = this.configService.config.locations ?? [];

    // Formulaire piloté (Reactive Forms)
    this.filterForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      monitoringLocation: [null, Validators.required],
    });
  }

  isFormValid(): boolean {
    return this.filterForm.valid;
  }

  applyFilter(): void {
    if (!this.isFormValid()) return;
    this.apply.emit(this.filterForm.value);
  }
}
