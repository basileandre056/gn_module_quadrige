import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { QuadrigeConfigService } from '../../services/quadrige-config.service';

@Component({
  selector: 'app-program-extraction-filter',
  templateUrl: './program-extraction-filter.component.html',
})
export class ProgramExtractionFilterComponent implements OnInit {
  @Output() apply = new EventEmitter<any>();
  @Output() close = new EventEmitter<void>();

  filterForm!: FormGroup;
  formsDefinition: any[] = [];

  constructor(
    private fb: FormBuilder,
    private configService: QuadrigeConfigService
  ) {}

  ngOnInit(): void {
    const cfg = this.configService.config;
    
    if (!cfg || !cfg.locations?.length) {
      return;
    }
  
    this.filterForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      monitoringLocation: ['', Validators.required],
    });
  
    this.formsDefinition = [
      {
        attribut_name: 'name',
        label: 'Nom du filtre',
        type_widget: 'input',
        required: true,
      },
      {
        attribut_name: 'monitoringLocation',
        label: 'Lieu de surveillance',
        type_widget: 'select',
        values: cfg.locations,
        key_label: 'label',
        key_value: 'code',
        required: true,
      },
    ];
  }


  applyFilter(): void {
    if (this.filterForm.invalid) return;
    this.apply.emit(this.filterForm.value);
  }
}
