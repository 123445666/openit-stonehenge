import { Component, OnInit, AfterViewInit, ElementRef, ViewChild, OnDestroy } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from "@angular/router";
import { FormArray } from '@angular/forms';
import { ConsommationService } from '../../services/consommation.service';
import * as moment from 'moment';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

@Component({
  selector: 'app-input-data-form',
  templateUrl: './input-data-form.component.html',
  styleUrls: ['./input-data-form.component.css'],
  providers: [ConsommationService],
})
export class InputDataFormComponent implements OnInit {
  @ViewChild('chartCanvas') chartCanvas: ElementRef;
  predireForm = this.formBuilder.group({
    data_date: [new Date()]
  });

  consommations: any = [];
  iday = 0;

  constructor(
    private _consommationService: ConsommationService, private router: Router, private formBuilder: FormBuilder,
  ) {
  }

  ngOnInit() {
  }

  async onPredire() {
    console.log(this.predireForm.value.data_date);
    var nextDay = moment(this.predireForm.value.data_date);

    const dateString = moment(nextDay).format('DD-MM-YYYY');
    console.log(dateString);

    await this._consommationService.predireData(dateString).subscribe(
      response => {
      },
      error => {
        console.log(<any>error);
      });
  }

  async onSearch() {
    this.iday = 0;
    console.log(this.predireForm.value.data_date);
    await this.getDataPredict(this.predireForm.value.data_date);
  }

  async getDataPredict(datePredict: any) {
    var nextDay = moment(datePredict).add(this.iday, 'days');
    this.iday = this.iday + 1;

    const dateString = moment(nextDay).format('DD-MM-YYYY');

    this._consommationService.getDatas(dateString).subscribe(
      response => {
        this.consommations = response;
        this.drawChart();
      },
      error => {
        console.log(<any>error);
      });
  }

  groupConsumptionByDate(data) {
    const groupedData = {};

    data.forEach(({ data_date, hour, consommation }) => {
      if (!groupedData[data_date]) {
        groupedData[data_date] = {
          morning: 0,
          afternoon: 0,
          night: 0,
        };
      }

      if (hour >= 5 && hour < 12) {
        groupedData[data_date].morning += Math.round(consommation);
      } else if (hour >= 13 && hour < 19) {
        groupedData[data_date].afternoon += Math.round(consommation);
      } else if (hour >= 20 || hour < 4) {
        groupedData[data_date].night += Math.round(consommation);
      }
    });

    return groupedData;
  }

  chart: Chart;

  drawChart() {
    const chartLabels: string[] = [];
    const chartData: number[][] = [[], [], []];

    if (this.chart) {
      this.chart.destroy();
    }

    for (const item of this.consommations) {
      chartLabels.push(item.data_date);
      chartData[0].push(item.consommation);
    }


    const canvas = this.chartCanvas.nativeElement;
    this.chart = new Chart(canvas, {
      type: 'line',
      data: {
        labels: chartLabels,
        datasets: [
          {
            label: 'Consommation prédite',
            data: chartData[0],
            backgroundColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 206, 86, 1)', 'rgba(255, 99, 132, 1)'],
            borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 206, 86, 1)', 'rgba(255, 99, 132, 1)'],
            borderWidth: 1
          }
        ]
      },
      options: {
        scales: {
          y: {
            type: 'linear',
            ticks: {
              stepSize: 50000
            }
          }
        }
      }
    });
  }
}


/*
Copyright Google LLC. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at https://angular.io/license
*/
