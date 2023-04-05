import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from "@angular/router";
import { FormArray } from '@angular/forms';
import { CompanyService } from '../../services/company.service';

@Component({
  selector: 'app-input-data-form',
  templateUrl: './input-data-form.component.html',
  styleUrls: ['./input-data-form.component.css'],
  providers: [CompanyService],
})
export class InputDataFormComponent implements OnInit {
  submitted = false;
  predireForm = this.formBuilder.group({
    name: [''],
    domain: ['']
  });

  constructor(
    private _companyService: CompanyService, private router: Router, private formBuilder: FormBuilder,
  ) {
  }

  ngOnInit() {
    this.predireForm.get("name").valueChanges.subscribe(selectedValue => {
      this.submitted = false;
    })
    this.predireForm.get("domain").valueChanges.subscribe(selectedValue => {
      this.submitted = false;
    })
  }

  onSubmit() {
    this.submitted = true;
    this.predireForm.value.data_date = this.predireForm.value.data_date.toLowerCase();
    this._companyService.importEmploys(this.predireForm.value).subscribe(
      response => {
        let path = '/';
        this.router.navigate([path]);
      },
      error => {
        console.log(<any>error);
      });
  }

}


/*
Copyright Google LLC. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at https://angular.io/license
*/
