import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class BookService {

  private baseUrl = 'http://localhost:3050';

  constructor(private http: HttpClient) {
  }

  public getBook(isbn: string): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/book/${isbn}`);
  }
}
