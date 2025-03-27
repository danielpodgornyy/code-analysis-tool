import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.scss'
})

export class AppComponent {
  
  analysisResults: any; // Sam: Trying to run program, but kept giving error that this was not defined.
  
  title: string = 'Code Analysis Tool'; 
  repoUrl: string = '';  // Bind to input field in the template
  repoPath: string = '';
  output: string = '';
  projectGrades: any[] = []; // New property to store grades
  selectedFile: File | null = null;  

  constructor(private http: HttpClient) {}

  handleAnalyzeGitRepo() {
    if (this.repoUrl.trim() === '') {
      alert('Please enter a valid repository URL.');
      return;
    }

    // Pull the analysis response from the backend
    const requestBody = { repo_url: this.repoUrl };
    this.http.post<AnalysisResponse>('http://127.0.0.1:5000/run-analyzer', requestBody)
    // Not sure what the pipe is for
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
          this.output = this.constructOutput(this.projectGrades);
        },
        error => {
          console.error('Request failed:', error);
          this.output = 'An error occurred while fetching the analysis results.';
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

    this.http.post<AnalysisResponse>('http://127.0.0.1:5000/run-analyzer', formData)
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
          this.output = this.constructOutput(this.projectGrades);
        },
        error => {
          console.error('Request failed:', error);
          this.output = 'An error occurred while analyzing the uploaded ZIP file.';
        }
      );
  }

  /** Format analysis results for display */
  // THIS WILL BE CHANGED ONCE FRONTEND IS REHASHED
  constructOutput(projectGrades: any[]): string {
    return projectGrades.map(file => 
      `${file.filename}: ${file.grade}`
    ).join('\n');
  }

  // ADD THESE TWO METHODS HERE ↓
  getGradeColor(grade: any): string {
    // Convert grade to a string if it's not already
    const gradeString = typeof grade === 'string' 
      ? grade 
      : (grade?.toString() || '0');
    
    // Remove any non-numeric characters and convert to number
    const numericGrade = parseFloat(gradeString.replace(/[^\d.]/g, ''));
    
    // Handle cases where parsing fails
    if (isNaN(numericGrade)) {
      return '#ef4444'; // default to red for invalid grades
    }
  
    if (numericGrade >= 90) return '#10b981'; // green
    if (numericGrade >= 80) return '#84cc16'; // lime
    if (numericGrade >= 70) return '#eab308'; // yellow
    if (numericGrade >= 60) return '#f97316'; // orange
    return '#ef4444'; // red
  }
  
  calculateDashArray(grade: any): string {
    // Convert grade to a string if it's not already
    const gradeString = typeof grade === 'string' 
      ? grade 
      : (grade?.toString() || '0');
    
    // Remove any non-numeric characters and convert to number
    const numericGrade = parseFloat(gradeString.replace(/[^\d.]/g, ''));
    
    // Handle cases where parsing fails
    if (isNaN(numericGrade)) {
      return '0, 100'; // default to 0% if parsing fails
    }
  
    return `${numericGrade}, 100`;
  }
}

interface AnalysisResponse {
  project_grades: any;
}
