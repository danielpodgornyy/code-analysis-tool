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
          this.output = this.constructOutput(response.files, response.analysis);
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
          this.analysisResults = response.analysis;
          this.output = this.constructOutput(response.files, response.analysis);
        },
        error => {
          console.error('Request failed:', error);
          this.output = 'An error occurred while analyzing the uploaded ZIP file.';
        }
      );
  }

  /** Format analysis results for display */
  // THIS WILL BE CHANGED ONCE FRONTEND IS REHASHED
  constructOutput(files: string[], analysis: any): string {
    let resultOutput = '';

    // Lists out the files within the repo
    if (files.length === 0) {
      return 'No files found in the repository.\n'; // Automatically return since there's no work to be done 
    } else { 
      resultOutput += `Files found in the repository:\n`;
      files.forEach(file => {
        resultOutput += `\n- ${file}`;
      });
    }

    resultOutput += '\n\nAnalysis Results:\n';

    // Iterates over every file name returned, 
    Object.keys(analysis).forEach(file => {
      const fileIssues = analysis[file]; 
      let healthy = true; // Keeps track of the health of each class

      resultOutput += `\n${file}:\n`; // File name
      Object.keys(fileIssues).forEach(criterion => {
        const violations = fileIssues[criterion];

        if (violations.length > 0) {
          healthy = false;

          resultOutput += `${criterion.charAt(0).toUpperCase() + criterion.slice(1)} Violations:\n`; //
          violations.forEach((violation: any) => {
            resultOutput += `- ${violation}\n`;
          });
        }
      });

      // If no criterion is marked, then it is healthy
      if (healthy) {
          resultOutput += `No issues found. File is healthy.\n`;
      }
    });

    return resultOutput;
  }

}

interface AnalysisResponse {
  files: string[];
  analysis: { [file: string]: { [criterion: string]: string[] } };  // Analysis result for each file and criterion
}
