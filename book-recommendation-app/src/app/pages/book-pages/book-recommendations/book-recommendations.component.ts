import {Component} from '@angular/core';
import {BookService} from '../book.service';
import {ActivatedRoute} from "@angular/router";
import {BookPreviewComponent} from "../../../components/book-preview/book-preview.component";

@Component({
  selector: 'app-book-recommendations',
  standalone: true,
  imports: [
    BookPreviewComponent
  ],
  templateUrl: './book-recommendations.component.html',
  styleUrl: './book-recommendations.component.css'
})
export class BookRecommendationsComponent {

  public recommendations: any[] = [];
  public bookTitle: string = '';

  constructor(private route: ActivatedRoute, private bookService: BookService) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const {isbn} = params;
      this.getBooks(isbn);
    })
    this.route.queryParams.subscribe(params => {
      const {title} = params;
      this.bookTitle = title;
    });
  }

  private getBooks(isbn: string): void {
    this.bookService.getBookRecommendation(isbn).subscribe({
      next: (response) => {
        this.recommendations = response.recommendations;
      },
      error: (error) => {
        console.error('Error fetching book recommendations', error);
      }
    });
  }
}
