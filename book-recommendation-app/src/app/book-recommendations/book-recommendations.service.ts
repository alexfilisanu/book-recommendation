import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class BookRecommendationsService {

  private baseUrl = 'http://localhost:3050';

  constructor(private http: HttpClient) {
  }

  public getBookRecommendation(isbn: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/book/recommendations/${isbn}`);
  }
}
