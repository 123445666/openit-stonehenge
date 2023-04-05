import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { InputDataFormComponent } from './layout/input-data-form/input-data-form.component';
import { TableDataFormComponent } from './layout/table-data-form/table-data-form.component';
import { Routes, RouterModule } from "@angular/router";

import { HttpClientModule } from '@angular/common/http';
import { HeaderComponent } from './layout/header/header.component';
import { FooterComponent } from './layout/footer/footer.component';
import { AppCustomLayoutComponent } from './layout/app-custom-layout/app-custom-layout.component';

import { AppRoutingModule } from './app-routing.module';

import {MatDatepickerModule} from '@angular/material/datepicker';

const routes: Routes = [
  {
    path: '',
    component: AppCustomLayoutComponent,
  },
  {
    path: 'company/:name',
    component: TableDataFormComponent
  },
];

@NgModule({
  declarations: [
    AppComponent,
    InputDataFormComponent,
    TableDataFormComponent,
    HeaderComponent,
    FooterComponent,
    AppCustomLayoutComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
