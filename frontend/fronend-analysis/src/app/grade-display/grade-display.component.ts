import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-grade-display',
  templateUrl: './grade-display.component.html',
  styleUrls: ['./grade-display.component.scss'],
  standalone: true,
  imports: [CommonModule]
})
export class GradeDisplayComponent {
  @Input() grade: any;
  @Input() filename: string = '';

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