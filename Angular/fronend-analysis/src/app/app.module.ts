import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration, withEventReplay } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { HttpClientModule  } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { initializeApp, provideFirebaseApp } from '@angular/fire/app';
import { getAuth, provideAuth } from '@angular/fire/auth';
import { getFirestore, provideFirestore } from '@angular/fire/firestore';
import { getStorage, provideStorage } from '@angular/fire/storage';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    provideClientHydration(withEventReplay()),
    provideFirebaseApp(() => initializeApp({ projectId: "code-analysis-a27ff", appId: "1:1020108267358:web:e1f017673c4be2e64939cf", storageBucket: "code-analysis-a27ff.firebasestorage.app", apiKey: "AIzaSyBy9ohipSmrQvI_7QRJvxKHi0Uy0wtWz00", authDomain: "code-analysis-a27ff.firebaseapp.com", messagingSenderId: "1020108267358" })),
    provideAuth(() => getAuth()),
    provideFirestore(() => getFirestore()),
    provideStorage(() => getStorage())
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
