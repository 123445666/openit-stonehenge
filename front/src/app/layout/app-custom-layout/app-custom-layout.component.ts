import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { CompanyService } from '../../services/company.service';

@Component({
  selector: 'app-app-custom-layout',
  templateUrl: './app-custom-layout.component.html',
  styleUrls: ['./app-custom-layout.component.scss'],
  providers: [CompanyService]
})
export class AppCustomLayoutComponent implements OnInit {
  id: String;

  constructor(
    private route: ActivatedRoute, private router: Router, private _companyService: CompanyService
  ) { }

  ngOnInit(): void {
    this.id = this.route.snapshot.params['id'];
    this._companyService.checkEmploy(this.id).subscribe(
      response => {
        this.router.navigate(['/company', response]);
      },
      error => {
        console.log(<any>error);
      });
  }

}
