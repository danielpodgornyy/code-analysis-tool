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
  title = 'Code Analysis Tool';
  repoUrl: string = '';  // Bind to input field in the template
  repoPath = '';
  output = '';
  analysisResults: any = {};  // Store analysis results for display


  constructor(private http: HttpClient) {}

  analyze() {
    if (this.repoUrl.trim() === '') {
      alert('Please enter a valid repository URL.');
      return;
    }

    const requestBody = { repo_url: this.repoUrl };  // Ensure repo_url is correctly passed

    this.http.post<AnalysisResponse>('http://127.0.0.1:5000/run-analyzer', requestBody)
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
          this.analysisResults = response.analysis;

          // Construct a user-friendly output
          this.output = this.constructOutput(response.files, this.analysisResults);
        },
        error => {
          console.error('Request failed:', error);
          // Handle the error appropriately, show error message in the UI
          this.output = 'An error occurred while fetching the analysis results.';
        }
      );
  }

  constructOutput(files: string[], analysis: any): string {
    let resultOutput = '';

    // Check if there are any files to analyze
    if (files.length === 0) {
      resultOutput += 'No files found in the repository.\n';
    } else {
      resultOutput += `Files found in the repository:\n`;
      files.forEach(file => {
        resultOutput += `\n- ${file}`;
      });

      // Analyze each file's issues
      resultOutput += '\n\nAnalysis Results:\n';
      Object.keys(analysis).forEach(file => {
        const fileIssues = analysis[file];
        resultOutput += `\n${file}:\n`;

        let healthy = true;
        Object.keys(fileIssues).forEach(criterion => {
          const violations = fileIssues[criterion];
          if (violations.length > 0) {
            healthy = false;
            resultOutput += `${criterion.charAt(0).toUpperCase() + criterion.slice(1)} Violations:\n`;
            violations.forEach((violation: any) => {
              resultOutput += `- ${violation}\n`;
            });
          }
        });

        if (healthy) {
          resultOutput += `No issues found. File is healthy.\n`;
        }
      });
    }

    return resultOutput;
  }

}

interface AnalysisResponse {
  files: string[];
  analysis: { [file: string]: { [criterion: string]: string[] } };  // Analysis result for each file and criterion
}