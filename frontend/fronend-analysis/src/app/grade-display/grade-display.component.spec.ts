import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GradeDisplayComponent } from './grade-display.component';

describe('GradeDisplayComponent', () => {
  let component: GradeDisplayComponent;
  let fixture: ComponentFixture<GradeDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GradeDisplayComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GradeDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
