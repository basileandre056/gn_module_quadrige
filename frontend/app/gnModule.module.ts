import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// Réutilisation des composants cœur GeoNature
import { GN2CommonModule } from '@geonature_common/GN2Common.module';

import { routes } from './routes';
import { QuadrigeExtractionComponent } from './components/QuadrigeExtractionComponent';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    GN2CommonModule,
    RouterModule.forChild(routes)
  ],
  declarations: [QuadrigeExtractionComponent]
})
export class GnModule {}