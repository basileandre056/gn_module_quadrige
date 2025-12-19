import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { QuadrigeConfigService } from '../../services/quadrige-config.service';

@Component({
  selector: 'app-frontend-filter',
  templateUrl: './frontend-filter.component.html',
  styleUrls: ['./frontend-filter.component.scss']
})
export class FrontendFilterComponent implements OnInit {
  @Output() apply = new EventEmitter<any>();
  @Output() close = new EventEmitter<void>();

  availableFields: string[] = [];
  filterForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private configService: QuadrigeConfigService
  ) {}

  ngOnInit(): void {
    this.availableFields = this.configService.config.extractable_fields;

    this.filterForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      fields: [[], Validators.required],
      startDate: [null],
      endDate: [null],
    });
  }

  get dateRangeInvalid(): boolean {
    const { startDate, endDate } = this.filterForm.value;
    if (!startDate && !endDate) return false;
    if (!startDate || !endDate) return true;
    return startDate > endDate;
  }

  applyFilter(): void {
    if (this.filterForm.invalid || this.dateRangeInvalid) return;

    const formatDate = (d: Date | null) =>
      d
        ? `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(
            d.getDate()
          ).padStart(2, '0')}`
        : null;

    const { name, fields, startDate, endDate } = this.filterForm.value;

    this.apply.emit({
      name,
      fields,
      startDate: formatDate(startDate),
      endDate: formatDate(endDate),
    });
  }
}
