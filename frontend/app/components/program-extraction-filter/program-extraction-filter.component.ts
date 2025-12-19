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
    this.filterForm = this.fb.group({
      name: ['', Validators.required],
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
        label: 'Lieu d’observation',
        type_widget: 'select',
        values: this.configService.config.locations,
        option_label: 'label',
        option_value: 'code',
      },
    ];
  }

  applyFilter(): void {
    if (this.filterForm.invalid) return;
    this.apply.emit(this.filterForm.value);
  }
}
