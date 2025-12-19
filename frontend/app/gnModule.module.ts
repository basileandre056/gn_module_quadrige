import { NgModule, APP_INITIALIZER, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MatSelectModule } from '@angular/material/select';



// ✅ À UTILISER
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';



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
  MatRippleModule,
  MatTableModule,
  MatButtonModule,
  MatIconModule,
  MatProgressSpinnerModule,
  MatCheckboxModule,
  MatCardModule,

  MatSelectModule,
  MatFormFieldModule,
  MatInputModule,
  
  MatDatepickerModule,
  MatNativeDateModule,
  
],

  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class GeonatureModule  {}
