import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Chart } from 'chart.js/auto';

@Component({
  selector: 'app-file-details',
  standalone: false,
  templateUrl: './file-details.component.html',
  styleUrl: './file-details.component.scss'
})
export class FileDetailsComponent implements OnInit, AfterViewInit {
  @ViewChild('gradeChart') gradeChartCanvas!: ElementRef;
  fileName: string = '';
  fileDetails: any = null;
  errorMessage: string = '';
  chart: any = null;


  constructor(private http: HttpClient, private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.fileName = params.get('filename') || '';
      if (this.fileName) {
        this.getFileDetails();
      }
    });
  }

  ngAfterViewInit() {
    // Ensure chart creation only happens after view is initialized
    if (this.fileDetails) {
      setTimeout(() => this.createChart(), 100);
    }
  }

  getFileDetails() {
    if (!this.fileName.trim()) {
      this.errorMessage = 'Invalid file name.';
      return;
    }

    this.http.get<any>(`http://127.0.0.1:5000/get-file-results?filename=${this.fileName}`)
      .subscribe(
        response => {
          this.fileDetails = response || null;
          this.errorMessage = '';
          setTimeout(() => this.createChart(), 100); // Ensure ViewChild is ready
        },
        error => {
          this.errorMessage = error.error?.error || 'Failed to fetch file details.';
          this.fileDetails = null;
        }
      );
  }

  createChart() {
    if (!this.gradeChartCanvas) return;


    if (this.chart) {
      this.chart.destroy(); // Destroy previous chart if exists
    }

    this.chart = new Chart(this.gradeChartCanvas.nativeElement, {
      type: 'pie',
      data: {
        labels: ['Score', 'Remaining'],
        datasets: [{
          data: [this.fileDetails.grade, 100 - this.fileDetails.grade],
          backgroundColor: ['#006400', '#8B0000'],
          hoverBackgroundColor: ['#228B22', '#B22222']
        }]
      }
    });
  }
}
