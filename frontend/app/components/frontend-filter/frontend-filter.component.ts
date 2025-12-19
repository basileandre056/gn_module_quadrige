import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { QuadrigeConfigService } from '../../services/quadrige-config.service';

@Component({
  selector: 'app-frontend-filter',
  templateUrl: './frontend-filter.component.html',
})
export class FrontendFilterComponent implements OnInit {
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

    if (!cfg || !cfg.extractable_fields?.length) {
      return; // ⬅️ empêche le rendu prématuré
    } 

    this.filterForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      fields: [[], Validators.required],
      startDate: [null],
      endDate: [null],
    }); 

    this.formsDefinition = [
      {
        attribut_name: 'name',
        label: 'Nom du filtre',
        type_widget: 'input',
        required: true,
      },
      {
        attribut_name: 'fields',
        label: 'Champs à extraire',
        type_widget: 'select',
        multiple: true,
        values: cfg.extractable_fields,
        simple_values: true,
        required: true,
      },
      {
        attribut_name: 'startDate',
        label: 'Date de début',
        type_widget: 'date',
      },
      {
        attribut_name: 'endDate',
        label: 'Date de fin',
        type_widget: 'date',
      },
    ];
  }


  applyFilter(): void {
    if (this.filterForm.invalid) return;
    this.apply.emit(this.filterForm.value);
  }
}
