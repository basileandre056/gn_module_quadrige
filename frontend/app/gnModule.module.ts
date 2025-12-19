import { NgModule, APP_INITIALIZER, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { MatTooltipModule } from '@angular/material/tooltip';


// ✅ À UTILISER
import { MatLegacyDatepickerModule } from '@angular/material/legacy-datepicker';
import { MatLegacyNativeDateModule } from '@angular/material/legacy-core';
import { MatLegacyFormFieldModule } from '@angular/material/legacy-form-field';
import { MatLegacyInputModule } from '@angular/material/legacy-input';
import { MatLegacyChipsModule } from '@angular/material/legacy-chips';
import { MatLegacyAutocompleteModule } from '@angular/material/legacy-autocomplete';


import { MatRippleModule } from '@angular/material/core';

import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatCardModule } from '@angular/material/card';
import { MatSortModule } from '@angular/material/sort';

import { GN2CommonModule } from '@geonature_common/GN2Common.module';


// Components
import { ProgrammeListComponent } from './components/programme-list/programme-list.component';
import { FrontendFilterComponent } from './components/frontend-filter/frontend-filter.component';
import { ProgramExtractionFilterComponent } from './components/program-extraction-filter/program-extraction-filter.component';
import { ExtractedLinksComponent } from './components/extracted-links/extracted-links.component';

// ROUTES — exactement comme MONITORINGS
const routes: Routes = [
  { path: '', component: ProgrammeListComponent },
  { path: '**', redirectTo: '' }
];


@NgModule({
  declarations: [
    ProgrammeListComponent,
    FrontendFilterComponent,
    ProgramExtractionFilterComponent,
    ExtractedLinksComponent,
  ],

  imports: [
  GN2CommonModule,
  RouterModule.forChild(routes),

  CommonModule,
  FormsModule,
  ReactiveFormsModule,
  HttpClientModule,

  MatSortModule,
  MatTooltipModule,
  MatRippleModule,
  MatTableModule,
  MatButtonModule,
  MatIconModule,
  MatProgressSpinnerModule,
  MatCheckboxModule,
  MatCardModule,

  // ✅ MATERIAL LEGACY UNIQUEMENT
  MatLegacyFormFieldModule,
  MatLegacyInputModule,
  MatLegacyAutocompleteModule,
  MatLegacyChipsModule,
  MatLegacyDatepickerModule,
  MatLegacyNativeDateModule,
],

  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class GeonatureModule  {}
