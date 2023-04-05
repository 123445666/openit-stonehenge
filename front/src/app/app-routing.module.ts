import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { InputDataFormComponent } from './layout/input-data-form/input-data-form.component';
import { TableDataFormComponent } from './layout/table-data-form/table-data-form.component';
import { AppCustomLayoutComponent } from './layout/app-custom-layout/app-custom-layout.component';

const routes: Routes = [
  {
    path: '',
    component: InputDataFormComponent,
  },
  {
    path: 'predire/:date',
    component: TableDataFormComponent
  },
  {
    path: 'get-data/:date',
    component: AppCustomLayoutComponent
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
