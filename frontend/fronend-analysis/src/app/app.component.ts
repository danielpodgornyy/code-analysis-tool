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
          // Handle the response, display results in the UI

          // Construct a user-friendly output
          this.output = this.constructOutput(response.project_grades);
        },
        error => {
          console.error('Request failed:', error);
          // Handle the error appropriately, show error message in the UI
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
          this.output = this.constructOutput(response.project_grades);
        },
        error => {
          console.error('Request failed:', error);
          this.output = 'An error occurred while analyzing the uploaded ZIP file.';
        }
      );
  }

  /** Format analysis results for display */
  // THIS WILL BE CHANGED ONCE FRONTEND IS REHASHED
  constructOutput(projectGrades: any): string {
    let resultOutput = '';

    resultOutput += '\n\nAnalysis Results:\n';

    projectGrades.forEach((file_result: any) => {
        resultOutput += `\n ${file_result['filename']}`;
        resultOutput += `\n ${file_result['grade']}`;
    })

    return resultOutput;
  }

}

interface AnalysisResponse {
  project_grades: any;
}
