import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormControl,
  Validators
} from '@angular/forms';
import { QUADRIGE_EXTRACTABLE_FIELDS } from '../../constants/quadrige_constants';



@Component({
  selector: 'app-frontend-filter',
  templateUrl: './frontend-filter.component.html',
  styleUrls: ['./frontend-filter.component.scss']
})
export class FrontendFilterComponent implements OnInit {
  @Output() apply = new EventEmitter<any>();
  @Output() close = new EventEmitter<void>();

  availableFields: string[] = [];

  filterForm!: FormGroup<{
    name: FormControl<string>;
    fields: FormControl<string[]>;
    startDate: FormControl<Date | null>;
    endDate: FormControl<Date | null>;
  }>;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.availableFields = QUADRIGE_EXTRACTABLE_FIELDS;

    this.filterForm = this.fb.nonNullable.group({
      name: this.fb.nonNullable.control('', [
        Validators.required,
        Validators.minLength(3),
      ]),
      fields: this.fb.nonNullable.control<string[]>([], Validators.required),
      startDate: this.fb.control<Date | null>(null),
      endDate: this.fb.control<Date | null>(null),
    });
  }

  isFormValid(): boolean {
    const { name, fields, startDate, endDate } = this.filterForm.value;

    const nameValid = !!name && name.trim().length >= 3;
    const fieldsValid = Array.isArray(fields) && fields.length > 0;

    let periodValid = true;
    if (startDate || endDate) {
      periodValid = !!(startDate && endDate && startDate <= endDate);
    }

    return nameValid && fieldsValid && periodValid;
  }

  get fieldsInvalid(): boolean {
    return !this.filterForm.value.fields?.length;
  }

  get dateRangeInvalid(): boolean {
    const { startDate, endDate } = this.filterForm.value;
    if (!startDate && !endDate) return false;
    if (!startDate || !endDate) return true;
    return startDate > endDate;
  }

  applyFilter(): void {
    if (!this.isFormValid()) return;

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
