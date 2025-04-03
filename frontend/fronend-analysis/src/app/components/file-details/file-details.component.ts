import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Chart } from 'chart.js/auto';
import { jsPDF } from 'jspdf';

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

  downloadCSV() {
    if (!this.fileDetails?.failed_criteria?.length) {
      alert("No failed criteria available.");
      return;
    }
  
    let csvContent = "Criteria,Message,Code Snippet\n";
  
    this.fileDetails.failed_criteria.forEach((failure: any) => {
      let codeSnippet = failure.code ? failure.code.join(' ') : '';
      // Adjusting text for better readability
      csvContent += `"${failure.criteria.replace(/"/g, '""')}","${failure.message.replace(/"/g, '""')}","${codeSnippet.replace(/"/g, '""')}"\n`;
    });
  
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${this.fileName}_failures.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  }
  
  downloadPDF() {
    if (!this.fileDetails?.failed_criteria?.length) {
      alert("No failed criteria available.");
      return;
    }
  
    const doc = new jsPDF();
  
    // Set Title Font Style
    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.text(`File Analysis Report: ${this.fileName}`, 10, 10);
  
    // Reset font style for the content
    doc.setFont("helvetica", "normal");
    doc.setFontSize(12);
  
    let y = 20;
    this.fileDetails.failed_criteria.forEach((failure: any, index: number) => {
      if (y > 270) { // Avoid overflow
        doc.addPage();
        y = 20;
      }
  
      // Styling for each text block
      doc.setFont("helvetica", "normal");
      doc.setFontSize(12);
      doc.text(`Criteria: ${failure.criteria}`, 10, y);
      doc.text(`Message: ${failure.message}`, 10, y + 5);
      doc.text(`Code Snippet: ${failure.code?.join(' ') || ''}`, 10, y + 10);
      
      // Space after each failure item
      y += 20;
    });
  
    // Save PDF
    doc.save(`${this.fileName}_failures.pdf`);
  }
}
