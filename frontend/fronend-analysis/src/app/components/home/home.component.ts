import { Component, ElementRef, ViewChild, QueryList, ViewChildren } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { Chart } from 'chart.js/auto';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: false,
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  repoUrl: string = '';
  selectedFile: File | null = null;
  projectGrades: { filename: string; grade: number }[] = [];
  charts: Chart[] = [];
  @ViewChild('chartCanvas', { static: false }) chartCanvas!: ElementRef;
  @ViewChildren('chartCanvas') chartCanvases!: QueryList<ElementRef>;

  constructor(private http: HttpClient, private router: Router) {}

  handleAnalyzeGitRepo() {
    if (this.repoUrl.trim() === '') {
      alert('Please enter a valid repository URL.');
      return;
    }

    // Pull the analysis response from the backend
    const requestBody = { repo_url: this.repoUrl };
    this.http.post<any>('http://127.0.0.1:5000/run-analyzer', requestBody)
      .pipe(
        catchError(error => {
          console.error('Error:', error);
          return throwError(error);
        })
      )
      .subscribe(
        response => {
          console.log('Analysis response:', response);
          this.projectGrades = response.project_grades;
          setTimeout(() => this.createCharts(), 100);
        },
        error => {
          console.error('Request failed:', error);
        }
      );
  }

  /** Handle file selection */
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  /** Upload local `.zip` file for analysis */
  uploadLocalRepo() {
    if (!this.selectedFile) {
      alert('Please select a ZIP file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post<any>('http://127.0.0.1:5000/run-analyzer', formData)
      .pipe(
        catchError(error => {
          console.error('Error:', error);
          return throwError(error);
        })
      )
      .subscribe(
        response => {
          console.log('Analysis response:', response);
          this.projectGrades = response.project_grades;
          setTimeout(() => this.createCharts(), 100);
        },
        error => {
          console.error('Request failed:', error);
        }
      );
  }

  onCardClick(file: { filename: string; grade: number }) {
    console.log(`Clicked on: ${file.filename}, Grade: ${file.grade}%`);
    this.router.navigate(['/file-details', file.filename]); // Navigate with filename as a parameter
  }

  ngAfterViewInit() {
    if (this.projectGrades.length) {
      this.createCharts();
    }  
  }

  createCharts() {
    this.charts.forEach(chart => chart.destroy()); // Clear existing charts
    this.charts = [];

    this.chartCanvases.forEach((canvas, index) => {
      const file = this.projectGrades[index];

      const chart = new Chart(canvas.nativeElement, {
        type: 'pie',
        data: {
          labels: ['Score', 'Remaining'],
          datasets: [{
            data: [file.grade, 100 - file.grade],
            backgroundColor: ['#006400', '#8B0000'],
            hoverBackgroundColor: ['#006400', '#8B0000']
          }]
        }
      });

      this.charts.push(chart);
    });
  }
}
