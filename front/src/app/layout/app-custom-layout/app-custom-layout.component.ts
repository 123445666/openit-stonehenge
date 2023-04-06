import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'app-app-custom-layout',
  templateUrl: './app-custom-layout.component.html',
  styleUrls: ['./app-custom-layout.component.scss'],
  providers: []
})
export class AppCustomLayoutComponent implements OnInit {
  id: String;

  constructor(
    private route: ActivatedRoute, private router: Router
  ) { }

  ngOnInit(): void {
  }

}
