import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Consommation } from 'src/app/models/consommation';
import { map, catchError } from 'rxjs/operators';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  })
};

@Injectable()
export class ConsommationService {
  items: Consommation[] = [];
  public url: string;
  constructor(
    public _http: HttpClient
  ) {
    this.url = 'http://localhost:3000';
  }

  getDatas(date: string): Observable<any> {
    return this._http.get(this.url + `/predire/get-data/${date}`, httpOptions);
  }

  predireData(date: string): Observable<any> {
    return this._http.get(this.url + `/predire/push-data/${date}`, httpOptions);
  }
}
