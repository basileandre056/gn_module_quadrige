export interface ExtractedLink {
  file_name: string;
  url: string;
  status?: 'SUCCESS' | 'WARNING';
  warning?: string | null;
}
