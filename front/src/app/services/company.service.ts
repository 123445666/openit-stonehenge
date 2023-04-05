import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Company } from 'src/app/models/company';
import { map, catchError } from 'rxjs/operators';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  })
};

@Injectable()
export class CompanyService {
  items: Company[] = [];
  public url: string;
  constructor(
    public _http: HttpClient
  ) {
    this.url = 'http://localhost:3000';
  }

  importEmploys(company: Company): Observable<any> {
    let params = JSON.stringify(company);
    return this._http.post(this.url + '/company/', params, httpOptions);
  }

  getEmploys(company: Company): Observable<any> {
    let params = JSON.stringify(company);
    return this._http.post(this.url + '/company/getemployees/', params, httpOptions);
  }

  checkEmploy(id: String): Observable<any> {
    return this._http.get(this.url + `/company/checkEmploy/${id}`);
  }

  deleteCompany( company: String): Observable<any> {
    return this._http.delete(this.url + `/company/${company}`, httpOptions);
  }

}
