import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class BookService {

  private baseUrl = 'http://localhost:3050';

  constructor(private http: HttpClient) {
  }

  public getTotalBooks(query: string): Observable<any> {
    const params = new HttpParams()
      .set('q', query);

    return this.http.get<any>(`${this.baseUrl}/total-books`, {params});
  }

  public getBooks(query: string, page: number = 1, limit: number = 10): Observable<any> {
    const params = new HttpParams()
      .set('q', query)
      .set('page', page.toString())
      .set('limit', limit.toString());

    return this.http.get<any>(`${this.baseUrl}/books`, {params});
  }

  public getBook(isbn: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/book/${isbn}`);
  }

  public getBookRecommendation(isbn: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/book/recommendations/${isbn}`);
  }
}
