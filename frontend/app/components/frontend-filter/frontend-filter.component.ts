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
      type: 'input',
      required: true,
      validators: ['required', 'minLength:3'],
    },
    {
      attribut_name: 'fields',
      label: 'Champs à extraire',
      type: 'select',
      multiple: true,
      values: this.configService.config.extractable_fields,
      required: true,
    },
    {
      attribut_name: 'startDate',
      label: 'Date de début',
      type: 'date',
      readonly: true,
    },
    {
      attribut_name: 'endDate',
      label: 'Date de fin',
      type: 'date',
      readonly: true,
    },
  ];
  }

  applyFilter(): void {
    if (this.filterForm.invalid) return;
    this.apply.emit(this.filterForm.value);
  }
}
