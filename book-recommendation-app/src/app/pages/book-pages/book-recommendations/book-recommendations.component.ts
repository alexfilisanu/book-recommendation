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
  public displayedRecommendations: any[] = [];
  public bookTitle: string = '';
  public currentPage: number = 1;
  public totalBooks: number = 0;
  public totalPages: number = 0;
  private booksPerPage: number = 4;

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
      this.currentPage = 1;
    });
  }

  private getBooks(isbn: string): void {
    this.bookService.getBookRecommendation(isbn).subscribe({
      next: (response) => {
        this.recommendations = response.recommendations;
        this.totalBooks = this.recommendations.length;
        this.totalPages = Math.ceil(this.totalBooks / this.booksPerPage);
        this.updateDisplayedRecommendations();
      },
      error: (error) => {
        console.error('Error fetching book recommendations', error);
      }
    });
  }

  private updateDisplayedRecommendations(): void {
    const start = (this.currentPage - 1) * this.booksPerPage;
    const end = start + this.booksPerPage;
    this.displayedRecommendations = this.recommendations.slice(start, end);
  }

  public nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.updateDisplayedRecommendations();
    }
  }

  public previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.updateDisplayedRecommendations();
    }
  }
}
