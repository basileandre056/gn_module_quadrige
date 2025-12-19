import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { QUADRIGE_LOCATIONS } from '../../constants/quadrige_constants';

@Component({
  selector: 'app-program-extraction-filter',
  templateUrl: './program-extraction-filter.component.html',
  styleUrls: ['./program-extraction-filter.component.scss']
})
export class ProgramExtractionFilterComponent implements OnInit {
  @Output() apply = new EventEmitter<any>();
  @Output() close = new EventEmitter<void>();

  filterForm!: FormGroup;
  sugested_locations: { code: string; label: string }[] = [];

  filteredLocations$!: Observable<any[]>;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    // Récupération des lieux depuis la config
    this.sugested_locations = QUADRIGE_LOCATIONS;


    // Initialisation du formulaire
    this.filterForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      monitoringLocation: new FormControl<string>('', Validators.required)
    });

    const monitoringCtrl = this.filterForm.get('monitoringLocation') as FormControl<string>;

    this.filteredLocations$ = monitoringCtrl.valueChanges.pipe(
      startWith(''),
      map((value: string) => this.filterLocations(value || ''))
    );
  }

  private filterLocations(value: string): any[] {
    const f = value.toLowerCase();
    return this.sugested_locations.filter(loc =>
      loc.label.toLowerCase().includes(f) || loc.code.toLowerCase().includes(f)
    );
  }

  isFormValid(): boolean {
    return this.filterForm.valid;
  }

  applyFilter(): void {
    if (!this.isFormValid()) return;
    this.apply.emit(this.filterForm.value);
  }
}
