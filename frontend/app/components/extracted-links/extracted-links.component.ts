import { Component, Input } from '@angular/core';
import { ExtractedLink } from '../models/extractedLinks';

@Component({
  selector: 'app-extracted-links',
  templateUrl: './extracted-links.component.html',
  styleUrls: ['./extracted-links.component.scss']
})
export class ExtractedLinksComponent {
  @Input() files: ExtractedLink[] = [];
  @Input() title: string = 'Liens extraits';

  getFileIconClass(fileName: string): string {
    if (!fileName) return 'icon-generic';
    const lower = fileName.toLowerCase();
    if (lower.endsWith('.csv')) return 'icon-csv';
    if (lower.endsWith('.zip')) return 'icon-zip';
    if (lower.endsWith('.json')) return 'icon-json';
    return 'icon-link';
  }
}
