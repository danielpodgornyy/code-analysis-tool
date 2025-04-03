import { RenderMode, ServerRoute } from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  {
    path: 'file-details/:filename',
    renderMode: RenderMode.Server  // Disable prerendering for this route
  },
  {
    path: '**',
    renderMode: RenderMode.Prerender
  }
];
