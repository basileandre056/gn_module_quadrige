import { NgModule, APP_INITIALIZER } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { MatTooltipModule } from '@angular/material/tooltip';
import { MatChipsModule } from '@angular/material/chips';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatRippleModule } from '@angular/material/core';

import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';


import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatCardModule } from '@angular/material/card';
import { MatSortModule } from '@angular/material/sort';

import { GN2CommonModule } from '@geonature_common/GN2Common.module';

import { QuadrigeConfigService } from './services/quadrige-config.service';

// 🔹 Composants Quadrige
import { ProgrammeListComponent } from './programme-list/programme-list.component';
import { FrontendFilterComponent } from './frontend-filter/frontend-filter.component';
import { ProgramExtractionFilterComponent } from './program-extraction-filter/program-extraction-filter.component';
import { ExtractedLinksComponent } from './extracted-links/extracted-links.component';


export function loadQuadrigeConfig(configService: QuadrigeConfigService) {
  return () => configService.loadConfig();
}

@NgModule({
  declarations: [
    ProgrammeListComponent,
    FrontendFilterComponent,
    ProgramExtractionFilterComponent,
    ExtractedLinksComponent,
  ],

  providers: [
    QuadrigeConfigService,
    {
      provide: APP_INITIALIZER,
      useFactory: loadQuadrigeConfig,
      deps: [QuadrigeConfigService],
      multi: true,
    },
  ],

  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,

    // Material
    MatSortModule,
    MatTooltipModule,
    MatRippleModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatCheckboxModule,
    MatCardModule,
    MatChipsModule,
    MatDatepickerModule,
    MatNativeDateModule,

    // GeoNature
    GN2CommonModule,
  ],

  

  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class GnModuleQuadrigeModule {}
