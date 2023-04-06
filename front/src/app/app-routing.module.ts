import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { InputDataFormComponent } from './layout/input-data-form/input-data-form.component';
import { AppCustomLayoutComponent } from './layout/app-custom-layout/app-custom-layout.component';

const routes: Routes = [
  {
    path: '',
    component: InputDataFormComponent,
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
