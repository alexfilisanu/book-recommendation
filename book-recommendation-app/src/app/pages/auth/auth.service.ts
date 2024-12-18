import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private baseUrl = 'http://localhost:3100/auth';

  constructor(private http: HttpClient) {
  }

  public registerUser(formData: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/register`, formData);
  }

  public loginUser(formData: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/login`, formData);
  }
}
